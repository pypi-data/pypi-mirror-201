from bunch import Bunch

from pytorch_common.callbacks import Callback
from pytorch_common.callbacks.output import Logger
from pytorch_common.util import Stopwatch


class CallbackManager:
    def __init__(self, ctx, callbacks=[Logger()]):
        self.callbacks = callbacks
        self.ctx = ctx
        Callback.invoke_on_init(ctx, callbacks)

    def on_epoch_start(self, epoch):
        self.ctx.stopwatch.reset()
        self.ctx.epoch = epoch + 1

    def on_epoch_end(self, train_loss, val_loss=None):
        self.ctx.train_loss = train_loss
        self.ctx.val_loss = val_loss
        self.ctx.time = self.ctx.stopwatch.to_str()
        Callback.invoke_on_after_train(self.ctx, self.callbacks)

    def break_training(self):
        return 'early_stop' in self.ctx and self.ctx.early_stop is True