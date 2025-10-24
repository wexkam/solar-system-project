// Базовый интерфейс Observer
class Observer {
    update(newsMessage) {
        throw new Error("Method 'update' must be implemented");
    }
}

// Класс для представления сообщения новостного агентства
class NewsMessage {
    constructor(message, date, type) {
        this.message = message;
        this.date = date;
        this.type = type;
    }

    getTypeDescription() {
        switch(this.type) {
            case 1: return "информация о погоде";
            case 2: return "курс валют";
            case 3: return "новости города";
            default: return "неизвестный тип";
        }
    }

    toString() {
        return `${this.message}, ${this.date}, ${this.type}`;
    }
}

// Класс новостного агентства (Subject)
class NewsAgency {
    constructor() {
        this.observers = [];
    }

    // Добавление наблюдателя
    addObserver(observer) {
        if (!this.observers.includes(observer)) {
            this.observers.push(observer);
            console.log(`Наблюдатель ${observer.name} добавлен`);
        }
    }

    // Удаление наблюдателя
    removeObserver(observer) {
        const index = this.observers.indexOf(observer);
        if (index > -1) {
            this.observers.splice(index, 1);
            console.log(`Наблюдатель ${observer.name} удален`);
        }
    }

    // Уведомление всех наблюдателей
    notifyObservers(newsMessage) {
        this.observers.forEach(observer => {
            observer.update(newsMessage);
        });
    }

    // Публикация новости
    publishNews(newsMessage) {
        console.log(`\n=== Агентство "Ulan-Ude news" публикует новость ===`);
        console.log(`Сообщение: ${newsMessage.message}`);
        console.log(`Дата: ${newsMessage.date}`);
        console.log(`Тип: ${newsMessage.getTypeDescription()}`);
        console.log("===============================================\n");
        
        this.notifyObservers(newsMessage);
    }
}

// Конкретные наблюдатели
class InformPolisObserver extends Observer {
    constructor() {
        super();
        this.name = "Информ полис";
    }

    update(newsMessage) {
        console.log(`${this.name} получил информацию: ${newsMessage.toString()}`);
    }
}

class ArigUsObserver extends Observer {
    constructor() {
        super();
        this.name = "Ариг Ус";
    }

    update(newsMessage) {
        console.log(`${this.name} получил информацию: ${newsMessage.toString()}`);
    }
}

// Класс для чтения данных из файла
class NewsReader {
    constructor(newsAgency) {
        this.newsAgency = newsAgency;
        this.isRunning = false;
    }

    // Парсинг строки сообщения
    parseNewsLine(line) {
        const parts = line.split(';').map(part => part.trim());
        if (parts.length !== 3) {
            throw new Error(`Неверный формат строки: ${line}`);
        }

        const [message, date, type] = parts;
        const messageType = parseInt(type);
        
        if (isNaN(messageType) || messageType < 1 || messageType > 3) {
            throw new Error(`Неверный тип сообщения: ${type}`);
        }

        return new NewsMessage(message, date, messageType);
    }

    // Чтение и обработка файла
    async readNewsFile(filename) {
        try {
            const response = await fetch(filename);
            if (!response.ok) {
                throw new Error(`Ошибка чтения файла: ${response.status}`);
            }
            
            const text = await response.text();
            const lines = text.split('\n').filter(line => line.trim() !== '');
            
            console.log(`Найдено ${lines.length} сообщений в файле ${filename}`);
            
            for (let i = 0; i < lines.length; i++) {
                if (!this.isRunning) break;
                
                try {
                    const newsMessage = this.parseNewsLine(lines[i]);
                    this.newsAgency.publishNews(newsMessage);
                } catch (error) {
                    console.error(`Ошибка обработки строки ${i + 1}: ${error.message}`);
                }
                
                // Задержка 5 секунд между сообщениями
                if (i < lines.length - 1) {
                    console.log("Ожидание 5 секунд до следующего сообщения...");
                    await this.delay(5000);
                }
            }
            
            console.log("Все сообщения обработаны");
        } catch (error) {
            console.error(`Ошибка чтения файла: ${error.message}`);
        }
    }

    // Запуск чтения с задержкой
    async startReading(filename) {
        this.isRunning = true;
        console.log(`Начинаем чтение файла ${filename}...`);
        await this.readNewsFile(filename);
    }

    // Остановка чтения
    stopReading() {
        this.isRunning = false;
        console.log("Чтение остановлено");
    }

    // Утилита для задержки
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Экспорт классов для использования в HTML
window.Observer = Observer;
window.NewsMessage = NewsMessage;
window.NewsAgency = NewsAgency;
window.InformPolisObserver = InformPolisObserver;
window.ArigUsObserver = ArigUsObserver;
window.NewsReader = NewsReader;