import time
from abc import ABC, abstractmethod

import numpy as np
from sklearn.utils._param_validation import (Integral, Interval, Real,
                                             StrOptions, validate_params)


class ProgressiveEnsembleClustering(ABC):
    """
    The ProgressiveClusteringEnsemble interface declares the hasNextIteration and  executeNextIteration methods.
    Each inherited class must implement them.
    """

    @validate_params(
        {
            'data': ['array-like', 'sparse matrix'],
            'n_clusters': [Interval(Integral, 1, None, closed='left')],
            'n_runs': [Interval(Integral, 1, None, closed='left')],
            'init': [StrOptions({'k-means++', 'random'})]
        }
    )
    def __init__(self, data, n_clusters=2, n_runs=4, random_state=None):
        self.data = data

        self.n = data.shape[0]  # number of data entries
        self.d = data.shape[1]  # number of dimensions
        self.k = n_clusters  # number of clusters
        self.r = n_runs # number of runs

        self._seeds = np.random.default_rng(random_state).integers(0, 4294967295, size=self.r)

        self._runs = None
        self._runInfo = [None] * self.r
        self._runMetrics = [None] * self.r
        self._partitions = np.empty((self.n, self.r), dtype=np.uint8)
        self._iteration = 0
        self._completed = False

    @abstractmethod
    def initializeRuns(self, seeds):
        pass

    @abstractmethod
    def generatePartialResult(self, iteration, isLast, runInfo, runMetrics, partitions, t0):
        pass

    def hasNextIteration(self) -> bool:
        return not self._completed

    def executeNextIteration(self):
        if self._completed:
            raise RuntimeError('no next iteration to execute')

        if self._runs is None:
            self._runs = self.initializeRuns(self._seeds)

        self._iteration += 1
        t0 = time.time()
        for i in range(self.r):
            if self._runs[i].hasNextIteration():
                r = self._runs[i].executeNextIteration()
                self._runInfo[i] = r.info
                self._runMetrics[i] = r.metrics
                self._partitions[:, i] = r.labels

        self._completed = np.all([not self._runs[i].hasNextIteration() for i in range(self.r)])
        partialResult = self.generatePartialResult(self._iteration, self._completed, self._runInfo, self._runMetrics, self._partitions, t0)
        return partialResult