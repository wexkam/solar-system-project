from datetime import datetime
from enum import Enum

class MessageType(Enum):
    """Типы сообщений"""
    WEATHER = 1      # Информация о погоде
    CURRENCY = 2     # Курс валют
    CITY_NEWS = 3    # Новости города

class Message:
    """Класс для представления сообщения информационного агентства"""
    
    def __init__(self, content: str, date: str, message_type: int):
        """
        Инициализация сообщения
        
        Args:
            content (str): Текст сообщения
            date (str): Дата в формате YYYY-mm-dd
            message_type (int): Тип сообщения (1-погода, 2-валюта, 3-новости)
        """
        self.content = content.strip()
        self.date = date.strip()
        self.message_type = MessageType(message_type)
    
    def __str__(self):
        """Строковое представление сообщения"""
        return f"{self.content}; {self.date}; {self.message_type.value}"
    
    def get_type_name(self):
        """Получить название типа сообщения"""
        type_names = {
            MessageType.WEATHER: "погода",
            MessageType.CURRENCY: "курс валют", 
            MessageType.CITY_NEWS: "новости города"
        }
        return type_names.get(self.message_type, "неизвестный тип")
    
    @classmethod
    def parse_from_line(cls, line: str):
        """
        Создать сообщение из строки файла
        
        Args:
            line (str): Строка в формате "content; date; type"
            
        Returns:
            Message: Объект сообщения
        """
        parts = line.strip().split(';')
        if len(parts) != 3:
            raise ValueError(f"Неверный формат строки: {line}")
        
        content = parts[0].strip()
        date = parts[1].strip()
        message_type = int(parts[2].strip())
        
        return cls(content, date, message_type)