from abc import ABC, abstractmethod


class AbstractSaveStrategy(ABC):
    @abstractmethod
    def save(self, issues_):
        pass
