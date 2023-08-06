from pytorch_common.callbacks.output import OutputCallback


class OutputHook(OutputCallback):
    def __init__(self, hook_fn, plot_each_n_epochs=2):
        super().__init__(plot_each_n_epochs)
        self.hook_fn = hook_fn

    def on_show(self, ctx):
        self.hook_fn(ctx)