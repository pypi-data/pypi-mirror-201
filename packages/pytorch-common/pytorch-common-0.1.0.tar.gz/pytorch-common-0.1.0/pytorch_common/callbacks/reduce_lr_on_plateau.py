from pytorch_common.callbacks import Callback
from torch.optim import lr_scheduler


class ReduceLROnPlateau(Callback):
    """Reduce learning rate when a metric has stopped improving.
    Models often benefit from reducing the learning rate by a factor
    of 2-10 once learning stagnates. This scheduler reads a metrics
    quantity and if no improvement is seen for a 'patience' number
    of epochs, the learning rate is reduced. See ReduceLROnPlateau.
    """

    def __init__(
            self,
            mode='min',
            factor=0.1,
            patience=10,
            metric='val_loss',
            threshold=1e-4,
            threshold_mode='rel',
            cooldown=0,
            min_lr=0,
            eps=1e-8
    ):
        """
        Args:
            :param mode (str): One of `min`, `max`. In `min` mode, lr will
                be reduced when the quantity monitored has stopped
                decreasing; in `max` mode it will be reduced when the
                quantity monitored has stopped increasing. Default: 'min'.

            :param factor (float): Factor by which the learning rate will be
                reduced. new_lr = lr * factor. Default: 0.1.

            :param patience (int): Number of epochs with no improvement after
                which learning rate will be reduced. For example, if
                `patience = 2`, then we will ignore the first 2 epochs
                with no improvement, and will only decrease the LR after the
                3rd epoch if the loss still hasn't improved then.
                Default: 10.

            :param metric: metric used to control learning rate reduction.

            :param threshold (float): Threshold for measuring the new optimum,
                to only focus on significant changes. Default: 1e-4.

            :param threshold_mode (str): One of `rel`, `abs`. In `rel` mode,
                dynamic_threshold = best * ( 1 + threshold ) in 'max'
                mode or best * ( 1 - threshold ) in `min` mode.
                In `abs` mode, dynamic_threshold = best + threshold in
                `max` mode or best - threshold in `min` mode. Default: 'rel'.

            :param cooldown (int): Number of epochs to wait before resuming
                normal operation after lr has been reduced. Default: 0.

            :param min_lr (float or list): A scalar or a list of scalars. A
                lower bound on the learning rate of all param groups
                or each group respectively. Default: 0.

            :param eps (float): Minimal decay applied to lr. If the difference
                between new and old lr is smaller than eps, the update is
                ignored. Default: 1e-8.

            :param verbose (bool): If ``True``, prints a message to stdout for
                each update. Default: ``False``.
        """
        self.scheduler = None
        self.mode = mode
        self.factor = factor
        self.patience = patience
        self.metric = metric
        self.threshold = threshold
        self.threshold_mode = threshold_mode
        self.cooldown = cooldown
        self.min_lr = min_lr
        self.eps = eps

    def on_init(self, ctx):
        self.scheduler = lr_scheduler.ReduceLROnPlateau(
            ctx.optimizer,
            mode=self.mode,
            factor=self.factor,
            patience=self.patience,
            threshold=self.threshold,
            threshold_mode=self.threshold_mode,
            cooldown=self.cooldown,
            min_lr=self.min_lr,
            eps=self.eps
        )

    def on_after_train(self, ctx):
        if self.metric in ctx and ctx[self.metric] is not None:
            self.scheduler.step(ctx[self.metric])

        for param_group in ctx.optimizer.param_groups:
            ctx['lr'] = param_group['lr']
