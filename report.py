import customtkinter
import tkinter
import re

from CTkMessagebox import CTkMessagebox
from hPyT import *
from PIL import Image
import os
from tkcalendar import Calendar
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from datetime import datetime
from docxtpl import DocxTemplate

from dataBase import DatabaseManager

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
        label_file = customtkinter.CTkLabel(master=self.frame, text="В разработке!")
        label_file.grid(row=1, column=0, pady=10, padx=10, sticky="ew")




if __name__ == "__main__":
    root = tkinter.Tk()
    app = Reports(root)
    root.mainloop()