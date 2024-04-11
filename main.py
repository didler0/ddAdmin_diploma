from tkinter import messagebox

import customtkinter
from CTkMessagebox import CTkMessagebox
from hPyT import *
import tkinter as tk
from dataBase import *
from addDevice import *
from editDevice import *
from aioBranchOfficeStructuralUnit import *
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")
# Сохранение строки в файл
with open('database_info.txt', 'w') as file:
    file.write("DDLAPTOP\\SQLEXPRESS, PCC")


with open('database_info.txt', 'r') as file:
    db_info = file.read().strip()
db_info_parts = db_info.split(', ')
db_manager = DatabaseManager(db_info_parts[0], db_info_parts[1])
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
            {"text": "Редактировать филиалы", "command": self.EditBranch},
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
    def EditBranch(self):
        """Метод для открытия окна редактирования филиалов"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AioBranchOfficeStructuralUnit(self)
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
        data = db_manager.get_data("branch_office", "name", "")
        data = [str(row[0]) for row in data]
        self.combobox1_branch_office = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly", command=self.load_data)
        self.combobox1_branch_office.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.FillComboBox(self.combobox1_branch_office,data)

        self.combobox2_structural_unit = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly",command=self.load_main_data)
        self.combobox2_structural_unit.grid(row=1, column=1, padx=10, pady=10, sticky="w")


        reload_data_button = customtkinter.CTkButton(master=self, text="Обновить", hover_color="green",command=lambda: self.reload_all())
        reload_data_button.grid(row=0, column=4, padx=10, pady=10, rowspan=2, sticky='nsew', columnspan=2)

    def load_main_data(self,choice):
        print(self.combobox1_branch_office.get())
        print(choice)
        branch_id = 1
        structural_unit_id = 55
        result = db_manager.exec_procedure("GetInfoByBranchAndStructuralUnit", branch_id, structural_unit_id)
        print(result)
        # Assuming result contains the data returned from the stored procedure

        # Define the structure of your data
        data_structure = {
            'basic_info': {
                'id': None,
                'ip': None,
                'name': None,
                'network_name': None,
                'type_of_device_id': None,
                'place_of_installation_id': None,
                'description': None,
                'material_resp_person_id': None,
                'last_status': None,
                'data_status': None,
                'last_repair': None,
                'detail_info_id': None,
                'branch_id': None,
                'structural_unit_id': None
            },
            'detail_info': {
                'id': None,
                'component_id': None,
                'inventory_number': None,
                'serial_number': None,
                'mac_address': None,
                'oper_system': None,
                'year_of_purchase': None,
                'month_of_warranty': None
            },
            'component': {
                'id': None,
                'processor': None,
                'ram': None,
                'motherboard': None,
                'gpu': None,
                'psu': None,
                'networkCard': None,
                'cooler': None,
                'chasis': None,
                'hdd': None,
                'ssd': None,
                'monitor': None,
                'keyboard': None,
                'mouse': None,
                'audio': None
            },
            'type_of_device': {
                'id': None,
                'name': None
            },
            'place_of_installation': {
                'id': None,
                'name': None
            },
            'material_resp_person': {
                'id': None,
                'name': None
            }
        }

        # Initialize the parsed data dictionary
        parsed_data = {}

        # Iterate over the result and fill in the parsed data dictionary
        for row in result:
            parsed_row = {}
            for table_name, table_structure in data_structure.items():
                parsed_row[table_name] = {}
                for i, column_value in enumerate(row[:len(table_structure)]):
                    column_name = list(table_structure.keys())[i]
                    parsed_row[table_name][column_name] = column_value
            parsed_data[row[0]] = parsed_row

        # Display the parsed data
        print(parsed_data)

    def reload_all(self):
        pass
    def FillComboBox(self, combobox, data_):
        data__ = [str(data) for data in data_]
        combobox.configure(values=data__)
        self.update()
    def load_data(self,choice):
        data= db_manager.exec_procedure("GetStructuralUnits",choice)
        data = [str(row[0]) for row in data]
        self.FillComboBox(self.combobox2_structural_unit,data)




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
        #data = db_manager.get_unique_branch_struct()
        #if data is not None:
        #    branches_, units_ = data
        #    branches_.sort()
        #    units_.sort()
        #else:
        #    CTkMessagebox(title="Ошибка", message="Отсутствуют данные!", icon="cancel")
#
        ## Создание вкладок для филиалов и структурных подразделений
        #for branch_name in branches_:
        #    tab = self.struct_unit_.add(branch_name)
        #    self.branches_tabs[branch_name] = tab
#
        #for unit_name in units_:
        #    tab = self.struct_unit_.add(unit_name)
        #    self.units_tabs[unit_name] = tab


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
