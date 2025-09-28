from abc import ABC, abstractmethod

class BaseAPI(ABC):

    @abstractmethod
    def get(self):
        pass
    