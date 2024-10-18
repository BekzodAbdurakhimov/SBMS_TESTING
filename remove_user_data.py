import os
def delete_login_file():
    file_path = 'login_x_password.py'

    # Проверяем, существует ли файл
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f'{file_path} успешно удален.')
    else:
        print(f'{file_path} не найден или уже был удален.')


if __name__ == "__main__":
    delete_login_file()
