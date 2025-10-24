from observer import Observer
from message import Message, MessageType

class InformPolis(Observer):
    """
    Газета "Информ полис" - наблюдатель за новостями агентства
    """
    
    def __init__(self):
        self.name = "Информ полис"
        self.received_messages = []
    
    def update(self, message: Message):
        """
        Получить уведомление о новом сообщении
        
        Args:
            message (Message): Новое сообщение от агентства
        """
        self.received_messages.append(message)
        print(f"{self.name} получил информацию: {message.content}, {message.date}, {message.message_type.value}")
    
    def get_received_count(self) -> int:
        """Получить количество полученных сообщений"""
        return len(self.received_messages)
    
    def get_messages_by_type(self, message_type: MessageType) -> list:
        """Получить сообщения определенного типа"""
        return [msg for msg in self.received_messages if msg.message_type == message_type]

class ArigUs(Observer):
    """
    Телеканал "Ариг Ус" - наблюдатель за новостями агентства
    """
    
    def __init__(self):
        self.name = "Ариг Ус"
        self.received_messages = []
        self.interested_types = [MessageType.WEATHER, MessageType.CITY_NEWS]  # Интересуется только погодой и новостями
    
    def update(self, message: Message):
        """
        Получить уведомление о новом сообщении
        Телеканал заинтересован только в определенных типах новостей
        
        Args:
            message (Message): Новое сообщение от агентства
        """
        self.received_messages.append(message)
        
        if message.message_type in self.interested_types:
            print(f"{self.name} получил информацию: {message.content}, {message.date}, {message.message_type.value}")
        else:
            print(f"{self.name} получил информацию о {message.get_type_name()}, но не заинтересован в этом типе новостей")
    
    def get_received_count(self) -> int:
        """Получить количество полученных сообщений"""
        return len(self.received_messages)
    
    def get_interested_messages(self) -> list:
        """Получить только интересующие сообщения"""
        return [msg for msg in self.received_messages if msg.message_type in self.interested_types]
    
    def set_interested_types(self, types: list):
        """
        Установить типы сообщений, которые интересуют телеканал
        
        Args:
            types (list): Список типов сообщений MessageType
        """
        self.interested_types = types
        print(f"{self.name} теперь интересуется типами: {[t.name for t in types]}")

class CustomObserver(Observer):
    """
    Пользовательский наблюдатель - демонстрирует возможность добавления новых наблюдателей
    без изменения существующего кода
    """
    
    def __init__(self, name: str, filter_types: list = None):
        """
        Инициализация пользовательского наблюдателя
        
        Args:
            name (str): Имя наблюдателя
            filter_types (list): Список типов сообщений для фильтрации (опционально)
        """
        self.name = name
        self.filter_types = filter_types or []
        self.received_messages = []
    
    def update(self, message: Message):
        """
        Получить уведомление о новом сообщении
        
        Args:
            message (Message): Новое сообщение от агентства
        """
        self.received_messages.append(message)
        
        if not self.filter_types or message.message_type in self.filter_types:
            print(f"{self.name} получил информацию: {message.content}, {message.date}, {message.message_type.value}")
        else:
            print(f"{self.name} получил сообщение, но оно не соответствует фильтру")
    
    def get_received_count(self) -> int:
        """Получить количество полученных сообщений"""
        return len(self.received_messages)