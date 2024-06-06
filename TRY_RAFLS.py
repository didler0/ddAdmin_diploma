import tkinter as tk
from tkinter import messagebox
import pyodbc

class DatabaseConnector:
    def __init__(self, server_name, database_name):
        self.server_name = server_name
        self.database_name = database_name
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={self.server_name};DATABASE={self.database_name};Trusted_Connection=yes;'
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to SQL Server successfully!")
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"Failed to connect to SQL Server: {str(e)}")

def on_connect_button_click():
    server_name = server_entry.get()
    database_name = database_entry.get()
    db_connector = DatabaseConnector(server_name, database_name)
    db_connector.connect()

# Создаем главное окно
root = tk.Tk()
root.title("Connect to Database")

# Поля для ввода имени сервера и базы данных
tk.Label(root, text="Server Name:").pack(pady=5)
server_entry = tk.Entry(root)
server_entry.pack(pady=5)

tk.Label(root, text="Database Name:").pack(pady=5)
database_entry = tk.Entry(root)
database_entry.pack(pady=5)

# Кнопка для подключения к базе данных
connect_button = tk.Button(root, text="Connect", command=on_connect_button_click)
connect_button.pack(pady=20)

# Запускаем главный цикл обработки событий
root.mainloop()
