import socket
import pyodbc
import json
from datetime import datetime

server_base = r'localhost\SQLEXPRESS'
database = 'db_logins'

dsn = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_base};DATABASE={database};Trusted_Connection=yes'

IP = '127.0.0.1'
PORT = 4000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(1)
print("Сервер запущен, ожидание подключения...")

conn, addr = server.accept()
print(f"Подключение от: {addr}")


while True:
    request = json.loads(conn.recv(1024).decode())
    now = str(datetime.now())
    action = request["action"]
    print(f"Принято: \n{request}")

    if action == "ADMIN":
        print("Просмотр:")
        try:
            conn_db = pyodbc.connect(dsn)
            cursor = conn_db.cursor()

            cursor.execute("SELECT [ID],[Time_log],[login] FROM [Clients]")
            rows = cursor.fetchall()

            result_str = ""
            for row in rows:
                result_str += f"\nID:{row[0]} Был в сети: {row[1]} Логин: {row[2]}"

            print("rez:")
            print(result_str)
            conn.send(result_str.encode())
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            conn.send(f"Ошибка подключения: {e}".encode())


    if action == "LOGIN":
        print("Вход:")
        login = request["data"]["name"]
        password = request["data"]["password"]

        try:
            conn_db = pyodbc.connect(dsn)
            cursor = conn_db.cursor()
            values = (login, password)

            insert_check = "SELECT [ID] FROM [Clients] WHERE [login] = ? AND [Password] = ?"
            cursor.execute(insert_check, values)
            print("zapisal")
            IsLoginAndPassword = cursor.fetchall()

            if IsLoginAndPassword:
                conn.send(f"Добро пожаловать {login}!".encode())

            else:
                conn.send(f"Нет такого пользователя".encode())


            insert_time = f"UPDATE [Clients] SET [Time_log] = ? WHERE [login] = ? AND [Password] = ?"
            cursor.execute(insert_time, (now, login, password))
            conn_db.commit()
            print("time")
            cursor.close()
            conn_db.close()

        except Exception as e:
            print(f"Ошибка подключения: {e}")
            conn.send(f"Ошибка подключения: {e}".encode())

    if action == "REGISTER":

        print("Регистрация:")
        login = request["data"]["name"]
        Password = request["data"]["password"]
        try:
            conn_db = pyodbc.connect(dsn)
            cursor = conn_db.cursor()

            insert_query = "INSERT INTO  [Clients] ([login], [Password]) VALUES (?, ?)"
            values = (login, Password)
            cursor.execute(insert_query, values)
            cursor.commit()
            conn_db.commit()
            print("Записано")
            result_str = "Данные успешно сохранены"
            conn.send(result_str.encode())

            cursor.close()
            conn_db.close()
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            if "23000" in str(e):
                conn.send("Этот логин уже существует".encode())
            else:
                result_str = (f"Ошибка подключения: {e}")
                conn.send(result_str.encode())

    if action == "BYE":
        print("Закрытие..")
        conn.send("Всего доброго".encode())
        break


conn.close()
server.close()