class MetricImproveMixin:
    def _init(self, last_metric_prefix, metric, mode='min'):
        """
        :param metric (str): Metric used to check model performance improving.
        :param mode (str): One of `min`, `max`. In `min` mode check that metric go down after each epoch.
        """
        self.__last_metric_prefix = last_metric_prefix
        self._metric_name = metric
        self._previous_metric_name = '{}_previous_{}'.format(self.__last_metric_prefix, self._metric_name)
        self._mode = mode

    def _update_last_metric(self, ctx):
        ctx[self._previous_metric_name] = ctx[self._metric_name]

    def _previous_metric(self, ctx):
        return ctx[self._previous_metric_name]

    def _metric(self, ctx):
        return ctx[self._metric_name]

    def _has_metric(self, ctx):
        return self._metric_name in ctx

    def _has_last_metric(self, ctx):
        return self._previous_metric_name in ctx

    def on_after_train(self, ctx):
        if self._has_metric(ctx):
            if self._has_last_metric(ctx):
                if self._did_improve_metric(ctx):
                    self._on_improve(ctx, self._mode)
                else:
                    self._on_not_improve(ctx)

            self._update_last_metric(ctx)

    def _did_improve_metric(self, ctx):
        return self._did_improve_min(ctx) or self._did_improve_max(ctx)

    def _did_improve_min(self, ctx):
        return self._mode == 'min' and ctx[self._metric_name] < self._previous_metric(ctx)

    def _did_improve_max(self, ctx):
        return self._mode == 'max' and ctx[self._metric_name] > self._previous_metric(ctx)

    def _on_improve(self, ctx, mode):
        pass

    def _on_not_improve(self, ctx):
        pass
