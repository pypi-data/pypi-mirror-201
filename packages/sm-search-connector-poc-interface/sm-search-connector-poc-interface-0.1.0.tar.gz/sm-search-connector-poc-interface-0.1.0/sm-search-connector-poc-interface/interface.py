from abc import ABC, abstractmethod


class ISearchConnector(ABC):
    """
    A search interface for serach conenctor
    """

    @abstractmethod
    def search(self, str: request) -> str:
        pass
