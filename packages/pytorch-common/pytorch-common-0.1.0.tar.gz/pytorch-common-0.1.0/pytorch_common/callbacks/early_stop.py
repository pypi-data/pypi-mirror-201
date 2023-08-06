from pytorch_common.callbacks import Callback
from pytorch_common.callbacks.mixin.metric_improve_mixin import MetricImproveMixin


class EarlyStop(MetricImproveMixin, Callback):
    """
    Stop training when model has stopped improving a specified metric.
    """

    def __init__(self, metric, mode='min', patience=10):
        """
        :param metric (str): Metric used to check model performance improving.
        :param mode (str): One of `min`, `max`. In `min` mode check that metric go down after each epoch.
        :param patience (int): Number of epochs with no metric improvement.
        """
        self._init('early_stop', metric, mode)
        self.__patience = patience

    def on_init(self, ctx): ctx['patience'] = 0

    def _on_improve(self, ctx, mode): self.on_init(ctx)

    def _on_not_improve(self, ctx):
        ctx['patience'] += 1
        ctx['early_stop'] = (ctx['patience'] == self.__patience)
