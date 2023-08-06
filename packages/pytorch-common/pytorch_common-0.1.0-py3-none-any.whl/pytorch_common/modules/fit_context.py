from bunch import Bunch
from pytorch_common.util import Stopwatch


class FitContextFactory:
    @staticmethod
    def create(model, loss_fn=None, epochs=0, optimizer=None, extra_ctx={}, verbose=1):
        """Creates a default context used to fit/train a model. Is important to note that this is an initial context.
        Depending of callbacks used then fit a model it context could have extra variables. This extra variables are use by callbacks.

        Args:
            model: model instance.
            loss_fn: Loss function.
            epochs int: Time to train a model over complete train set.
            optimizer: Optimizer isntace used to fit the model.
            extra_ctx (dict, optional): Extra properties appended when invoke model.fit(extra_ctx={...}]). Defaults to {}.
            verbose (int, optional): Show logs. Defaults to 1.

        Returns:
            a context dictionary.
        """
        ctx = Bunch({
            'verbose': verbose,
            'epochs': epochs,
            'optimizer': optimizer,
            'loss_fn': loss_fn,
            'device': model.device,
            'model': model,
            'stopwatch': Stopwatch()
        })

        for (k, v) in extra_ctx.items():
            ctx[k] = v

        return ctx
