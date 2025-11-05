from collections import deque  # Импортируем очередь


# Класс Посетитель - хранит данные о посетителе выставки
class Visitor:
    def __init__(self, id, name, dress_number):
        self.id = id  # Уникальный идентификатор
        self.name = name  # Имя посетителя
        self.dress_number = dress_number  # Номер одежды в гардеробе


# Класс Гардероб - управляет очередью и хранением одежды
class Wardrobe:
    def __init__(self):
        self.queue = deque()  # Очередь посетителей (первый пришел - первый ушел)
        self.storage = {}  # Словарь для быстрого поиска по номеру одежды
        self.load_data()  # Загружаем данные при создании гардероба

    def add_visitor(self, visitor):
        """Добавить посетителя в очередь гардероба"""
        self.queue.append(visitor)  # Добавляем в конец очереди
        self.storage[visitor.dress_number] = visitor  # Сохраняем в хранилище
        self.save_data()  # Сохраняем в файл
        print(f"+ {visitor.name} сдал одежду №{visitor.dress_number}")

    def serve_visitor(self):
        """Обслужить следующего посетителя в очереди"""
        if not self.queue:  # Проверяем, не пуста ли очередь
            print("Очередь пуста!")
            return

        visitor = self.queue.popleft()  # Берем первого из очереди
        del self.storage[visitor.dress_number]  # Удаляем из хранилища
        self.save_data()  # Сохраняем изменения
        print(f"- {visitor.name} получил одежду №{visitor.dress_number}")

    def show_queue(self):
        """Показать текущее состояние очереди"""
        print(f"В очереди: {len(self.queue)} человек")
        for v in self.queue:
            print(f"  {v.name} (№{v.dress_number})")

    def save_data(self):
        """Сохранить данные очереди в текстовый файл"""
        with open('wardrobe.txt', 'w') as f:
            for visitor in self.queue:
                # Записываем каждого посетителя в формате: id,имя,номер_одежды
                f.write(f"{visitor.id},{visitor.name},{visitor.dress_number}\n")

    def load_data(self):
        """Загрузить данные очереди из текстового файла"""
        try:
            with open('wardrobe.txt', 'r') as f:
                for line in f:
                    if line.strip():  # Пропускаем пустые строки
                        # Разбиваем строку на части: id, имя, номер одежды
                        id, name, dress = line.strip().split(',')
                        visitor = Visitor(int(id), name, int(dress))
                        self.queue.append(visitor)
                        self.storage[visitor.dress_number] = visitor
        except FileNotFoundError:
            # Если файл не найден - начинаем с пустой очереди
            pass


# Главная программа - точка входа в приложение
def main():
    wardrobe = Wardrobe()  # Создаем гардероб

    # Бесконечный цикл меню
    while True:
        print("\n1 - Сдать одежду")
        print("2 - Получить одежду")
        print("3 - Показать очередь")
        print("0 - Выход")

        choice = input("Выберите: ")

        if choice == "1":
            # Сдать одежду: запрашиваем данные и создаем посетителя
            name = input("Имя: ")
            dress = int(input("Номер одежды: "))
            # ID генерируем как длина очереди + 1
            visitor = Visitor(len(wardrobe.queue) + 1, name, dress)
            wardrobe.add_visitor(visitor)

        elif choice == "2":
            # Получить одежду: обслуживаем первого в очереди
            wardrobe.serve_visitor()

        elif choice == "3":
            # Показать текущую очередь
            wardrobe.show_queue()

        elif choice == "0":
            # Выход из программы
            break


# Запускаем программу только если это главный файл
if __name__ == "__main__":
    main()
