import customtkinter
import tkinter
import re

from CTkMessagebox import CTkMessagebox
from hPyT import *
from PIL import Image
import os
from tkcalendar import Calendar

from datetime import datetime, timedelta
import CTkSelectDate
from CTkSelectDate import *
from dataBase import DatabaseManager

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
        self.geometry("850x450")
        self.minsize(850, 450)
        self.frame = customtkinter.CTkFrame(self, height=490)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.fisrt = FirstFrameReport(self.frame)
        self.fisrt.grid(row=1, column=0, padx=10, pady=10, sticky="ew")


class FirstFrameReport(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure((0, 1), weight=1)
        self.configure(border_color="dodgerblue", border_width=3)
        customtkinter.CTkLabel(master=self, text="Отчет по статусам работы", fg_color="gray30",
                               font=("Arial", 14)).grid(row=0, columnspan=3, column=0, padx=10, pady=10, sticky="ew")
        self.date_Start = CTkSelectDate.SelectDate(self, label_text="Выберите дату начала периода")
        self.date_Start.grid(row=1, columnspan=2, column=0, padx=10, pady=10, sticky="ew")

        self.date_End = CTkSelectDate.SelectDate(self, label_text="Выберите дату конца периода")
        self.date_End.grid(row=2, columnspan=2, column=0, padx=10, pady=10, sticky="ew")

        self.MakeReport1Button = customtkinter.CTkButton(master=self, text="Сформировать и открыть отчет",
                                                         command=lambda: self.make_report())
        self.MakeReport1Button.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    def compare_dates(self, date1_str, date2_str):
        return datetime.strptime(date1_str, "%Y-%m-%d") <= datetime.strptime(date2_str, "%Y-%m-%d")

    def make_report(self):
        date_start_str = self.date_Start.get_current_date()
        date_end_str = self.date_End.get_current_date()

        date_start = datetime.strptime(date_start_str, "%Y-%m-%d")
        date_end = datetime.strptime(date_end_str, "%Y-%m-%d")

        if self.compare_dates(date_start_str, date_end_str):
            # Разница между датами
            diff = date_end - date_start
            if diff.days >= 0:

                data_for_report = db_manager.exec_procedure("GetBasicInfoStatusBetweenDates",date_start,date_end)
                data_for_report = [str(row) for row in data_for_report]
                #(72, 0, datetime.datetime(2024, 5, 7, 16, 4, 55, 350000), 'Рабочая станция', '1')

            else:
                print("Ошибка: Дата начала позже даты окончания.")
        else:
            print("Ошибка: Дата начала позже даты окончания.")

if __name__ == "__main__":
    root = tkinter.Tk()
    app = Reports(root)
    root.mainloop()
