import json
import socket
import tkinter as tk

IP = '127.0.0.1'
PORT = 4000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
client.settimeout(3)

root = tk.Tk()
root.title("Admin-panel")
root.geometry("500x700")

label_response = tk.Label(root, text="", width=60, height=40, borderwidth=1, relief="solid")
label_response.pack(pady=10)

def admin():
    json_output = json.dumps({"data": '', "action": "ADMIN"})
    client.send(json_output.encode())
    response = client.recv(4096).decode()
    label_response.config(text=f"Ответ сервера:\n{response}")

def exit_app():
    json_output = json.dumps({"data": "", "action": "BYE"})
    client.send(json_output.encode())
    client.close()
    root.destroy()

tk.Button(root, text="Админ", command=admin).pack(pady=5)
tk.Button(root, text="Выход", command=exit_app).pack(pady=5)

root.mainloop()