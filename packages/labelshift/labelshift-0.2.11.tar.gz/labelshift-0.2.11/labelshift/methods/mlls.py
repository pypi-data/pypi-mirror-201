import numpy as np

from labelshift.utils import to_one_hot, softmax, to_hard_labels

from .base import BaseEstimator


class MLLS(BaseEstimator):
    def __init__(self, hard_label=False, calibrator=None, tolerance=1e-6, max_iterations=100, verbose=False):
        self.verbose = verbose
        self.tolerance = tolerance
        self.hard_label = hard_label
        self.calibrator = calibrator
        self.max_iterations = max_iterations
        self.estim_source_dist = None  # estimate source class distribution
        self.estim_target_dist = None  # estimate target class distribution
        self.imp_weights = None  # importance weights

    def __str__(self):
        return "Maximum Likelihood Label Shift (MLLS)"

    def __copy__(self):
        calirator_copy = self.calibrator.__copy__() if self.calibrator is not None else None
        mlls_copy = MLLS(self.hard_label, calirator_copy, self.tolerance, self.max_iterations, self.verbose)
        mlls_copy.estim_source_dist = self.estim_source_dist
        mlls_copy.estim_target_dist = self.estim_target_dist
        mlls_copy.imp_weights = self.imp_weights
        return mlls_copy

    # TODO: add torch.tensor type support for target_logits, src_logits, src_labels
    def fit(self, target_logits, src_logits, src_labels=None):
        if src_labels is not None:
            src_labels = to_one_hot(src_labels)

        if self.calibrator is not None:
            assert src_labels is not None, "source_labels can't be None"
            self.calibrator.fit(src_logits, src_labels)
            src_logits = self.calibrator.calibrate(src_logits)
            target_logits = self.calibrator.calibrate(target_logits)
        else:
            src_logits = softmax(src_logits)
            target_logits = softmax(target_logits)

        if self.hard_label:
            target_logits = to_hard_labels(target_logits, one_hot=True)
            src_logits = to_hard_labels(src_logits, one_hot=True)

        est_src_dist = np.mean(src_labels, axis=0)
        est_src_dist = est_src_dist / np.sum(est_src_dist)  # normalize

        est_target_dist = est_src_dist
        for _ in range(self.max_iterations):
            est_target_posterior_probs = target_logits * (est_target_dist / est_src_dist)[None, :]
            est_target_posterior_probs = est_target_posterior_probs / np.sum(est_target_posterior_probs, axis=-1)[:, None]
            next_est_target_dist = np.mean(est_target_posterior_probs, axis=0)
            if np.all(np.abs(next_est_target_dist - est_target_dist) <= self.tolerance):
                break
            est_target_dist = next_est_target_dist

        self.estim_source_dist = est_src_dist
        self.estim_target_dist = next_est_target_dist
        self.imp_weights = self.estim_target_dist / self.estim_source_dist

        if self.verbose:
            with np.printoptions(precision=3, suppress=True, formatter={"float": "{: 0.3f}".format}):
                print(f"Est Source Class Distribution: {self.estim_source_dist}")
                print(f"Est Target Class Distribution: {self.estim_target_dist}")
                print(f"Est Importance Weights       : {self.imp_weights}")

        return self
