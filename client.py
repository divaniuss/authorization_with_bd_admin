
import json
import socket
import hashlib
import tkinter as tk
from tkinter import messagebox

IP = '127.0.0.1'
PORT = 4000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

root = tk.Tk()
root.title("Welcome")
root.geometry("300x200")

def register():
    reg_window = tk.Toplevel(root)
    reg_window.title("Регистрация")
    reg_window.geometry("300x200")

    tk.Label(reg_window, text="Логин:").pack()
    login_entry = tk.Entry(reg_window)
    login_entry.pack()

    tk.Label(reg_window, text="Пароль:").pack()
    password_entry = tk.Entry(reg_window, show="*")
    password_entry.pack()

    tk.Label(reg_window, text="Повторите пароль:").pack()
    password_confirm_entry = tk.Entry(reg_window, show="*")
    password_confirm_entry.pack()

    def send_register():
        login = login_entry.get().strip()
        password = password_entry.get()
        password_confirm = password_confirm_entry.get()

        if password != password_confirm or not login or not password:
            messagebox.showerror("Ошибка", "Пароли не совпадают или пустые поля")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        json_output = json.dumps({"data": {"name": login, "password": hashed_password}, "action": "REGISTER"})
        client.send(json_output.encode())
        response = client.recv(1024).decode()
        messagebox.showinfo("Ответ сервера", response)
        reg_window.destroy()

    tk.Button(reg_window, text="Зарегистрироваться", command=send_register).pack()

def login():
    login_window = tk.Toplevel(root)
    login_window.title("Логин")
    login_window.geometry("300x150")

    tk.Label(login_window, text="Логин:").pack()
    login_entry = tk.Entry(login_window)
    login_entry.pack()

    tk.Label(login_window, text="Пароль:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def send_login():
        login = login_entry.get().strip()
        password = password_entry.get()

        if not login or not password:
            messagebox.showerror("Ошибка", "Поля не должны быть пустыми")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        json_output = json.dumps({"data": {"name": login, "password": hashed_password}, "action": "LOGIN"})
        client.send(json_output.encode())
        response = client.recv(1024).decode()
        messagebox.showinfo("Ответ сервера", response)
        login_window.destroy()

    tk.Button(login_window, text="Войти", command=send_login).pack()

def exit_app():
    json_output = json.dumps({"data": "", "action": "BYE"})
    client.send(json_output.encode())
    response = client.recv(1024).decode()
    root.destroy()
    client.close()

tk.Button(root, text="Регистрация", command=register).pack(pady=5)
tk.Button(root, text="Логин", command=login).pack(pady=5)
tk.Button(root, text="Выход", command=exit_app).pack(pady=5)

root.mainloop()
