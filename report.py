import customtkinter
import tkinter
import re

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
        self.geometry("850x650")
        self.minsize(850, 650)
        self.frame = customtkinter.CTkFrame(self, height=490)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.first = FirstFrameChoise(self.frame)
        self.first.grid(row=0, column=0, padx=10, pady=10, sticky="")

        # Отчет по статусам работы  - готово
        self.second = FirstFrameReport(self.frame, self.first)
        self.second.grid(row=1, column=0, padx=10, pady=10, sticky="")



        # Отчет по ремонтам за промежуток дат
        # Отчет на выбранное устройство
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
        date_start_str = self.date_Start.get_current_date()
        date_end_str = self.date_End.get_current_date()

        date_start = datetime.strptime(date_start_str, "%Y-%m-%d")
        date_end = datetime.strptime(date_end_str, "%Y-%m-%d")

        if self.compare_dates(date_start_str, date_end_str):

            diff = date_end - date_start
            if diff.days >= 0:
                print(self.first_frame_choise.combobox1_branch_office.get())
                print(self.first_frame_choise.combobox2_structural_unit.get())
                data_for_report = db_manager.exec_procedure("GetBasicInfoStatusBetweenDatesInBranchAndStructUnit",
                                                            date_start, date_end,
                                                            f"{self.first_frame_choise.combobox1_branch_office.get()}",
                                                            f"{self.first_frame_choise.combobox2_structural_unit.get()}")

                print(data_for_report)
                self.make_document(data_for_report)

            else:
                print("Ошибка: Дата начала позже даты окончания.")
        else:
            print("Ошибка: Дата начала позже даты окончания.")

    def make_document(self, data):
        print(data)
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


if __name__ == "__main__":
    root = tkinter.Tk()
    app = Reports(root)
    root.mainloop()
