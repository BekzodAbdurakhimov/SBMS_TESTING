import tkinter as tk
from tkinter import messagebox
import subprocess

# Функция для сохранения логина и пароля в файл login_x_password.py
def save_credentials_to_config(login, password):
    try:
        with open('login_x_password.py', 'w') as config_file:
            config_file.write(f'LOGIN = "{login}"\n')
            config_file.write(f'PASSWORD = "{password}"\n')
        messagebox.showinfo("Успех", "Данные успешно сохранены!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")


# Функция для обработки нажатия кнопки "Сохранить"
def on_submit():
    login = login_entry.get()
    password = password_entry.get()

    if not login:
        messagebox.showwarning("Предупреждение", "Введите логин")
        return
    if not password:
        messagebox.showwarning("Предупреждение", "Введите пароль")
        return

    # Сохранить логин и пароль в файл
    save_credentials_to_config(login, password)


# Функция для запуска тестов
def run_tests():
    try:
        subprocess.run(["python", "run_all_tests_v2.py"], check=True)
        messagebox.showinfo("Успех", "Тесты успешно запущены")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить тесты: {e}")


# Создание окна
root = tk.Tk()
root.title("Тестирование SBMS")

# Установите размер окна
window_width = 300
window_height = 250

# Получите размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Рассчитайте координаты центра
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Установите размеры и позицию окна
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Метки и поля ввода
tk.Label(root, text="Логин:").pack(pady=5)
login_entry = tk.Entry(root)
login_entry.pack(pady=5)

tk.Label(root, text="Пароль:").pack(pady=5)
password_entry = tk.Entry(root, show='*')
password_entry.pack(pady=5)

# Кнопка "Сохранить"
submit_button = tk.Button(root, text="Сохранить", command=on_submit)
submit_button.pack(pady=10)

# Кнопка "Запустить тест кейсы"
test_button = tk.Button(root, text="Запустить тест кейсы", command=run_tests)
test_button.pack(pady=10)

# Запуск основного цикла приложения
root.mainloop()
