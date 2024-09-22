import json
import os
from datetime import datetime

# Файл для хранения событий
FILE_NAME = 'events.json'

class Event:
    # Конструктор класса события
    def __init__(self, event_id, title, importance, date, completed=False):
        self.id = event_id           # ID события
        self.title = title           # Название события
        self.importance = importance # Важность события
        self.date = date             # Дата события (в формате 'YYYY-MM-DD')
        self.completed = completed   # Статус выполнения (по умолчанию False)

    # Преобразование объекта Event в словарь для хранения в JSON
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'importance': self.importance,
            'date': self.date,
            'completed': self.completed
        }

    # Статический метод для создания объекта Event из словаря
    @staticmethod
    def from_dict(data):
        return Event(
            data['id'],
            data['title'],
            data['importance'],
            data['date'],
            data.get('completed', False)  # Если ключа 'completed' нет, значение по умолчанию False
        )


class Diary:
    # Конструктор класса для управления событиями
    def __init__(self):
        self.events = []  # Список всех событий
        self.load_events()  # Загрузка событий из файла

    # Метод загрузки событий из файла JSON
    def load_events(self):
        if os.path.exists(FILE_NAME):  # Проверяем наличие файла
            with open(FILE_NAME, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Чтение данных из файла
                self.events = [Event.from_dict(event) for event in data]  # Преобразуем данные в объекты Event
        else:
            self.events = []  # Если файл не найден, список событий пуст

    # Метод сохранения всех событий в файл JSON
    def save_events(self):
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump([event.to_dict() for event in self.events], f, ensure_ascii=False, indent=4)  # Сохранение в JSON

    # Метод для добавления нового события
    def add_event(self, title, importance, date):
        event_id = self._generate_id()  # Генерация уникального ID
        new_event = Event(event_id, title, importance, date)  # Создание нового события
        self.events.append(new_event)  # Добавление события в список
        self.save_events()  # Сохранение изменений в файл
        print("Событие добавлено успешно.")

    # Генерация уникального ID для события
    def _generate_id(self):
        if not self.events:
            return 1  # Если список пуст, начинаем с ID 1
        else:
            return max(event.id for event in self.events) + 1  # Возвращаем следующий ID

    # Метод для редактирования существующего события
    def edit_event(self, event_id, title=None, importance=None, date=None):
        event = self.get_event_by_id(event_id)  # Получение события по ID
        if event:
            if title:
                event.title = title  # Изменение названия
            if importance:
                event.importance = importance  # Изменение важности
            if date:
                event.date = date  # Изменение даты
            self.save_events()  # Сохранение изменений
            print("Событие обновлено успешно.")
        else:
            print("Событие не найдено.")

    # Метод для удаления события
    def delete_event(self, event_id):
        event = self.get_event_by_id(event_id)  # Получение события по ID
        if event:
            self.events.remove(event)  # Удаление события из списка
            self.save_events()  # Сохранение изменений
            print("Событие удалено успешно.")
        else:
            print("Событие не найдено.")

    # Метод для отметки события как выполненного
    def mark_completed(self, event_id):
        event = self.get_event_by_id(event_id)  # Получение события по ID
        if event:
            event.completed = True  # Помечаем событие как выполненное
            self.save_events()  # Сохранение изменений
            print("Событие отмечено как выполненное.")
        else:
            print("Событие не найдено.")

    # Метод для сортировки событий по дате
    def sort_events_by_date(self):
        self.events.sort(key=lambda event: event.date)  # Сортировка по дате
        self.save_events()  # Сохранение изменений
        print("События отсортированы по дате.")

    # Метод для получения события по его ID
    def get_event_by_id(self, event_id):
        for event in self.events:
            if event.id == event_id:
                return event
        return None

    # Метод для отображения всех событий
    def display_events(self):
        if not self.events:
            print("Событий нет.")  # Если список событий пуст
            return
        print("\nСписок событий:")
        # Заголовки столбцов с выравниванием
        print("{:<5} {:<30} {:<10} {:<12} {:<12}".format("ID", "Название", "Важность", "Дата", "Статус"))
        print("-" * 70)
        for event in self.events:
            status = "Выполнено" if event.completed else "Не выполнено"  # Статус события
            # Форматированный вывод каждого события
            print("{:<5} {:<30} {:<10} {:<12} {:<12}".format(
                event.id, event.title[:30], event.importance, event.date, status))
        print()


# Функция для запроса даты с проверкой корректности формата
def input_date(prompt):
    while True:
        date_str = input(prompt)  # Запрос даты от пользователя
        try:
            datetime.strptime(date_str, '%Y-%m-%d')  # Проверка формата даты
            return date_str
        except ValueError:
            print("Неверный формат даты. Используйте YYYY-MM-DD.")  # Сообщение об ошибке

# Главная функция для работы с ежедневником
def main():
    diary = Diary()  # Создание экземпляра дневника

    while True:
        # Меню для выбора действия
        print("\n=== Ежедневник ===")
        print("1. Показать все события")
        print("2. Добавить событие")
        print("3. Редактировать событие")
        print("4. Удалить событие")
        print("5. Отметить событие как выполненное")
        print("6. Отсортировать события по дате")
        print("0. Выход")

        choice = input("Выберите действие: ")  # Запрос действия от пользователя

        if choice == '1':
            diary.display_events()  # Показать все события
        elif choice == '2':
            # Добавление нового события
            title = input("Введите название события: ")
            importance = input("Введите важность (Высокая/Средняя/Низкая): ")
            date = input_date("Введите дату события (YYYY-MM-DD): ")
            diary.add_event(title, importance, date)
        elif choice == '3':
            # Редактирование события
            try:
                event_id = int(input("Введите ID события для редактирования: "))
                event = diary.get_event_by_id(event_id)
                if event:
                    print("Оставьте поле пустым, чтобы не изменять.")
                    new_title = input(f"Новое название ({event.title}): ") or event.title
                    new_importance = input(f"Новая важность ({event.importance}): ") or event.importance
                    new_date = input_date(f"Новая дата ({event.date}): ") if input("Изменить дату? (y/n): ").lower() == 'y' else event.date
                    diary.edit_event(event_id, new_title, new_importance, new_date)
                else:
                    print("Событие не найдено.")
            except ValueError:
                print("Некорректный ввод ID.")
        elif choice == '4':
            # Удаление события
            try:
                event_id = int(input("Введите ID события для удаления: "))
                diary.delete_event(event_id)
            except ValueError:
                print("Некорректный ввод ID.")
        elif choice == '5':
            # Отметить событие как выполненное
            try:
                event_id = int(input("Введите ID события для отметки как выполненного: "))
                diary.mark_completed(event_id)
            except ValueError:
                print("Некорректный ввод ID.")
        elif choice == '6':
            diary.sort_events_by_date()  # Сортировка событий по дате
        elif choice == '0':
            print("До свидания!")
            break  # Выход из программы
        else:
            print("Некорректный выбор. Пожалуйста, попробуйте снова.")  # Обработка неправильного ввода

if __name__ == "__main__":
    main()
