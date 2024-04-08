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

        add_data_button = customtkinter.CTkButton(master=self, text="Добавить", command=lambda: self.add_whole_data_to_bd())
        add_data_button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

    def create_basic_info_tab(self, labels_basic):
        self.tabview.tab("Базовая информация").grid_columnconfigure(1, weight=1)
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
                type_of_device = CTkAddDelCombobox.ComboBoxWithButtons(table="type_of_device", master=self.tabview.tab("Базовая информация"), values=data)
                type_of_device.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(type_of_device)
            elif text == "Филиал":
                data = db_manager.get_data("branch_office", "name", "")
                data = [str(row[0]) for row in data]
                branch_office = CTkAddDelCombobox.ComboBoxWithButtons(table="branch_office", master=self.tabview.tab("Базовая информация"), values=data)
                branch_office.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(branch_office)
            elif text == "Структурное подразделение":
                data = db_manager.get_data("structural_unit", "name", "")
                data = [str(row[0]) for row in data]
                structural_unit = CTkAddDelCombobox.ComboBoxWithButtons(table="structural_unit", master=self.tabview.tab("Базовая информация"), values=data)
                structural_unit.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(structural_unit)
            else:
                textBox = customtkinter.CTkTextbox(master=self.tabview.tab("Базовая информация"), height=90)
                textBox.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(textBox)

    def create_detail_info_tab(self, labels_detail):
        self.tabview.tab("Детальное описание").grid_columnconfigure(1, weight=1)
        self.tabview.tab("Детальное описание").grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        for i, text in enumerate(labels_detail):
            label = customtkinter.CTkLabel(master=self.tabview.tab("Детальное описание"), text=text, font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=10, sticky="ew")

            entry = customtkinter.CTkEntry(master=self.tabview.tab("Детальное описание"), placeholder_text=text)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
            self.widgetsDetail.append(entry)

    def create_components_info_tab(self, labels_components):
        self.tabview.tab("Компоненты").grid_columnconfigure(1, weight=1)

        for i, text in enumerate(labels_components):
            label = customtkinter.CTkLabel(master=self.tabview.tab("Компоненты"), text=text, font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=10, sticky="ew")

            entry = customtkinter.CTkEntry(master=self.tabview.tab("Компоненты"), placeholder_text=text)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
            self.widgetsComponents.append(entry)

    def get_data_from_components(self):
        values_component = []
        for widget in self.widgetsComponents:
            if isinstance(widget, customtkinter.CTkEntry):
                value = widget.get()
                widget.delete(0, customtkinter.END)
            else:
                value = None
            values_component.append(value)

        return values_component

    def get_data_from_details(self):
        values_detail = []
        for widget in self.widgetsDetail:
            if isinstance(widget, customtkinter.CTkEntry):
                value = widget.get()
                widget.delete(0, customtkinter.END)
            else:
                value = None
            values_detail.append(value)

        return values_detail

    def get_data_from_basic(self):
        values_basic = []
        for widget in self.widgetsBasic:
            if isinstance(widget, customtkinter.CTkEntry):
                value = widget.get()  # Получение значения из CTkEntry
                widget.delete(0, customtkinter.END)
            elif isinstance(widget, customtkinter.CTkTextbox):
                value = widget.get("1.0", "end-1c")  # Получение значения из CTkTextbox
                widget.delete("1.0", "end-1c")
            elif isinstance(widget, CTkAddDelCombobox.ComboBoxWithButtons):
                value = widget.get_current_value()
                widget.clear_data()
            else:
                value = None
            values_basic.append(value)
        return values_basic

    def clear_data_from_section(self, widgets):
        """
        Clear data from a section based on the provided list of widgets.
        """
        for widget in widgets:
            if isinstance(widget, customtkinter.CTkEntry):
                widget.delete(0, customtkinter.END)
            elif isinstance(widget, customtkinter.CTkTextbox):
                widget.delete("1.0", "end-1c")
            elif isinstance(widget, CTkAddDelCombobox.ComboBoxWithButtons):
                widget.clear_data()

    def clear_whole_data(self):
        """
        Clear all data in the components, details, and basic sections.
        """
        self.clear_data_from_section(self.widgetsBasic)
        self.clear_data_from_section(self.widgetsDetail)
        self.clear_data_from_section(self.widgetsComponents)

    def add_whole_data_to_bd(self):
        try:
            # Получение данных
            values_component = self.get_data_from_components()
            values_details = self.get_data_from_details()
            values_basic = self.get_data_from_basic()

            # Вставка данных в таблицу basic_info
            columns_basic = "ip, name, network_name, type_of_device_id, place_of_installation_id, description, " \
                            "material_resp_person, last_status, data_status, last_repair, detail_info_id, " \
                            "branch_id, structural_unit_id"
            if db_manager.insert_data("basic_info", columns_basic, values_basic):
                print("Data inserted into basic_info successfully.")
            else:
                print("Failed to insert data into basic_info.")

            # Вставка данных в таблицу detail_info
            columns_detail = "component_id, inventory_number, serial_number, mac_address, oper_system, " \
                             "year_of_purchase, month_of_warranty"
            if db_manager.insert_data("detail_info", columns_detail, values_details):
                print("Data inserted into detail_info successfully.")
            else:
                print("Failed to insert data into detail_info.")

            # Вставка данных в таблицу component
            columns_component = "processor, ram, motherboard, gpu, psu, networkCard, cooler, chasis, " \
                                "hdd, ssd, monitor, keyboard, mouse, audio"
            if db_manager.insert_data("component", columns_component, values_component):
                print("Data inserted into component successfully.")
            else:
                print("Failed to insert data into component.")

            self.clear_whole_data()
        except Exception as e:
            print("An error occurred:", e)
            # Откатываем все операции в случае возникновения ошибки
            self.conn.rollback()


if __name__ == "__main__":
    root = tkinter.Tk()
    app = AddDevice_(root)
    root.mainloop()
