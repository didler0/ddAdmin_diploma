import os
import tkinter
import shutil
from tkinter import filedialog

import customtkinter
from PIL import Image
from hPyT import maximize_minimize_button
from tkcalendar import Calendar
from dataBase import DatabaseManager
from CTkToolTip import *
import pandas as pd
from CTkMessagebox import CTkMessagebox




class ImportDataFromExcel(customtkinter.CTkToplevel):
    """Класс для реализации функциональности импорта данных из Excel в базу данных."""
    def __init__(self, *args,db_manager=None, **kwargs):
        """Инициализация класса и создание окна."""
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.create_window()
        self.file_path = pd.DataFrame

    def create_window(self):
        """
        Создание окна Импорта из Excel.
        """
        self.title("Импорт из Excel")
        self.geometry("600x220")
        self.minsize(600, 220)

        self.frame = customtkinter.CTkFrame(self, height=490)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        load_file_button = customtkinter.CTkButton(master=self.frame, text="Выбрать файл", hover_color="green", command=lambda: self.load_excel())
        load_file_button.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        self.label_file = customtkinter.CTkLabel(master=self.frame, text="Файл не выбран!")
        self.label_file.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        insert_into_db_button = customtkinter.CTkButton(master=self.frame, text="Загрузить в базу данных", hover_color="red",
                                                        command=lambda: self.insert_into_db())
        insert_into_db_button.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

        open_right_formatButton = customtkinter.CTkButton(master=self.frame, text="Открыть пример верного формата файла", hover_color="green",
                                                          command=lambda: self.open_excel())
        open_right_formatButton.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

    def open_excel(self):
        """Открытие копии файла примера"""
        # Путь к исходному файлу Excel
        source_file = 'resources\\excel_import_exsample.xlsx'
        # Путь к копии файла Excel
        copy_file = 'resources\\excel_import_exsample_copy.xlsx'
        try:
            # Копируем исходный файл в копию
            shutil.copyfile(source_file, copy_file)

            # Открываем копию файла
            os.startfile(copy_file)

            print("Файл успешно открыт.")
        except Exception as e:
            print(f"Ошибка при открытии файла: {e}")

    def load_excel(self):
        """Добавляет новый файл Excel."""
        try:
            file_path = filedialog.askopenfilename(
                title="Выберите файл Excel",
                filetypes=[("Файлы Excel", "*.xlsx;*.xls")]
            )
            if file_path:
                # Чтение данных из файла Excel
                df = pd.read_excel(file_path)
                required_columns = [
                    "Филиал", "Структурное подразделение", "№ кабинета", "Тип устройства", "Материально ответственное лицо",
                    "ip", "Название", "Сетевое название", "Описание", "Инвентарный номер", "Серийный номер", "MAC адрес",
                    "Операционная система", "Год выпуска/дата покупки", "Гарантия, мес.", "Процессор", "ОЗУ", "Материнская плата",
                    "Видеокарта", "Блок питания", "Сетевая карта", "Куллер", "Корпус", "ХДД", "ССД", "Монитор", "Мышь", "Клавиатура"
                ]
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    missing_columns_message = "\n".join(missing_columns)
                    CTkMessagebox(title="Отсутствующие столбцы", message=f"Файл не загружен! \n Отсутствующие столбцы в файле Excel:\n{missing_columns_message}",
                                  icon="warning")
                    return 0
                else:
                    self.file_path = df
                    CTkMessagebox(title="Успех", message="Все требуемые столбцы присутствуют в файле Excel.", icon="info")
                    CTkMessagebox(title="Успех", message="Файл успешно открыт!", icon="check", option_1="Ok")
                    self.label_file.configure(text=f"Выбран файл - {file_path}")
        except Exception as e:
            CTkMessagebox(title="Ошибка", message="Ошибка при чтении файла!\nВозможно файл имеет неверный формат.\nОзнакомьтесь с верным форматом!", icon="cancel")

    def insert_into_db(self):
        """Метод для вставки данных в БД"""
        try:
            type_of_device = self.file_path['Тип устройства'].unique()
            fillial = self.file_path['Филиал'].unique()
            structural_unit = self.file_path['Структурное подразделение'].unique()
            mater_face = self.file_path['Материально ответственное лицо'].unique()
            place_of_install = self.file_path['№ кабинета'].unique()
            for device in type_of_device:
                self.db_manager.insert_data("type_of_device", "name", f"'{device}'")
            for branch_office in fillial:
                self.db_manager.insert_data("branch_office", "name", f"'{branch_office}'")
            for structural_unit_ in structural_unit:
                self.db_manager.insert_data("structural_unit", "name", f"'{structural_unit_}'")
            for mat_face in mater_face:
                self.db_manager.insert_data("material_resp_person", "name", f"'{mat_face}'")
            for place_of_installation in place_of_install:
                self.db_manager.insert_data("place_of_installation", "name", f"'{place_of_installation}'")
            df = self.file_path.values.tolist()
            for item in df:
                # Получение идентификаторов филиала и структурного подразделения
                id_branch = self.db_manager.get_data("branch_office", "id", f"name = '{item[0]}'")[0][0]
                id_unit = self.db_manager.get_data("structural_unit", "id", f"name = '{item[1]}'")[0][0]

                # Проверка наличия сочетания филиала и структурного подразделения в базе данных
                existing_record = self.db_manager.get_data("branch_structural_unit", "*", f"branch_office_id = '{id_branch}' AND structural_unit_id = '{id_unit}'")
                if not existing_record:
                    # Если сочетание не существует, вставляем новые данные
                    self.db_manager.insert_data("branch_structural_unit", "branch_office_id, structural_unit_id", f"'{id_branch}', '{id_unit}'")
                # Составление списка данных для вставки в таблицу basic_info
                list_basic_info = [
                    item[5], item[6], item[7],
                    self.db_manager.get_data("type_of_device", "id", f"name = '{item[3]}'")[0][0],
                    self.db_manager.get_data("place_of_installation", "id", f"name = '{item[2]}'")[0][0],
                    item[8],
                    self.db_manager.get_data("material_resp_person", "id", f"name = '{item[4]}'")[0][0],
                    id_branch,
                    id_unit
                ]
                # Составление списка данных для вставки в таблицу detail_info
                list_detail_info = item[9:15]
                # Составление списка данных для вставки в таблицу component
                list_component = item[15:]
                # Вставка данных в таблицы в порядке: component, detail_info, basic_info
                self.db_manager.insert_data_component(*list_component)
                last_component_id = self.db_manager.get_last_id("component")
                list_detail_info.insert(0, last_component_id)
                self.db_manager.insert_data_detail_info(*list_detail_info)

                last_details_id = self.db_manager.get_last_id("detail_info")
                list_basic_info.append(last_details_id)
                self.db_manager.insert_data_basic_info(*list_basic_info)

            CTkMessagebox(title="Успех", message="Данные успешно добавлены в базу данных!", icon="check", option_1="Ok")

        except IndexError:
            CTkMessagebox(title="Ошибка", message="Ошибка при обработке данных: индекс за пределами диапазона.", icon="cancel")
        except ValueError as ve:
            CTkMessagebox(title="Ошибка", message=f"Ошибка при обработке данных: {ve}", icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Ошибка", message=f"Ошибка при обработке данных: {e}", icon="cancel")


if __name__ == "__main__":
    app = ImportDataFromExcel()
    app.mainloop()
