# import needed library
import json
import copy
import random
import shutil
import logging
import warnings
import numpy as np
from pathlib import Path
from sklearn.metrics import mean_squared_error

import torch
import torch.nn.parallel
import torch.backends.cudnn as cudnn
from torchvision import transforms

from labelshift.trainer import ModelTrainer
from labelshift.get_method import get_lse_methods
from labelshift.datasets import get_data_loader, BasicDataset, ResampleDataset, ResampleDataset
from labelshift.utils import get_net_builder, get_optimizer, get_cosine_schedule_with_warmup, over_write_args_from_dict, Config


class LSE:
    def __init__(self, args=None, **kwargs):
        if args is not None:
            args = over_write_args_from_dict(args, kwargs)
            self.cfg = over_write_args_from_dict(Config(), args.__dict__)
        else:
            self.cfg = Config(**kwargs)

        print(f"\n{self.cfg}\n")
        if Path(self.cfg.save_folder).exists() and self.cfg.overwrite:
            shutil.rmtree(self.cfg.save_folder)

    def train_base_models(self, lb_data, lb_targets, num_classes=None, train_transform=None, test_transform=None, seed=None):
        self.pre_check()

        if num_classes is not None:
            self.cfg.num_classes = num_classes
        assert self.cfg.num_classes > 0, "please provide the number of classes"

        train_transform = train_transform if train_transform is not None else transforms.ToTensor()
        test_transform = test_transform if test_transform is not None else transforms.ToTensor()

        random_state = random.getstate()
        np_random_state = np.random.get_state()
        torch_random_state = torch.random.get_rng_state()

        if seed is not None:
            warnings.warn(
                "You have chosen to seed training. "
                "This will turn on the CUDNN deterministic setting, "
                "which can slow down your training considerably! "
                "You may see unexpected behavior when restarting "
                "from checkpoints.\n"
            )
            random.seed(seed)
            torch.manual_seed(seed)
            np.random.seed(seed)
            cudnn.deterministic = True

        cudnn.benchmark = True

        net_builder = get_net_builder(self.cfg.net, self.cfg.net_from_name)

        # Construct Dataset & DataLoader
        lb_dataset = ResampleDataset(
            lb_data, lb_targets, self.cfg.num_classes, train_transform, test_transform, onehot=False, seed=self.cfg.seed
        )

        for idx, train_lb_dset, val_lb_dset in lb_dataset.resample(self.cfg.num_val_per_class, self.cfg.num_ensemble):
            print(f"\nTraining [{idx}/{self.cfg.num_ensemble}] Model")

            save_model_path = Path(self.cfg.save_folder) / "models" / f"model_{idx}.pt"
            save_val_logits_path = Path(self.cfg.save_folder) / "models" / f"val_logits_{idx}.pt"

            if save_model_path.exists() and save_val_logits_path.exists():
                print(f"found existing model at {save_model_path}")
                print(f"found existing validation logits at {save_val_logits_path}, skip training.\n")
                continue
            
            loader_dict = {}
            dataset_dict = {"train_lb": train_lb_dset, "val_lb": val_lb_dset}

            loader_dict["train_lb"] = get_data_loader(
                dataset_dict["train_lb"],
                self.cfg.batch_size,
                data_sampler=self.cfg.train_sampler,
                num_iters=self.cfg.num_train_iter,
                num_workers=self.cfg.num_workers,
                replacement=False,
            )
            loader_dict["val_lb"] = get_data_loader(
                dataset_dict["val_lb"], self.cfg.eval_batch_size, num_workers=self.cfg.num_workers, drop_last=False
            )
            
            model = ModelTrainer(net_builder, self.cfg.num_classes, num_eval_iter=self.cfg.num_eval_iter, ema_m=self.cfg.ema_m, save_path=save_model_path)
            # SET Optimizer & LR Scheduler
            ## construct SGD and cosine lr scheduler
            optimizer = get_optimizer(model.model, self.cfg.optim, self.cfg.lr, self.cfg.momentum, self.cfg.weight_decay)
            scheduler = get_cosine_schedule_with_warmup(optimizer, self.cfg.num_train_iter, num_warmup_steps=self.cfg.num_train_iter * 0)
            ## set SGD and cosine lr
            model.set_optimizer(optimizer, scheduler)

            if self.cfg.gpu is not None:
                torch.cuda.set_device(self.cfg.gpu)
                model.model = model.model.cuda(self.cfg.gpu)
            else:
                model.model = torch.nn.DataParallel(model.model).cuda()

            model.ema_model = copy.deepcopy(model.model)

            ## set DataLoader
            model.set_dataset(dataset_dict)
            model.set_data_loader(loader_dict)

            # START TRAINING
            model.train(self.cfg)
            # Load Best Model
            model.load_model(save_model_path)

            raw_val_outputs, val_targets = model.get_logits(loader_dict["val_lb"], args=self.cfg)
            logits = {"val_logits": raw_val_outputs, "val_targets": val_targets}
            torch.save(logits, save_val_logits_path)

        random.setstate(random_state)
        np.random.set_state(np_random_state)
        torch.random.set_rng_state(torch_random_state)

        logging.warning("\nTraining is FINISHED\n")

    def pre_check(self):
        if not torch.cuda.is_available():
            raise Exception("ONLY GPU TRAINING IS SUPPORTED")

        if self.cfg.gpu is not None:
            warnings.warn("You have chosen a specific GPU. This will completely disable data parallelism.")

    def estimate(self, ulb_data, ulb_dist=None, test_transform=None, save_name=None, verbose=False):
        test_transform = test_transform if test_transform is not None else transforms.ToTensor()

        # Construct Dataset & DataLoader
        ulb_dset = BasicDataset(ulb_data, None, self.cfg.num_classes, test_transform, is_ulb=True, onehot=False)

        logits = self.get_logits(ulb_dset)
        estimations = self.apply_lse(logits)

        with np.printoptions(precision=3, suppress=True, formatter={"float": "{: 0.3f}".format}):
            if verbose:
                print(f"\nTarget distribution: {ulb_dist}")
                print("\nEstimations:")

            mse = None
            for name, est_target_dist in estimations.items():
                if ulb_dist is not None:
                    mse = mean_squared_error(ulb_dist, est_target_dist)
                    estimations[name] = {"estimation": est_target_dist.tolist(), "mse": mse}
                    if verbose:
                        print(f"{name}: {est_target_dist}, MSE: {mse:.5f}")
                else:
                    estimations[name] = {"estimation": est_target_dist.tolist()}
                    if verbose:
                        print(f"{name}: {est_target_dist}")

        if save_name is not None:
            save_est_path = Path(self.cfg.save_folder) / f"{save_name}.json"
            with open(save_est_path, "w") as f:
                json.dump(estimations, f, indent=4)
            if verbose:
                print(f"\nestimations Saved Successfully: {save_est_path}")

        return estimations

    def get_logits(self, ulb_dset):
        net_builder = get_net_builder(self.cfg.net, self.cfg.net_from_name)

        logits = {"val_logits": [], "val_targets": [], "ulb_logits": []}
        ulb_loader = get_data_loader(ulb_dset, self.cfg.eval_batch_size, num_workers=self.cfg.num_workers, drop_last=False)
        model = ModelTrainer(net_builder, self.cfg.num_classes, num_eval_iter=self.cfg.num_eval_iter, ema_m=self.cfg.ema_m)

        if self.cfg.gpu is not None:
            torch.cuda.set_device(self.cfg.gpu)
            model.model = model.model.cuda(self.cfg.gpu)
        else:
            model.model = torch.nn.DataParallel(model.model).cuda()

        model.ema_model = copy.deepcopy(model.model)

        for idx in range(self.cfg.num_ensemble):
            val_logits_path = Path(self.cfg.save_folder) / "models" / f"val_logits_{idx}.pt"
            if val_logits_path.exists():
                data = torch.load(val_logits_path)
                logits["val_logits"].append(data["val_logits"])
                logits["val_targets"].append(data["val_targets"])
            else:
                raise RuntimeError(f"Can't find validation logits at {val_logits_path}, please run train_models() first.")

            model_path = Path(self.cfg.save_folder) / "models" / f"model_{idx}.pt"
            if model_path.exists():
                model.load_model(model_path)
            else:
                raise RuntimeError(f"Can't find model at {model_path}, please run train_models() first.")

            raw_outputs, _ = model.get_logits(ulb_loader, args=self.cfg)
            logits["ulb_logits"].append(raw_outputs)

        return logits

    def apply_lse(self, logits):
        if self.cfg.lse_algs is None:
            raise RuntimeError("please provide a lse algorithm")

        assert len(logits["ulb_logits"]) == len(logits["val_logits"]) == len(logits["val_targets"]) >= self.cfg.num_ensemble
        ulb_logits = logits["ulb_logits"][: self.cfg.num_ensemble]
        val_logits = logits["val_logits"][: self.cfg.num_ensemble]
        val_targets = logits["val_targets"][: self.cfg.num_ensemble]

        estimations = {}
        names, estimators = get_lse_methods(self.cfg.lse_algs, self.cfg.calibrations, use_ensemble=True)
        for name, estimator in zip(names, estimators):
            estimator.fit(ulb_logits, val_logits, val_targets)
            estimations[name] = estimator.estim_target_dist

        return estimations
