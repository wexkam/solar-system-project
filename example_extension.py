#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пример расширения системы новыми наблюдателями
Демонстрирует, как можно добавлять новых наблюдателей без изменения существующего кода
"""

from observer import Observer
from message import Message, MessageType
from news_agency import NewsAgency
from observers import InformPolis, ArigUs

class WeatherService(Observer):
    """
    Метеослужба - заинтересована только в информации о погоде
    Ведет детальную статистику по погодным условиям
    """
    
    def __init__(self):
        self.name = "Метеослужба Бурятии"
        self.weather_data = []
        self.temperature_readings = []
    
    def update(self, message: Message):
        """Обработка сообщений о погоде"""
        if message.message_type == MessageType.WEATHER:
            self.weather_data.append(message)
            
            # Попытка извлечь температуру из сообщения
            try:
                content = message.content.lower()
                if 'температура' in content:
                    # Простой парсинг температуры
                    parts = content.split()
                    for i, part in enumerate(parts):
                        if 'температура' in part and i + 1 < len(parts):
                            temp_str = parts[i + 1].replace(',', '').replace('+', '')
                            if temp_str.lstrip('-').isdigit():
                                self.temperature_readings.append(int(temp_str))
                                break
                elif content.startswith('-') or content.startswith('+'):
                    # Формат: "-15 1 20"
                    temp = int(content.split()[0])
                    self.temperature_readings.append(temp)
            except:
                pass
            
            print(f"{self.name} зафиксировал погодные данные: {message.content}")
        else:
            # Игнорируем сообщения не о погоде
            pass
    
    def get_average_temperature(self):
        """Получить среднюю температуру"""
        if not self.temperature_readings:
            return None
        return sum(self.temperature_readings) / len(self.temperature_readings)
    
    def get_weather_report(self):
        """Получить сводку по погоде"""
        return {
            'total_reports': len(self.weather_data),
            'temperature_readings': len(self.temperature_readings),
            'average_temp': self.get_average_temperature(),
            'min_temp': min(self.temperature_readings) if self.temperature_readings else None,
            'max_temp': max(self.temperature_readings) if self.temperature_readings else None
        }

class CurrencyExchange(Observer):
    """
    Обменный пункт - отслеживает курсы валют
    Ведет историю изменения курсов
    """
    
    def __init__(self):
        self.name = "Обменный пункт 'Байкал'"
        self.currency_rates = {}
        self.rate_history = []
    
    def update(self, message: Message):
        """Обработка сообщений о валютах"""
        if message.message_type == MessageType.CURRENCY:
            self.rate_history.append(message)
            
            # Парсинг курса валют
            try:
                content = message.content.lower()
                for currency in ['dollar', 'euro', 'yuan', 'bitcoin']:
                    if currency in content:
                        parts = content.split()
                        for i, part in enumerate(parts):
                            if currency in part and i + 1 < len(parts):
                                rate = float(parts[i + 1])
                                self.currency_rates[currency] = {
                                    'rate': rate,
                                    'date': message.date
                                }
                                break
            except:
                pass
            
            print(f"{self.name} обновил курсы валют: {message.content}")
    
    def get_current_rates(self):
        """Получить текущие курсы"""
        return self.currency_rates
    
    def get_currency_trend(self, currency):
        """Получить тренд по валюте"""
        rates = []
        for msg in self.rate_history:
            if currency.lower() in msg.content.lower():
                try:
                    parts = msg.content.lower().split()
                    for i, part in enumerate(parts):
                        if currency.lower() in part and i + 1 < len(parts):
                            rates.append(float(parts[i + 1]))
                            break
                except:
                    pass
        return rates

class NewsAggregator(Observer):
    """
    Новостной агрегатор - собирает все новости для веб-сайта
    Категоризирует новости по типам
    """
    
    def __init__(self, website_name):
        self.name = f"Новостной сайт '{website_name}'"
        self.all_news = []
        self.categories = {
            MessageType.WEATHER: [],
            MessageType.CURRENCY: [],
            MessageType.CITY_NEWS: []
        }
    
    def update(self, message: Message):
        """Сохранение всех новостей"""
        self.all_news.append(message)
        self.categories[message.message_type].append(message)
        
        category_names = {
            MessageType.WEATHER: "Погода",
            MessageType.CURRENCY: "Экономика", 
            MessageType.CITY_NEWS: "Городские новости"
        }
        
        category = category_names.get(message.message_type, "Разное")
        print(f"{self.name} опубликовал в разделе '{category}': {message.content}")
    
    def get_latest_news(self, count=5):
        """Получить последние новости"""
        return self.all_news[-count:] if len(self.all_news) >= count else self.all_news
    
    def get_news_by_category(self, message_type):
        """Получить новости по категории"""
        return self.categories.get(message_type, [])
    
    def get_statistics(self):
        """Получить статистику по новостям"""
        return {
            'total': len(self.all_news),
            'weather': len(self.categories[MessageType.WEATHER]),
            'currency': len(self.categories[MessageType.CURRENCY]),
            'city_news': len(self.categories[MessageType.CITY_NEWS])
        }

def demonstration():
    """Демонстрация расширения системы новыми наблюдателями"""
    print("=" * 70)
    print("Демонстрация расширения системы новыми наблюдателями")
    print("=" * 70)
    
    # Создание агентства
    agency = NewsAgency()
    
    # Существующие наблюдатели
    inform_polis = InformPolis()
    arig_us = ArigUs()
    
    # Новые наблюдатели (без изменения существующего кода!)
    weather_service = WeatherService()
    currency_exchange = CurrencyExchange()
    news_site = NewsAggregator("Улан-Удэ Онлайн")
    
    # Подписка всех наблюдателей
    observers = [inform_polis, arig_us, weather_service, currency_exchange, news_site]
    
    print("Подписка наблюдателей:")
    for observer in observers:
        agency.attach(observer)
    
    print(f"\nВсего подписчиков: {agency.get_observers_count()}")
    
    # Тестовые сообщения
    test_messages = [
        Message("Температура -8, ветер 15 м/с", "2020-12-10", 1),
        Message("dollar 76.2", "2020-12-10", 2),
        Message("В Улан-Удэ открылся новый театр", "2020-12-10", 3),
        Message("Завтра температура +2, солнечно", "2020-12-11", 1),
        Message("euro 92.1", "2020-12-11", 2),
        Message("bitcoin 48000", "2020-12-11", 2),
    ]
    
    print("\n" + "=" * 50)
    print("Отправка тестовых сообщений:")
    print("=" * 50)
    
    for msg in test_messages:
        print(f"\n>>> Отправляется: {msg}")
        agency.add_message(msg)
        print("-" * 50)
    
    # Статистика по специализированным наблюдателям
    print("\n" + "=" * 50)
    print("Статистика специализированных наблюдателей:")
    print("=" * 50)
    
    # Метеослужба
    weather_report = weather_service.get_weather_report()
    print(f"\n{weather_service.name}:")
    print(f"  Погодных сводок: {weather_report['total_reports']}")
    print(f"  Температурных показаний: {weather_report['temperature_readings']}")
    if weather_report['average_temp']:
        print(f"  Средняя температура: {weather_report['average_temp']:.1f}°C")
        print(f"  Мин/Макс температура: {weather_report['min_temp']}°C / {weather_report['max_temp']}°C")
    
    # Обменный пункт
    current_rates = currency_exchange.get_current_rates()
    print(f"\n{currency_exchange.name}:")
    print(f"  Отслеживаемых валют: {len(current_rates)}")
    for currency, data in current_rates.items():
        print(f"  {currency.upper()}: {data['rate']} (на {data['date']})")
    
    # Новостной сайт
    site_stats = news_site.get_statistics()
    print(f"\n{news_site.name}:")
    print(f"  Всего новостей: {site_stats['total']}")
    print(f"  Погода: {site_stats['weather']}")
    print(f"  Экономика: {site_stats['currency']}")
    print(f"  Городские новости: {site_stats['city_news']}")
    
    print("\n" + "=" * 70)
    print("Демонстрация завершена!")
    print("Система легко расширяется новыми наблюдателями без изменения кода!")
    print("=" * 70)

if __name__ == "__main__":
    demonstration()