#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрый старт для демонстрации системы Observer
Информационного агентства "Ulan-Ude news"
"""

import time
from news_agency import NewsAgency
from observers import InformPolis, ArigUs, CustomObserver
from message import Message, MessageType

def quick_demo():
    """Быстрая демонстрация основных возможностей"""
    print("🏢 Информационное агентство 'Ulan-Ude news'")
    print("📰 Быстрая демонстрация системы Observer\n")
    
    # 1. Создание агентства
    print("1️⃣ Создание агентства...")
    agency = NewsAgency()
    
    # 2. Создание и подписка наблюдателей
    print("2️⃣ Подписка наблюдателей...")
    inform_polis = InformPolis()
    arig_us = ArigUs()
    radio = CustomObserver("Радио Байкал", [MessageType.WEATHER])
    
    agency.attach(inform_polis)
    agency.attach(arig_us)
    agency.attach(radio)
    
    # 3. Отправка тестовых сообщений
    print("3️⃣ Отправка тестовых сообщений...\n")
    
    messages = [
        Message("☀️ Сегодня солнечно, +5°C", "2024-10-24", 1),
        Message("💰 USD курс: 95.5 рублей", "2024-10-24", 2),
        Message("🏛️ Открытие нового музея в центре города", "2024-10-24", 3),
    ]
    
    for i, msg in enumerate(messages, 1):
        print(f"📤 Сообщение {i}:")
        agency.add_message(msg)
        print()
        time.sleep(1)
    
    # 4. Демонстрация удаления наблюдателя
    print("4️⃣ Удаление наблюдателя...")
    agency.detach(radio)
    
    agency.add_message(Message("🌨️ Завтра ожидается снег", "2024-10-25", 1))
    
    # 5. Статистика
    print("\n5️⃣ Статистика:")
    print(f"📊 Информ полис: {inform_polis.get_received_count()} сообщений")
    print(f"📺 Ариг Ус: {arig_us.get_received_count()} сообщений")
    print(f"📻 Радио Байкал: {radio.get_received_count()} сообщений")
    
    print("\n✅ Демонстрация завершена!")

def file_reading_demo():
    """Демонстрация чтения из файла"""
    print("\n" + "="*50)
    print("📁 Демонстрация чтения из файла")
    print("="*50)
    
    agency = NewsAgency()
    inform_polis = InformPolis()
    arig_us = ArigUs()
    
    agency.attach(inform_polis)
    agency.attach(arig_us)
    
    print("🔄 Запуск чтения файла news_data.txt...")
    print("⏰ Интервал: 2 секунды (для демонстрации)")
    print("⏱️ Длительность: 10 секунд\n")
    
    agency.start_reading_from_file('news_data.txt', delay=2)
    
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        agency.stop_reading()
    
    print(f"\n📈 Результаты чтения:")
    print(f"   Информ полис: {inform_polis.get_received_count()} сообщений")
    print(f"   Ариг Ус: {arig_us.get_received_count()} сообщений")

if __name__ == "__main__":
    try:
        # Основная демонстрация
        quick_demo()
        
        # Демонстрация чтения файла
        file_reading_demo()
        
        print("\n🎉 Все демонстрации завершены успешно!")
        print("\n💡 Для расширенной демонстрации запустите:")
        print("   python3 example_extension.py")
        print("\n📖 Для полной демонстрации запустите:")
        print("   python3 main.py")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")