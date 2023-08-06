import logging
from datetime import datetime

import torch
from pytorch_common.callbacks import Callback
from pytorch_common.callbacks.mixin.metric_improve_mixin import MetricImproveMixin
from pytorch_common.util import create_path


class SaveBestModel(MetricImproveMixin, Callback):
    """
    Save model weights to file while model validation metric improve.
    """

    def __init__(self, metric, path='./weights', mode='min', experiment_name='experiment',
                 time_pattern='%Y-%m-%d_%H-%M-%S'):
        self._init('checkpoint', metric, mode)
        self.__path = create_path(path)
        self.__time_pattern = time_pattern
        self.__experiment_name = experiment_name

    def _update_last_metric(self, ctx):
        if not self._has_last_metric(ctx) or self._did_improve_metric(ctx):
            super()._update_last_metric(ctx)

    def _on_improve(self, ctx, mode):
        file_path = self.__get_file_path(ctx)
        logging.info("Save best model: {}".format(file_path))
        torch.save(ctx.model.state_dict(), file_path)
        ctx['best_model_path'] = file_path

    def __get_file_path(self, ctx):
        return '{}/{}--{}--epoch_{}--{}_{}.pt'.format(
            self.__path,
            datetime.now().strftime(self.__time_pattern),
            self.__experiment_name,
            ctx.epoch,
            self._metric_name,
            self._metric(ctx)
        )
