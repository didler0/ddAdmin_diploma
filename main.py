from tkinter import messagebox

import customtkinter
from CTkMessagebox import CTkMessagebox
from hPyT import *
import tkinter as tk
from dataBase import *
from addDevice import *

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

db_manager = DatabaseManager('DDLAPTOP\\SQLEXPRESS', 'PCC')
db_manager.create_tables()


class UpperFrame(customtkinter.CTkFrame):
    """Класс для верхнего фрейма"""

    def __init__(self, master):
        """Конструктор класса"""
        super().__init__(master)

        self.toplevel_window = None

        button_data = [
            {"text": "Добавить устройство", "command": self.AddPc},
            {"text": "Редактировать данные о устройствах", "command": self.EditPc},
            {"text": "Формирование отчетов", "command": self.ExportPc},
            {"text": "Обновить данные", "command": self.ReloadData},
            {"text": "Ремонты", "command": self.Repairs, "fg_color": "#FF8C19", "hover_color": "#4DFFFF", "text_color": "black"}
        ]

        for idx, button_info in enumerate(button_data):
            button = customtkinter.CTkButton(master=self, text=button_info["text"],
                                             command=lambda command=button_info["command"]: command())
            button.grid(row=0, column=idx, pady=10, padx=10)
            if "fg_color" in button_info:
                button.configure(fg_color=button_info["fg_color"])
            if "hover_color" in button_info:
                button.configure(hover_color=button_info["hover_color"])
            if "text_color" in button_info:
                button.configure(text_color=button_info["text_color"])

        self.AppearanceButton = customtkinter.CTkOptionMenu(
            self, values=["Светлая", "Тёмная"], command=self.change_appearance_mode_event)
        self.AppearanceButton.grid(
            row=0, column=len(button_data), padx=20, pady=(10, 10))

    def AddPc(self):
        """Метод для открытия окна добавления устройства"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AddDevice_(self)
        else:
            self.toplevel_window.focus()

    def EditPc(self):
        """Метод для открытия окна редактирования устройства"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = editPC(self)
        else:
            self.toplevel_window.focus()

    def ReloadData(self):
        """Метод для обновления данных"""
        self.scroll_frame.destroy_and_recreate()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Метод для смены цветовой темы"""
        if new_appearance_mode == "Светлая":
            customtkinter.set_appearance_mode("Light")
        elif new_appearance_mode == "Тёмная":
            customtkinter.set_appearance_mode("Dark")

    def Repairs(self):
        """Метод для открытия окна ремонтов"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():

            self.toplevel_window = Repairs(self)
        else:
            self.toplevel_window.focus()

    def ExportPc(self):
        """Метод для открытия окна экспорта данных"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():

            self.toplevel_window = Reports(self)
        else:
            self.toplevel_window.focus()
            # стальные методы класса остаются без изменений


class DownFrame(customtkinter.CTkScrollableFrame):
    """"Класс для нижнего фрейма"""

    def __init__(self, master):
        """"Инициализация нижнего фрейма"""
        super().__init__(master, height=400)
        self.struct_unit_ = customtkinter.CTkTabview(master=self)

        self.struct_unit_.pack(fill='both', expand=True, padx=10, pady=10)
        self.struct_unit_tabs = []
        self.branch_ = customtkinter.CTkTabview(master=self.struct_unit_)
        self.branch_.grid(row=0, column=0, padx=10, pady=10)
        self.branches_tabs = []

        data = db_manager.get_unique_branch_struct()

        if data is not None:
            branches_, units_ = data
        else:
            CTkMessagebox(title="Ошибка", message="Отсутствуют данные!", icon="cancel")
        branches_, units_.sort()

        for branch_name in branches_:
            print(branch_name)
            tab = self.branch_.add(branch_name)
            self.branches_tabs.append(tab)

        for unit_name in units_:
            tab = self.struct_unit_.add(unit_name)
            self.struct_unit_tabs.append(tab)


class App(customtkinter.CTk):
    """Класс приложения"""
    WIDTH = 1100
    HEIGHT = 500

    def __init__(self):
        """Инициализация главного окна приложения."""
        super().__init__()

        self.title("ddAdmin")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        maximize_minimize_button.hide(self)
        self.grid_columnconfigure(0, weight=1)

        maximize_minimize_button.hide(self)
        self.frame_down = DownFrame(self)
        self.frame_down.grid(row=1, column=0, padx=10, pady=10)
        self.frame_up = UpperFrame(self)
        self.frame_up.grid(row=0, column=0, padx=10, pady=10)

    def on_closing(self):
        """Обработчик события закрытия приложения."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            db_manager.close_connection()  # Закрываем соединение с базой данных
            self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
