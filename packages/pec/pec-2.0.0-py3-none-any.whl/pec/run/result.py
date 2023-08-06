import time

from sklearn.utils import Bunch


class RunPartialResult(Bunch):
    def __init__(self, info, metrics, centroids, labels):
        if not isinstance(info, RunPartialResultInfo):
            raise RuntimeError('info is not instance of RunPartialResultInfo')
        if not isinstance(metrics, RunPartialResultMetrics):
            raise RuntimeError('metrics is not instance of RunPartialResultMetrics')
        super().__init__(
            info=info,
            metrics=metrics,
            centroids=centroids,
            labels=labels
        )


class RunPartialResultInfo(Bunch):
    def __init__(self, iteration, isLast):
        super().__init__(
            iteration=iteration,
            isLast=isLast,
            timestamp=time.time()
        )


class RunPartialResultMetrics(Bunch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
