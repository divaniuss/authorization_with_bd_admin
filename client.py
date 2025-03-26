
import json
import socket
import hashlib

IP = '127.0.0.1'
PORT = 4000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
while True:
    ansv = input("Регистрация(+) или вход?(-) или (!) для выхода?: ")
    if ansv == "+":
        while True:
            login_reg = input("\nВведите новый логин: ")
            password_reg = input("Введите новый пароль: ")
            password_reg_second = input("Введите пароль повторно:")

            if (password_reg == password_reg_second) and (len(login_reg.strip()) != 0 and len(password_reg.strip()) != 0):
                break
            else:
                print("Пароли не совпадают или вы ничего не ввели")

        data = password_reg
        hashed_password = hashlib.sha256(data.encode()).hexdigest()
        str_hashed_password = str(hashed_password)
        json_output = json.dumps({"data": {"name": login_reg, "password": str_hashed_password}, "action": "REGISTER"})
        client.send(json_output.encode())
        print("\n Отправляю.. \n")
        ansver_reg = client.recv(1024).decode()
        print(f"Ответ сервера: {ansver_reg}\n")
    elif ansv == "-":
        while True:
            login_log = input("\nВведите ваш логин: ")
            password_log = input("Введите ваш пароль: ")

            if len(login_log.strip()) != 0 and len(password_log.strip()) != 0:
                break
            else:
                print("Пароли не совпадают или вы ничего не ввели")

        data = password_log
        hashed_password_log = hashlib.sha256(data.encode()).hexdigest()
        str_hashed_password_log = str(hashed_password_log)
        json_output = json.dumps({"data": {"name": login_log, "password": str_hashed_password_log}, "action": "LOGIN"})
        client.send(json_output.encode())
        print("\n Отправляю.. \n")
        ansver_log = client.recv(1024).decode()
        print(f"Ответ сервера: {ansver_log}\n")

    elif ansv == "!":
        json_output = json.dumps({"data": "", "action": "BYE"})
        client.send(json_output.encode())
        print("\n Отправляю.. \n")
        ansver_bye = client.recv(1024).decode()
        print(f"\nОтвет сервера: {ansver_bye}")
        break
    else:
        print("Введите + or - or !")



client.close()
