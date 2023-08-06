from pytorch_common.callbacks import Callback
from pytorch_common.modules import Fn


class Validation(Callback):
    """
    This callback allows to validation model performance into a validation using one or more specified validation metrics.
    """

    def __init__(self, data_loader, metrics, each_n_epochs=1, validation_fn = Fn.validation):
        """
        Validation callback constructor.
        :param data_loader: validation set data_loader.
        :param metrics: a dict with each metric name and calculation function. i.e.:

            metrics={
                'val_loss': lambda y_pred, y_true: BCELoss()(y_pred, y_true).item(),
                'val_auc':  lambda y_pred, y_true: roc_auc_score(y_true.cpu().numpy(), y_pred.cpu().numpy())
            }

        :param each_n_epochs: number of epochs to wait to calculate validation metrics.
        :validation_fn: Validation callback. Usefull to override the default validation process.
        """
        self.data_loader   = data_loader
        self.metrics       = metrics
        self.each_n_epochs = each_n_epochs
        self.validation_fn = validation_fn


    def on_after_train(self, ctx):
        if ctx.epoch % self.each_n_epochs == 0:
            y_pred, y_true = Fn.validation(ctx, self.data_loader)
            ctx['time'] = ctx.stopwatch.to_str()
            for (name, fn) in self.metrics.items():
                ctx[name] = fn(y_pred, y_true)
        else:
            for (name, fn) in self.metrics.items():
                ctx[name] = None
