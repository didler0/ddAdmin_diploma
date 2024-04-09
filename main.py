from tkinter import messagebox

import customtkinter
from CTkMessagebox import CTkMessagebox
from hPyT import *
import tkinter as tk
from dataBase import *
from addDevice import *
from editDevice import *

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
            self, values=[ "Тёмная","Светлая"], command=self.change_appearance_mode_event)
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
            self.toplevel_window = EditDevice_(self)
        else:
            self.toplevel_window.focus()


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

class MiddleFrame(customtkinter.CTkFrame):

    def __init__(self,master):
        super().__init__(master)



        customtkinter.CTkLabel(master=self, text="Выберите филиал").grid(row=0, column=0, padx=10, pady=10,sticky='nsew')
        customtkinter.CTkLabel(master=self, text="Выберите структурное подразделение").grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        combobox1 = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly")
        combobox1.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.FillComboBox(combobox1,db_manager.get_data("branch_office","*"))

        combobox2 = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly")
        combobox2.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.FillComboBox(combobox2, db_manager.get_data("structural_unit", "*"))


        load_data_button = customtkinter.CTkButton(master=self, text="Загрузить данные", command=lambda: self.add_whole_data_to_bd())
        load_data_button.grid(row=0, column=2, padx=10, pady=10,rowspan=2, sticky='nsew', columnspan=2)

        reload_data_button = customtkinter.CTkButton(master=self, text="Обновить", hover_color="green",command=lambda: self.add_whole_data_to_bd())
        reload_data_button.grid(row=0, column=4, padx=10, pady=10, rowspan=2, sticky='nsew', columnspan=2)

    def FillComboBox(self, combobox_, data_):
        dataa = [str(data[0]) + " | " + str(data[1]) for data in data_]
        combobox_.configure(values=dataa)
        self.update()



class DownFrame(customtkinter.CTkScrollableFrame):
    """"Класс для нижнего фрейма"""

    def __init__(self, master):
        super().__init__(master, height=400)
        self.grid_columnconfigure(0, weight=1)
        self.struct_unit_ = customtkinter.CTkTabview(master=self)
        self.struct_unit_.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.branches_tabs = {}
        self.units_tabs = {}

        # Получение уникальных филиалов и структурных подразделений из базы данных
        data = db_manager.get_unique_branch_struct()
        if data is not None:
            branches_, units_ = data
            branches_.sort()
            units_.sort()
        else:
            CTkMessagebox(title="Ошибка", message="Отсутствуют данные!", icon="cancel")

        # Создание вкладок для филиалов и структурных подразделений
        for branch_name in branches_:
            tab = self.struct_unit_.add(branch_name)
            self.branches_tabs[branch_name] = tab

        for unit_name in units_:
            tab = self.struct_unit_.add(unit_name)
            self.units_tabs[unit_name] = tab


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
        self.grid_rowconfigure((1),weight=0)

        maximize_minimize_button.hide(self)
        self.frame_middle = MiddleFrame(self)
        self.frame_middle.grid(row=1, column=0, padx=10, pady=10)
        self.frame_down = DownFrame(self)
        self.frame_down.grid(row=2, column=0, padx=10, pady=10,sticky="nsew")

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
