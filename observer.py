from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    """Абстрактный интерфейс наблюдателя"""
    
    @abstractmethod
    def update(self, message):
        """Метод для получения уведомлений от Subject"""
        pass

class Subject(ABC):
    """Абстрактный интерфейс субъекта (издателя)"""
    
    @abstractmethod
    def attach(self, observer: Observer):
        """Добавить наблюдателя"""
        pass
    
    @abstractmethod
    def detach(self, observer: Observer):
        """Удалить наблюдателя"""
        pass
    
    @abstractmethod
    def notify(self):
        """Уведомить всех наблюдателей"""
        pass