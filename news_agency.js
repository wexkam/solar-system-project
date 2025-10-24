// Интерфейс Observer (Наблюдатель)
class Observer {
    update(message, date, type) {
        throw new Error("Метод update() должен быть реализован");
    }
}

// Конкретные наблюдатели
class InformPolis extends Observer {
    constructor() {
        super();
        this.name = "Информ полис";
    }

    update(message, date, type) {
        const typeNames = {
            1: "Погода",
            2: "Курс валют",
            3: "Новости города"
        };
        console.log(`${this.name} получил информацию: ${message}, ${date}, ${typeNames[type] || "Тип " + type}`);
    }
}

class ArigUs extends Observer {
    constructor() {
        super();
        this.name = "Ариг Ус";
    }

    update(message, date, type) {
        const typeNames = {
            1: "Погода",
            2: "Курс валют",
            3: "Новости города"
        };
        console.log(`${this.name} получил информацию: ${message}, ${date}, ${typeNames[type] || "Тип " + type}`);
    }
}

// Subject (Субъект) - Информационное агентство
class NewsAgency {
    constructor() {
        this.observers = [];
        this.name = "Ulan-Ude news";
    }

    // Добавить наблюдателя
    addObserver(observer) {
        if (!this.observers.includes(observer)) {
            this.observers.push(observer);
            console.log(`Наблюдатель ${observer.name} подписан на ${this.name}`);
            return true;
        }
        console.log(`Наблюдатель ${observer.name} уже подписан`);
        return false;
    }

    // Удалить наблюдателя
    removeObserver(observer) {
        const index = this.observers.indexOf(observer);
        if (index > -1) {
            this.observers.splice(index, 1);
            console.log(`Наблюдатель ${observer.name} отписан от ${this.name}`);
            return true;
        }
        console.log(`Наблюдатель ${observer.name} не найден`);
        return false;
    }

    // Оповестить всех наблюдателей
    notifyObservers(message, date, type) {
        console.log(`\n--- ${this.name} рассылает информацию ---`);
        this.observers.forEach(observer => {
            observer.update(message, date, type);
        });
    }

    // Парсинг строки сообщения
    parseMessage(line) {
        // Формат: сообщение; дата; тип
        const parts = line.split(';').map(part => part.trim());
        
        if (parts.length !== 3) {
            console.error(`Неверный формат строки: ${line}`);
            return null;
        }

        const message = parts[0];
        const date = parts[1];
        const type = parseInt(parts[2]);

        if (isNaN(type)) {
            console.error(`Неверный тип сообщения: ${parts[2]}`);
            return null;
        }

        return { message, date, type };
    }

    // Чтение данных из файла с задержкой
    async readFromFile(fileContent) {
        const lines = fileContent.split('\n').filter(line => line.trim() !== '');
        
        console.log(`${this.name} начинает обработку ${lines.length} сообщений...\n`);

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const parsed = this.parseMessage(line);
            
            if (parsed) {
                this.notifyObservers(parsed.message, parsed.date, parsed.type);
            }

            // Задержка 5 секунд перед следующим сообщением
            if (i < lines.length - 1) {
                console.log(`\nОжидание 5 секунд перед следующим сообщением...\n`);
                await this.delay(5000);
            }
        }

        console.log(`\n${this.name} завершил обработку всех сообщений.`);
    }

    // Вспомогательная функция для задержки
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Экспорт для использования в HTML
if (typeof window !== 'undefined') {
    window.NewsAgency = NewsAgency;
    window.InformPolis = InformPolis;
    window.ArigUs = ArigUs;
}
