from abc import ABC, abstractmethod

from .result import RunPartialResult


class ProgressiveClusteringRun(ABC):
    """
    The ProgressiveClusteringRun interface declares the hasNextIteration and  executeNextIteration methods.
    Each inherited class must implement them.
    """

    @abstractmethod
    def hasNextIteration(self) -> bool:
        pass

    @abstractmethod
    def executeNextIteration(self) -> RunPartialResult:
        pass
