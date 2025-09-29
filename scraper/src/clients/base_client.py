from abc import ABC, abstractmethod

class BaseAPI(ABC):

    @abstractmethod
    def get(self):
        pass
    
class BaseClient(ABC):

    @abstractmethod
    def update_products(self):
        pass