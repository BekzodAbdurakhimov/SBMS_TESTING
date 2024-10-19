import os
def delete_or_create_login_file():
    file_path = 'login_x_password.py'

    # Проверяем существует ли файл
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f'{file_path} успешно удален.')
    else:
    # Создаем файл если его не существует
        with open(file_path, 'w') as f:
            f.write('# Файл для хранения логина и пароля\n')
        print(f'{file_path} создан, так как он уже существовал.')

if __name__ == "__main__":
    delete_or_create_login_file()