import logging

from pytorch_common.callbacks.output import OutputCallback


class Logger(OutputCallback):
    """
    Logs context properties. In general is used to log performance metrics every n epochs. i.e.:

        metrics=['time', 'epoch', 'train_loss', 'val_loss', 'val_auc', 'patience', 'lr']

    """

    def __init__(self, metrics=['time', 'epoch', 'train_loss'], each_n_epochs=1):
        super().__init__(each_n_epochs)
        self.metrics = metrics

    def can_plot(self, ctx): return True

    def on_show(self, ctx):
        logging.info({m: ctx[m] for m in self.metrics if m in ctx and ctx[m] is not None})
