import time

from sklearn.utils import Bunch


class PartialResult(Bunch):
    def __init__(self, info, metrics, labels, partitions):
        if not isinstance(info, PartialResultInfo):
            raise RuntimeError('info is not instance of PartialResultInfo')
        if not isinstance(metrics, PartialResultMetrics):
            raise RuntimeError('metrics is not instance of PartialResultMetrics')
        super().__init__(
            info=info,
            metrics=metrics,
            labels=labels,
            partitions=partitions
        )


class PartialResultInfo(Bunch):
    def __init__(self, iteration, isLast, runIteration, elapsedTime, **kwargs):
        super().__init__(
            iteration=iteration,
            isLast=isLast,
            timestamp=time.time(),
            runIteration=runIteration,
            elapsedTime=round(elapsedTime, 8),
            **kwargs
        )


class PartialResultMetrics(Bunch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
