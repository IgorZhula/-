import os

class Book:
    def __init__(self, title, author, status="доступна"):
        self.title = title #Название книги
        self.author = author #Автор
        self.status = status #Статус

    def __str__(self):
        return f"{self.title} - {self.author} ({self.status})"

class User:
    def __init__(self, name):
        self.name = name
        self.borrowed = []

class Library:
    def __init__(self):
        self.books = []
        self.users = []
        self.current = None
        self.load()

    def load(self):
        # Книги
        if os.path.exists("books.txt"):
            with open("books.txt", "r") as f:
                for line in f:
                    if line.strip():
                        t, a, s = line.strip().split("|")
                        self.books.append(Book(t, a, s))

        # Пользователи
        if os.path.exists("users.txt"):
            with open("users.txt", "r") as f:
                for line in f:
                    if line.strip():
                        data = line.strip().split("|")
                        user = User(data[0])
                        if len(data) > 1 and data[1]:
                            user.borrowed = data[1].split(",")
                        self.users.append(user)

    # Сохранение в файлы
    def save(self):
        # Книги
        with open("books.txt", "w") as f:
            for book in self.books:
                f.write(f"{book.title}|{book.author}|{book.status}\n")

        # Пользователи
        with open("users.txt", "w") as f:
            for user in self.users:
                f.write(f"{user.name}|{','.join(user.borrowed)}\n")

    # Поиск книги
    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    # Поиск пользователя
    def find_user(self, name):
        for user in self.users:
            if user.name.lower() == name.lower():
                return user
        return None

    # Меню библиотекаря
    def librarian(self):
        while True:
            print("\n1. Добавить книгу")
            print("2. Удалить книгу")
            print("3. Добавить пользователя")
            print("4. Все пользователи")
            print("5. Все книги")
            print("6. Выйти")

            c = input("Выбор: ")

            if c == "1":
                title = input("Название: ")
                author = input("Автор: ")
                self.books.append(Book(title, author))
                print("Книга добавлена")

            elif c == "2":
                title = input("Название книги: ")
                book = self.find_book(title)
                if book:
                    if book.status == "доступна":
                        self.books.remove(book)
                        print("Книга удалена")
                    else:
                        print("Книга выдана, нельзя удалить")
                else:
                    print("Книга не найдена")

            elif c == "3":
                name = input("Имя пользователя: ")
                if not self.find_user(name):
                    self.users.append(User(name))
                    print("Пользователь добавлен")
                else:
                    print("Пользователь уже есть")

            elif c == "4":
                print("\nВсе пользователи:")
                if not self.users:
                    print("Нет пользователей")
                for u in self.users:
                    print(f"{u.name} (книг: {len(u.borrowed)})")

            elif c == "5":
                print("\nВсе книги:")
                if not self.books:
                    print("Нет книг")
                for b in self.books:
                    print(b)

            elif c == "6":
                break

            else:
                print("Неверный выбор")

    # Меню пользователя
    def user_menu(self):
        user = self.current
        while True:
            print(f"\nПользователь: {user.name}")
            print("1. Доступные книги")
            print("2. Взять книгу")
            print("3. Вернуть книгу")
            print("4. Мои книги")
            print("5. Выйти")

            c = input("Выбор: ")

            if c == "1":
                print("\nДоступные книги:")
                found = False
                for b in self.books:
                    if b.status == "доступна":
                        print(f"- {b.title} ({b.author})")
                        found = True
                if not found:
                    print("Нет доступных книг")

            elif c == "2":
                title = input("Название книги: ")
                book = self.find_book(title)
                if book:
                    if book.status == "доступна":
                        book.status = "выдана"
                        user.borrowed.append(book.title)
                        print("Книга взята")
                    else:
                        print("Книга уже выдана")
                else:
                    print("Книга не найдена")

            elif c == "3":
                if not user.borrowed:
                    print("У вас нет книг")
                    continue

                print("Ваши книги:")
                for i, title in enumerate(user.borrowed, 1):
                    print(f"{i}. {title}")

                try:
                    num = int(input("Номер для возврата: ")) - 1
                    if 0 <= num < len(user.borrowed):
                        title = user.borrowed[num]
                        book = self.find_book(title)
                        if book:
                            book.status = "доступна"
                            user.borrowed.pop(num)
                            print("Книга возвращена")
                    else:
                        print("Неверный номер")
                except:
                    print("Ошибка ввода")

            elif c == "4":
                print("\nВаши книги:")
                if not user.borrowed:
                    print("Нет книг")
                for title in user.borrowed:
                    print(f"- {title}")

            elif c == "5":
                break

            else:
                print("Неверный выбор")

    # Главное меню
    def start(self):
        print("=== БИБЛИОТЕКА ===")

        while True:
            print("\n1. Библиотекарь")
            print("2. Пользователь")
            print("3. Выход")

            role = input("Кто вы? ")

            if role == "1":
                # Простой вход для библиотекаря
                self.librarian()

            elif role == "2":
                name = input("Ваше имя: ")
                user = self.find_user(name)

                if user:
                    self.current = user
                    self.user_menu()
                else:
                    print("Пользователь не найден")

            elif role == "3":
                self.save()
                print("Данные сохранены. Пока!")
                break

            else:
                print("Неверный выбор")

if __name__ == "__main__":
    lib = Library()
    lib.start()