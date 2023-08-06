from pytorch_common.callbacks               import CallbackManager
from pytorch_common.callbacks.output        import Logger
from pytorch_common.modules                 import Fn
from pytorch_common.modules.common_mixin    import CommonMixin
from .fit_context                           import FitContextFactory


class FitMixin(CommonMixin):
    def fit(
            self,
            data_loader,
            loss_fn,
            epochs,
            optimizer,
            callbacks = [Logger()],
            verbose   = 1,
            extra_ctx = {},
            train_fn  = Fn.train
    ):
        """
        Train a model using data_loader data. It implement a common training workflow that is responsible to invoke callbacks and train/evalidation functions.
        to custom training and evaluation process you can use a custom train_fn(param) and evaluate_fn(Under Evaluation callback).
        Also could create custom callbacks extending from Callback or OutputCallback base classes. i.e: To plot realtime matrics during train process, etc..

        :param data_loader: data_loader with train set.
        :param loss_fn: function to minimize.
        :param epochs: number of epochs to train model.
        :param optimizer: optimizer used to adjust model.
        :param callbacks: callback collection. See Callback.
        :param verbose: show/hide logs.
        :params extra_ctx: add extra ctx variables.
        :param train_fn: Contains all train logic. Useffull to override train process.
        """

        ctx = FitContextFactory.create(self, loss_fn, epochs, optimizer, extra_ctx, verbose)

        callback_manager = CallbackManager(ctx, callbacks)

        for epoch in range(epochs):
            callback_manager.on_epoch_start(epoch)

            train_loss = train_fn(ctx, data_loader)

            callback_manager.on_epoch_end(train_loss)

            if callback_manager.break_training():
                break

        return callback_manager.ctx
