import os

def get_and_save_user_data():
    # Запрашиваем логин и пароль
    LOGIN = input("Введите логин: ")
    PASSWORD = input("Введите пароль: ")

    # Путь к уже существующему файлу config.py
    config_path = "config.py"

    # Проверяем, существует ли файл config.py
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            lines = file.readlines()

        # Флаги для отслеживания наличия переменных
        username_found = False
        password_found = False

        # Обновляем строки, если переменные уже существуют
        for i, line in enumerate(lines):
            if line.startswith("LOGIN"):
                lines[i] = f"LOGIN = '{LOGIN}'\n"
                username_found = True
            elif line.startswith("PASSWORD"):
                lines[i] = f"PASSWORD = '{PASSWORD}'\n"
                password_found = True

        # Если переменные не найдены, добавляем их в конце файла
        if not username_found:
            lines.append(f"LOGIN = '{LOGIN}'\n")
        if not password_found:
            lines.append(f"PASSWORD = '{PASSWORD}'\n")

        # Записываем обновлённые данные обратно в файл
        with open(config_path, 'w') as file:
            file.writelines(lines)

        print(f"Логин и пароль успешно сохранены в {config_path}.")
    else:
        print(f"Файл {config_path} не найден.")

get_and_save_user_data()