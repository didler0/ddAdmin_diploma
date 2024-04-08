import customtkinter
import tkinter
import re
from dataBase import *
from CTkMessagebox import CTkMessagebox
import CTkAddDelCombobox
from hPyT import *

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

db_manager = DatabaseManager('DDLAPTOP\\SQLEXPRESS', 'PCC')



class AddDevice_(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabview = None
        self.widgetsBasic = []
        self.widgetsDetail = []
        self.widgetsComponents = []
        self.create_window()
        # maximize_minimize_button.hide(self)

    def create_window(self):
        self.title("Add Computer")
        self.geometry("600x595")

        labels_basic = ["IP Адрес", "Название", "Сетевое имя", "Тип устройства", "Место установки", "Описание",
                        "Материально ответственный", "Филиал", "Структурное подразделение"]
        self.widgetsBasic = []
        labels_detail = ["Инвентарный №", "Серийный №", "MAC - адрес", "Операционная система", "Год покупки", "Месяцы гарантии"]
        self.widgetsDetail = []
        labels_components = ["Процессор", "ОЗУ", "Материнская плата", "Видеокарта", "Блок питания", "Сетевая карта", "Куллер", "Корпус", "HDD", "SSD",
                             "Монитор", "Клавиатура", "Мышь", "Аудио"]
        self.widgetsComponents = []

        self.grid_columnconfigure(0, weight=1)
        self.frame = customtkinter.CTkScrollableFrame(self, height=520)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.tabview = customtkinter.CTkTabview(master=self.frame, height=515, width=550)
        self.tabview.pack()

        self.tabview.add("Базовая информация")
        self.create_basic_info_tab(labels_basic)
        self.tabview.add("Детальное описание")
        self.create_detail_info_tab(labels_detail)
        self.tabview.add("Компоненты")
        self.create_components_info_tab(labels_components)

    def create_basic_info_tab(self, labels_basic):
        self.tabview.tab("Базовая информация").grid_columnconfigure(1,weight=1)
        for i, text in enumerate(labels_basic):
            label = customtkinter.CTkLabel(master=self.tabview.tab("Базовая информация"), text=text, font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=10, sticky="ew")

            if text == "IP Адрес":
                entry = customtkinter.CTkEntry(master=self.tabview.tab("Базовая информация"), placeholder_text="IP Адрес")
                entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(entry)
            elif text == "Сетевое имя":
                entry = customtkinter.CTkEntry(master=self.tabview.tab("Базовая информация"), placeholder_text="Сетевое имя")
                entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(entry)
            elif text == "Тип устройства":
                data = db_manager.get_data("type_of_device", "name", "")
                data = [str(row[0]) for row in data]
                type_of_device = CTkAddDelCombobox.ComboBoxWithButtons(table="type_of_device",master=self.tabview.tab("Базовая информация"),values=data)
                type_of_device.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(type_of_device)
            elif text == "Филиал":
                data = db_manager.get_data("branch_office", "name", "")
                data = [str(row[0]) for row in data]
                branch_office = CTkAddDelCombobox.ComboBoxWithButtons(table="branch_office",master=self.tabview.tab("Базовая информация"),values=data)
                branch_office.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(branch_office)
            elif text == "Структурное подразделение":
                data = db_manager.get_data("structural_unit", "name", "")
                data = [str(row[0]) for row in data]
                structural_unit = CTkAddDelCombobox.ComboBoxWithButtons(table="structural_unit",master=self.tabview.tab("Базовая информация"), values=data)
                structural_unit.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(structural_unit)
            else:
                textBox = customtkinter.CTkTextbox(master=self.tabview.tab("Базовая информация"), height=90)
                textBox.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(textBox)

    def create_detail_info_tab(self, labels_detail):
        pass

    def create_components_info_tab(self, labels_components):
        pass


if __name__ == "__main__":
    root = tkinter.Tk()
    app = AddDevice_(root)
    root.mainloop()
