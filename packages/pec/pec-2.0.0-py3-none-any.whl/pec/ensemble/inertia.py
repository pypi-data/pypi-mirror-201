import time

import numpy as np
from sklearn.utils._param_validation import (Integral, Interval, Real,
                                             StrOptions, validate_params)

from ..run import ProgressiveKMeansRun
from .ensemble import ProgressiveEnsembleClustering
from .result import PartialResult, PartialResultInfo, PartialResultMetrics


class _InertiaBasedPEC(ProgressiveEnsembleClustering):
    @validate_params(
        {
            'data': ['array-like', 'sparse matrix'],
            'n_clusters': [Interval(Integral, 1, None, closed='left')],
            'max_iter': [Interval(Integral, 1, None, closed='left')],
            'tol': [Interval(Real, 0, None, closed='left')],
            'random_state': ['random_state'],
            'init': [StrOptions({'k-means++', 'random'})]
        }
    )
    def __init__(self, data, n_clusters=2, n_runs=4, max_iter=300, tol=1e-4, random_state=None):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs, random_state=random_state)
        self.max_iter = max_iter
        self.tol = tol

    def generatePartialResult(self, iteration, isLast, runInfo, runMetrics, partitions, t0):
        runIteration = [r.iteration for r in runInfo]
        bestRun = np.argmin([m.inertia for m in runMetrics])
        bestInertia = runMetrics[bestRun].inertia
        bestLabels = partitions[:, bestRun]

        elapsedTime = time.time() - t0
        info = PartialResultInfo(iteration, isLast, runIteration, elapsedTime, bestRun=bestRun)
        metrics = PartialResultMetrics(inertia=bestInertia)
        return PartialResult(info, metrics, bestLabels, partitions)


class IPECK(_InertiaBasedPEC):
    def __init__(self, data, n_clusters=2, n_runs=4, max_iter=300, tol=1e-4, random_state=None):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs, max_iter=max_iter, tol=tol,
                         random_state=random_state)

    def initializeRuns(self, seeds):
        runs = []
        for s in seeds:
            runs.append(
                ProgressiveKMeansRun(self.data, n_clusters=self.k, random_state=s, max_iter=self.max_iter,
                                     tol=self.tol, init='random'))
        return runs


class IPECKPP(_InertiaBasedPEC):
    def __init__(self, data, n_clusters=2, n_runs=4, max_iter=300, tol=1e-4, random_state=None):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs, max_iter=max_iter, tol=tol,
                         random_state=random_state)

    def initializeRuns(self, seeds):
        runs = []
        for s in seeds:
            runs.append(
                ProgressiveKMeansRun(self.data, n_clusters=self.k, random_state=s, max_iter=self.max_iter, tol=self.tol,
                                     init='k-means++'))
        return runs
