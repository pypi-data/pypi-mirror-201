import torch
from pytorch_common.modules import Fn
from .fit_context   import FitContextFactory


class PredictMixin:
    def evaluate(self, data_loader):
        """Evaluate a data_loader to model.

        Args:
            data_loader: a data_loder.

        Returns:
            a (y_pre, y_true) tuple
        """
        ctx = FitContextFactory(self)
        return Fn.validation(ctx, data_loader)


    def evaluate_score(self, data_loader, score_fn):
        """Evaluate a data_loader to model and apply score_fn to result.

        Args:
            data_loader: a data_loder.
            score_fn: Custom funcion used to evaluate model performance. i.e: MSE, RMSE, Binary Cross Entropy, etc...

        Returns:
            score function result.
        """
        return Fn.validation_score(self, data_loader, score_fn)


    def predict(self, features):
        self.eval()
        with torch.no_grad():
            return self(features.to(self.device))
