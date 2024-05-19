import customtkinter
import tkinter
import re
from docxtpl import DocxTemplate
from CTkMessagebox import CTkMessagebox
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from hPyT import *
from PIL import Image
import os
from tkcalendar import Calendar
from CTkToolTip import *
from docx import *
from datetime import datetime, timedelta
import CTkSelectDate
from CTkSelectDate import *
from dataBase import DatabaseManager
import tkinter as tk
from tkinter import filedialog
from docx.shared import RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

with open('database_info.txt', 'r') as file:
    db_info = file.read().strip()
db_info_parts = db_info.split(', ')
db_manager = DatabaseManager(db_info_parts[0], db_info_parts[1])
db_manager.create_tables()


class Reports(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.title("Формирование отчетов")
        self.geometry("1100x650")
        self.minsize(1100, 650)
        self.frame = customtkinter.CTkScrollableFrame(self, height=490, orientation="horizontal")

        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure((0, 1), weight=1)

        self.first = FirstFrameChoise(self.frame)
        self.first.grid(row=0, column=0, padx=10, pady=10, sticky="", columnspan=3)

        # Отчет по статусам работы  - готово
        self.second = FirstFrameReport(self.frame, self.first)
        self.second.grid(row=1, column=0, padx=10, pady=10, sticky="")

        # Отчет по ремонтам за промежуток дат
        self.third = SecondFrameReport(self.frame, self.first, self.second)
        self.third.grid(row=1, column=1, padx=10, pady=10, sticky="")

        # Отчет на выбранное устройство
        self.fourth = ThirdFrameReport(self.frame, self.first, self.second)
        self.fourth.grid(row=1, column=2, padx=10, pady=10, sticky="")
        # Отчет по месту установки

        # отчет по всем устройствам филиала

        # отчет по всем устройствам по структурного подразделения


class FirstFrameChoise(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(border_color="dodgerblue", border_width=3)
        customtkinter.CTkLabel(master=self, text="Выберите филиал").grid(row=0, column=0, padx=10, pady=10,
                                                                         sticky='nsew')

        customtkinter.CTkLabel(master=self, text="Выберите структурное подразделение").grid(row=1, column=0, padx=10,
                                                                                            pady=10, sticky='nsew')
        data = db_manager.get_data("branch_office", "name", "")
        data = [str(row[0]) for row in data]
        self.combobox1_branch_office = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly",
                                                                 command=self.load_data)
        self.combobox1_branch_office.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        CTkToolTip(self.combobox1_branch_office, message="Выберите филиал.")
        self.FillComboBox(self.combobox1_branch_office, data)

        self.combobox2_structural_unit = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly")
        self.combobox2_structural_unit.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        CTkToolTip(self.combobox2_structural_unit, message="Выберите структурное подразделение.")

    def load_data(self, choice):
        data = db_manager.exec_procedure("GetStructuralUnits", choice)
        data = [str(row[0]) for row in data]
        self.FillComboBox(self.combobox2_structural_unit, data)

    def FillComboBox(self, combobox, data_):
        data__ = [str(data) for data in data_]
        combobox.configure(values=data__)
        self.update()


class FirstFrameReport(customtkinter.CTkFrame):
    def __init__(self, master, first_frame_ch_instance):
        super().__init__(master)
        self.first_frame_choise = first_frame_ch_instance
        self.configure(border_color="dodgerblue", border_width=3)
        customtkinter.CTkLabel(master=self, text="Отчет по статусам работы", fg_color="gray30",
                               font=("Arial", 14)).grid(row=0, columnspan=3, column=0, padx=10, pady=10, sticky="ew")
        self.date_Start = CTkSelectDate.SelectDate(self, label_text="Выберите дату начала периода")
        self.date_Start.grid(row=1, columnspan=2, column=0, padx=10, pady=10, sticky="ew")

        self.date_End = CTkSelectDate.SelectDate(self, label_text="Выберите дату конца периода")
        self.date_End.grid(row=2, columnspan=2, column=0, padx=10, pady=10, sticky="ew")

        customtkinter.CTkLabel(master=self, text="Дата конца не включает последний день!").grid(row=3, columnspan=2,
                                                                                                column=0, padx=2,
                                                                                                pady=2, sticky="ew")

        self.MakeReport1Button = customtkinter.CTkButton(master=self, text="Сформировать и открыть отчет",
                                                         command=lambda: self.make_report())
        self.MakeReport1Button.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    def compare_dates(self, date1_str, date2_str):
        return datetime.strptime(date1_str, "%Y-%m-%d") <= datetime.strptime(date2_str, "%Y-%m-%d")

    def make_report(self):
        branch_office = self.first_frame_choise.combobox1_branch_office.get()
        structural_unit = self.first_frame_choise.combobox2_structural_unit.get()

        # Check if either combobox is empty
        if not branch_office.strip():
            CTkMessagebox(title="Ошибка", message="Выберите филиал!", icon="warning")
            return
        if not structural_unit.strip():
            CTkMessagebox(title="Ошибка", message="Выберите структурное подразделение!", icon="warning")
            return

        date_start_str = self.date_Start.get_current_date()
        date_end_str = self.date_End.get_current_date()

        # Check if either date is empty
        if not date_start_str.strip():
            CTkMessagebox(title="Ошибка", message="Выберите дату начала периода!", icon="warning")
            return
        if not date_end_str.strip():
            CTkMessagebox(title="Ошибка", message="Выберите дату конца периода!", icon="warning")
            return

        try:
            date_start = datetime.strptime(date_start_str, "%Y-%m-%d")
            date_end = datetime.strptime(date_end_str, "%Y-%m-%d")
        except ValueError as e:
            CTkMessagebox(title="Ошибка", message="Неверный формат даты!", icon="warning")
            return

        if self.compare_dates(date_start_str, date_end_str):
            diff = date_end - date_start
            if diff.days >= 0:
                print(branch_office)
                print(structural_unit)
                self.make_document()
            else:
                CTkMessagebox(title="Ошибка", message="Дата начала позже даты окончания.", icon="warning")
        else:
            CTkMessagebox(title="Ошибка", message="Дата начала позже даты окончания.", icon="warning")

    def make_document(self):
        date_start_str = self.date_Start.get_current_date()
        date_end_str = self.date_End.get_current_date()
        date_start = datetime.strptime(date_start_str, "%Y-%m-%d")
        date_end = datetime.strptime(date_end_str, "%Y-%m-%d")
        data = db_manager.exec_procedure("GetBasicInfoStatusBetweenDatesInBranchAndStructUnit",
                                         date_start, date_end,
                                         f"{self.first_frame_choise.combobox1_branch_office.get()}",
                                         f"{self.first_frame_choise.combobox2_structural_unit.get()}")
        # Создание диалогового окна выбора места сохранения документа
        root = tk.Tk()
        root.withdraw()  # Скрытие корневого окна
        file_path = filedialog.asksaveasfilename(defaultextension=".docx",
                                                 filetypes=[("Word Document", "*.docx")],
                                                 title="Выберите место сохранения документа",
                                                 initialfile="ОтчетПоСтатусамРаботы")

        if not file_path:
            return  # Прерывание функции, если пользователь не выбрал место сохранения

        doc = Document()
        title = doc.add_heading(
            f'Отчет по статусам работы устройств.\n Филиал - {self.first_frame_choise.combobox1_branch_office.get()} \n '
            f'Структурное подразделение - {self.first_frame_choise.combobox2_structural_unit.get()}', level=1)
        title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # Добавление таблицы с данными
        table = doc.add_table(rows=1, cols=5)
        table.style = 'Table Grid'
        # название, сетевое название, статус, дата,место установки
        # "('Рабочая станция', 'WS-FI05-120', 0, datetime.datetime(2024, 5, 8, 9, 21, 17, 350000), '2')"

        # Заголовки столбцов
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Название'
        hdr_cells[1].text = 'Сетевое имя'
        hdr_cells[2].text = 'Статус'
        hdr_cells[3].text = 'Место установки'
        hdr_cells[4].text = 'Дата'

        # Заполнение таблицы данными
        for item in data:
            row_cells = table.add_row().cells
            row_cells[0].text = item[0]  # Название
            row_cells[1].text = item[1]  # Сетевое имя
            row_cells[2].text = "On" if item[2] else "Off"  # Статус
            row_cells[3].text = item[4]  # Место установки
            row_cells[4].text = str(item[3])

            # Установка цвета текста в ячейке в зависимости от статуса
            if item[2]:  # Если статус равен True (1 или "On")
                color = RGBColor(0, 128, 0)  # Зеленый цвет
            else:
                color = RGBColor(255, 0, 0)  # Красный цвет
            for cell in row_cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.color.rgb = color

        # Сохранение документа
        doc.save(file_path)


class SecondFrameReport(customtkinter.CTkFrame):
    def __init__(self, master, first_frame_ch_instance, second_instance):
        super().__init__(master)
        self.first_frame_choise = first_frame_ch_instance
        self.second_frame_instance = second_instance
        self.configure(border_color="dodgerblue", border_width=3)
        customtkinter.CTkLabel(master=self, text="Отчет по ремонтам", fg_color="gray30",
                               font=("Arial", 14)).grid(row=0, columnspan=3, column=0, padx=10, pady=10, sticky="ew")
        self.date_Start = CTkSelectDate.SelectDate(self, label_text="Выберите дату начала периода")
        self.date_Start.grid(row=1, columnspan=2, column=0, padx=10, pady=10, sticky="ew")

        self.date_End = CTkSelectDate.SelectDate(self, label_text="Выберите дату конца периода")
        self.date_End.grid(row=2, columnspan=2, column=0, padx=10, pady=10, sticky="ew")

        customtkinter.CTkLabel(master=self, text="Дата конца не включает последний день!").grid(row=3, columnspan=2,
                                                                                                column=0, padx=2,
                                                                                                pady=2, sticky="ew")

        self.MakeReport1Button = customtkinter.CTkButton(master=self, text="Сформировать и открыть отчет",
                                                         command=lambda: self.make_report())
        self.MakeReport1Button.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    def make_report(self):
        branch_office = self.first_frame_choise.combobox1_branch_office.get()
        structural_unit = self.first_frame_choise.combobox2_structural_unit.get()

        # Check if either combobox is empty
        if not branch_office.strip():
            CTkMessagebox(title="Ошибка", message="Выберите филиал!", icon="warning")
            return
        if not structural_unit.strip():
            CTkMessagebox(title="Ошибка", message="Выберите структурное подразделение!", icon="warning")
            return

        date_start_str = self.date_Start.get_current_date()
        date_end_str = self.date_End.get_current_date()

        # Check if either date is empty
        if not date_start_str.strip():
            CTkMessagebox(title="Ошибка", message="Выберите дату начала периода!", icon="warning")
            return
        if not date_end_str.strip():
            CTkMessagebox(title="Ошибка", message="Выберите дату конца периода!", icon="warning")
            return

        try:
            date_start = datetime.strptime(date_start_str, "%Y-%m-%d")
            date_end = datetime.strptime(date_end_str, "%Y-%m-%d")
        except ValueError as e:
            CTkMessagebox(title="Ошибка", message="Неверный формат даты!", icon="warning")
            return

        if self.second_frame_instance.compare_dates(date_start_str, date_end_str):
            diff = date_end - date_start
            if diff.days >= 0:
                print(branch_office)
                print(structural_unit)
                self.make_document()
            else:
                CTkMessagebox(title="Ошибка", message="Дата начала позже даты окончания.", icon="warning")
        else:
            CTkMessagebox(title="Ошибка", message="Дата начала позже даты окончания.", icon="warning")

    def make_document(self):
        date_start_str = self.date_Start.get_current_date()
        date_end_str = self.date_End.get_current_date()
        date_start = datetime.strptime(date_start_str, "%Y-%m-%d")
        date_end = datetime.strptime(date_end_str, "%Y-%m-%d")
        # Отчет по ремонтам за промежуток дат

        data = db_manager.exec_procedure("GetRepairsBetweenTwoDates", date_start, date_end,
                                         f"{self.first_frame_choise.combobox1_branch_office.get()}",
                                         f"{self.first_frame_choise.combobox2_structural_unit.get()}")
        print(data)
        # [('WS-FI01-101', '192.168.100.1', 'jhmgh', '2024-05-21', 'repairs\\ФИ-01\\Отдел первый\\Роутер\\2024-05-21_WS-FI01-101')]
        # сетевое имя
        # IP
        # Описание
        # Дата ремонта
        # Папка с документами
        # 5 столбцов

        root = tk.Tk()
        root.withdraw()  # Скрытие корневого окна
        file_path = filedialog.asksaveasfilename(defaultextension=".docx",
                                                 filetypes=[("Word Document", "*.docx")],
                                                 title="Выберите место сохранения документа",
                                                 initialfile="ОтчетПоРемонтам")

        if not file_path:
            return  # Прерывание функции, если пользователь не выбрал место сохранения

        doc = Document()
        title = doc.add_heading(
            f'Отчет по ремонтам устройств.\n Филиал - {self.first_frame_choise.combobox1_branch_office.get()} \n '
            f'Структурное подразделение - {self.first_frame_choise.combobox2_structural_unit.get()}', level=1)
        title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # Добавление таблицы с данными
        table = doc.add_table(rows=1, cols=5)
        table.style = 'Table Grid'
        # название, сетевое название, статус, дата,место установки
        # "('Рабочая станция', 'WS-FI05-120', 0, datetime.datetime(2024, 5, 8, 9, 21, 17, 350000), '2')"

        # Заголовки столбцов
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Сетевое имя'
        hdr_cells[1].text = 'IP'
        hdr_cells[2].text = 'Описание'
        hdr_cells[3].text = 'Дата ремонта'
        hdr_cells[4].text = 'Папка с документами'

        for item in data:
            row_cells = table.add_row().cells
            row_cells[0].text = str(item[0])  # Название
            row_cells[1].text = str(item[1])  # Сетевое имя
            row_cells[2].text = str(item[2])
            row_cells[3].text = str(item[3])  # Место установки
            row_cells[4].text = str(item[4])

        # Сохранение документа
        doc.save(file_path)


class ThirdFrameReport(customtkinter.CTkFrame):
    def __init__(self, master, first_frame_ch_instance, second_instance):
        super().__init__(master)
        self.first_frame_choise = first_frame_ch_instance
        self.second_frame_instance = second_instance
        self.configure(border_color="dodgerblue", border_width=3)
        customtkinter.CTkLabel(master=self, text="Отчет по выбранному устройству", fg_color="gray30",
                               font=("Arial", 14)).grid(row=0, columnspan=3, column=0, padx=10, pady=10, sticky="ew")
        customtkinter.CTkButton(master=self, text="Загрузить устройства",
                                command=lambda: self.load_devices_types()).grid(
            row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=3)

        customtkinter.CTkLabel(master=self, text="Выберите тип устройства").grid(
            row=2, column=0, padx=10, pady=10)

        self.type_of_device_combob = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly",
                                                               command=self.load_devices)
        self.type_of_device_combob.grid(row=2, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(master=self, text="Выберите устройство").grid(
            row=3, column=0, padx=10, pady=10)
        self.device_combob = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly")
        self.device_combob.grid(row=3, column=1, padx=10, pady=10)

        customtkinter.CTkButton(master=self, text="Сформировать отчёт",
                                command=lambda: self.make_report()).grid(
            row=4, column=0, padx=10, pady=10, sticky="ew", columnspan=3)

    def load_devices_types(self):
        branch_office = self.first_frame_choise.combobox1_branch_office.get()
        structural_unit = self.first_frame_choise.combobox2_structural_unit.get()
        # Check if either combobox is empty
        if not branch_office.strip():
            CTkMessagebox(title="Ошибка", message="Выберите филиал!", icon="warning")
            return
        if not structural_unit.strip():
            CTkMessagebox(title="Ошибка", message="Выберите структурное подразделение!", icon="warning")
            return
        try:
            id_branch = db_manager.get_data("branch_office", "id", f"name = '{branch_office}'")[0][0]
            id_unit = db_manager.get_data("structural_unit", "id", f"name = '{structural_unit}'")[0][0]
            data = db_manager.exec_procedure("GetUniqueDeviceNames", id_branch, id_unit)
            data = [str(row[0]) for row in data]
            self.type_of_device_combob.configure(values=data)
            self.update()
            CTkMessagebox(title="Успех", message="Типы устройств успешно загуржены", icon="check")
        except Exception as e:
            CTkMessagebox(title="Ошибка", message=f"Ошибка на этапе загрузки типов устройств!\n {e}", icon="warning")
    def load_devices(self, choice):
        print(choice)
        branch_office = self.first_frame_choise.combobox1_branch_office.get()
        structural_unit = self.first_frame_choise.combobox2_structural_unit.get()
        # Check if either combobox is empty
        if not branch_office.strip():
            CTkMessagebox(title="Ошибка", message="Выберите филиал!", icon="warning")
            return
        if not structural_unit.strip():
            CTkMessagebox(title="Ошибка", message="Выберите структурное подразделение!", icon="warning")
            return
        id_branch = db_manager.get_data("branch_office", "id", f"name = '{branch_office}'")[0][0]
        id_unit = db_manager.get_data("structural_unit", "id", f"name = '{structural_unit}'")[0][0]
        id_type_of_device = db_manager.get_data("type_of_device", "id", f"name = '{choice}'")[0][0]

        data = db_manager.exec_procedure("GetDeviceDetails", id_branch, id_unit, id_type_of_device)
        data = [str(row[0] + " | " + row[1]) for row in data]
        self.device_combob.configure(values=data)
        self.update()


    def make_report(self):
        branch_office = self.first_frame_choise.combobox1_branch_office.get()
        structural_unit = self.first_frame_choise.combobox2_structural_unit.get()
        type_of_device = self.type_of_device_combob.get()
        device = self.device_combob.get()
        parts = device.split('|')
        # Удаление лишних пробелов с каждой части
        ip_address = parts[0].strip()
        network_name = parts[1].strip()

        # Check if either combobox is empty
        if not branch_office.strip():
            CTkMessagebox(title="Ошибка", message="Выберите филиал!", icon="warning")
            return
        if not structural_unit.strip():
            CTkMessagebox(title="Ошибка", message="Выберите структурное подразделение!", icon="warning")
            return
        if not type_of_device.strip():
            CTkMessagebox(title="Ошибка", message="Выберите тип устройства!", icon="warning")
            return
        if not device.strip():
            CTkMessagebox(title="Ошибка", message="Выберите устройствo!", icon="warning")
            return
        root = tk.Tk()
        root.withdraw()  # Скрытие корневого окна
        file_path = filedialog.asksaveasfilename(defaultextension=".docx",
                                                 filetypes=[("Word Document", "*.docx")],
                                                 title="Выберите место сохранения документа",
                                                 initialfile="ОтчетПоРемонтам")

        if not file_path:
            return  # Прерывание функции, если пользователь не выбрал место сохранения

        data = db_manager.exec_procedure("GetDeviceInfoByBranchStrUnitTypeOfDeviceIpNetworkName",
                                         branch_office,structural_unit,type_of_device,ip_address,network_name)
        print(data)
        doc = DocxTemplate("resources\\pattern_for_third_report.docx")
        context = {
            'branch_office': data[0][0],
            'structural_unit': data[0][1],
            'inv_numb': data[0][2],
            'name': data[0][3],
            'network_name': data[0][4],
            'type_of_device': data[0][5],
            'location': data[0][6],
            'description_basic': data[0][7],
            'material_resp_person': data[0][8],
            'last_status': 'Вкл' if data[0][9] else 'Выкл',
            'last_repair': data[0][10] if data[0][10] is not None else '',
            'serial_numb': data[0][11],
            'mac_adr': data[0][12],
            'os': data[0][13],
            'year_of_pushare': data[0][14],
            'month_of_garanty': data[0][15],
            'processor': data[0][16],
            'ram': data[0][17],
            'motherboard': data[0][18],
            'graphicCard': data[0][19],
            'psu': data[0][20],
            'networkCard': data[0][21],
            'cooler': data[0][22],
            'chasis': data[0][23],
            'hdd': data[0][24],
            'ssd': data[0][25],
            'monitor': data[0][26],
            'keyboard': data[0][27],
            'mouse': data[0][28],
            'audio': data[0][29]
        }

        doc.render(context)
        doc.save(file_path)




if __name__ == "__main__":
    root = tkinter.Tk()
    app = Reports(root)
    root.mainloop()
