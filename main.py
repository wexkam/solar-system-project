#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Демонстрация работы информационного агентства "Ulan-Ude news"
с использованием паттерна Observer
"""

import time
import signal
import sys
from news_agency import NewsAgency
from observers import InformPolis, ArigUs, CustomObserver
from message import MessageType

def signal_handler(sig, frame):
    """Обработчик сигнала для корректного завершения программы"""
    print('\n\nЗавершение работы программы...')
    sys.exit(0)

def main():
    """Главная функция демонстрации"""
    print("=" * 60)
    print("Информационное агентство 'Ulan-Ude news'")
    print("Демонстрация паттерна Observer")
    print("=" * 60)
    
    # Создание агентства
    agency = NewsAgency()
    
    # Создание наблюдателей
    print("\n1. Создание наблюдателей:")
    inform_polis = InformPolis()
    arig_us = ArigUs()
    custom_observer = CustomObserver("Радио Байкал", [MessageType.WEATHER])
    
    # Подписка наблюдателей
    print("\n2. Подписка наблюдателей на агентство:")
    agency.attach(inform_polis)
    agency.attach(arig_us)
    agency.attach(custom_observer)
    
    print(f"Количество подписчиков: {agency.get_observers_count()}")
    
    # Демонстрация добавления нового наблюдателя без изменения кода
    print("\n3. Демонстрация добавления нового наблюдателя:")
    new_observer = CustomObserver("Интернет-портал Бурятия", [MessageType.CITY_NEWS, MessageType.CURRENCY])
    agency.attach(new_observer)
    
    # Установка обработчика сигнала для корректного завершения
    signal.signal(signal.SIGINT, signal_handler)
    
    print("\n4. Начало чтения новостей из файла (каждые 5 секунд):")
    print("Нажмите Ctrl+C для завершения программы\n")
    
    # Запуск чтения файла
    agency.start_reading_from_file('news_data.txt', delay=5)
    
    try:
        # Демонстрация работы в течение 30 секунд
        time.sleep(30)
        
        print("\n\n5. Демонстрация удаления наблюдателя:")
        agency.detach(custom_observer)
        print("Радио Байкал отписался от новостей")
        
        # Продолжение работы еще 15 секунд
        time.sleep(15)
        
        print("\n\n6. Статистика:")
        print(f"Информ полис получил {inform_polis.get_received_count()} сообщений")
        print(f"Ариг Ус получил {arig_us.get_received_count()} сообщений")
        print(f"Интернет-портал Бурятия получил {new_observer.get_received_count()} сообщений")
        
        # Показать сообщения по типам для Информ полис
        weather_msgs = inform_polis.get_messages_by_type(MessageType.WEATHER)
        currency_msgs = inform_polis.get_messages_by_type(MessageType.CURRENCY)
        news_msgs = inform_polis.get_messages_by_type(MessageType.CITY_NEWS)
        
        print(f"\nИнформ полис получил:")
        print(f"  - Сообщений о погоде: {len(weather_msgs)}")
        print(f"  - Сообщений о валюте: {len(currency_msgs)}")
        print(f"  - Городских новостей: {len(news_msgs)}")
        
        # Показать интересующие сообщения для Ариг Ус
        interested_msgs = arig_us.get_interested_messages()
        print(f"\nАриг Ус заинтересовался {len(interested_msgs)} сообщениями из {arig_us.get_received_count()}")
        
    except KeyboardInterrupt:
        pass
    finally:
        # Остановка чтения файла
        agency.stop_reading()
        print("\nРабота агентства завершена.")

def demo_manual_messages():
    """Демонстрация ручного добавления сообщений"""
    print("\n" + "=" * 60)
    print("Демонстрация ручного добавления сообщений")
    print("=" * 60)
    
    agency = NewsAgency()
    inform_polis = InformPolis()
    arig_us = ArigUs()
    
    agency.attach(inform_polis)
    agency.attach(arig_us)
    
    # Создание тестовых сообщений
    from message import Message
    
    messages = [
        Message("Температура -10, снег", "2020-12-01", 1),
        Message("USD 75.5", "2020-12-01", 2),
        Message("В городе открылся новый музей", "2020-12-01", 3),
        Message("Завтра будет солнечно", "2020-12-02", 1),
    ]
    
    print("Отправка сообщений:")
    for msg in messages:
        agency.add_message(msg)
        time.sleep(1)  # Небольшая задержка для наглядности
    
    print(f"\nВсего отправлено: {len(messages)} сообщений")

if __name__ == "__main__":
    try:
        # Основная демонстрация
        main()
        
        # Дополнительная демонстрация ручного добавления
        demo_manual_messages()
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)