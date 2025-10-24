import time
import threading
from typing import List
from observer import Subject, Observer
from message import Message

class NewsAgency(Subject):
    """
    Информационное агентство "Ulan-Ude news"
    Реализует паттерн Subject для уведомления наблюдателей о новых сообщениях
    """
    
    def __init__(self):
        """Инициализация агентства"""
        self._observers: List[Observer] = []
        self._messages: List[Message] = []
        self._running = False
        self._thread = None
    
    def attach(self, observer: Observer):
        """
        Добавить наблюдателя
        
        Args:
            observer (Observer): Наблюдатель для добавления
        """
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"Наблюдатель {observer.__class__.__name__} добавлен")
    
    def detach(self, observer: Observer):
        """
        Удалить наблюдателя
        
        Args:
            observer (Observer): Наблюдатель для удаления
        """
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"Наблюдатель {observer.__class__.__name__} удален")
    
    def notify(self):
        """Уведомить всех наблюдателей о последнем сообщении"""
        if self._messages:
            latest_message = self._messages[-1]
            for observer in self._observers:
                observer.update(latest_message)
    
    def add_message(self, message: Message):
        """
        Добавить новое сообщение и уведомить наблюдателей
        
        Args:
            message (Message): Новое сообщение
        """
        self._messages.append(message)
        print(f"Агентство получило новое сообщение: {message}")
        self.notify()
    
    def start_reading_from_file(self, filename: str, delay: int = 5):
        """
        Начать чтение сообщений из файла с заданной задержкой
        
        Args:
            filename (str): Имя файла с сообщениями
            delay (int): Задержка между чтениями в секундах (по умолчанию 5)
        """
        if self._running:
            print("Чтение уже запущено")
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._read_file_loop, args=(filename, delay))
        self._thread.daemon = True
        self._thread.start()
        print(f"Начато чтение файла {filename} с интервалом {delay} секунд")
    
    def stop_reading(self):
        """Остановить чтение файла"""
        self._running = False
        if self._thread:
            self._thread.join()
        print("Чтение файла остановлено")
    
    def _read_file_loop(self, filename: str, delay: int):
        """
        Цикл чтения файла с задержкой
        
        Args:
            filename (str): Имя файла
            delay (int): Задержка в секундах
        """
        processed_lines = 0
        
        while self._running:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    
                    # Обработать только новые строки
                    if len(lines) > processed_lines:
                        for i in range(processed_lines, len(lines)):
                            line = lines[i].strip()
                            if line:  # Пропустить пустые строки
                                try:
                                    message = Message.parse_from_line(line)
                                    self.add_message(message)
                                except ValueError as e:
                                    print(f"Ошибка парсинга строки '{line}': {e}")
                        
                        processed_lines = len(lines)
                
                # Задержка перед следующим чтением
                time.sleep(delay)
                
            except FileNotFoundError:
                print(f"Файл {filename} не найден. Ожидание...")
                time.sleep(delay)
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")
                time.sleep(delay)
    
    def get_messages(self) -> List[Message]:
        """Получить все сообщения"""
        return self._messages.copy()
    
    def get_observers_count(self) -> int:
        """Получить количество наблюдателей"""
        return len(self._observers)