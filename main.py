import concurrent.futures
import os
import sys
import threading
import subprocess
from datetime import datetime
from tkinter import messagebox
import pyodbc
import customtkinter as customtkinter
from CTkToolTip import *
from ctkcomponents import *
from hPyT import *
from PIL import Image
from addDevice import *
from editDevice import *
from PhotoViewer import *
from Repairs import *
from aioBranchOfficeStructuralUnit import *
from description import *
from import_from_excel import *
from report import *

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")






class UpperFrame(customtkinter.CTkFrame):
    """Класс для верхнего фрейма, содержащего кнопки и функциональность"""

    def __init__(self, master,db_manager=None):
        """Инициализация верхнего фрейма"""
        super().__init__(master)
        self.db_manager=db_manager
        self.toplevel_window = None  # Переменная для хранения ссылки на верхнеуровневое окно

        # Список с информацией о кнопках
        button_data = [
            {"text": "Добавить устройство", "command": self.AddPc},
            {"text": "Редактировать филиалы", "command": self.EditBranch},
            {"text": "Импорт из Excel", "command": self.ImportFromExcel},
            {"text": "Формирование отчетов", "command": self.ExportPc},
            {"text": "Ремонты", "command": self.Repairs, "fg_color": "#FF8C19", "hover_color": "#4DFFFF", "text_color": "black"},
            {"text":"БД", "command": self.OpenConnectionString,"width":30,"customTooltip":"Открыть файл с строкой подключения к БД."},
            {"text": "Справка", "command": self.OpenSpravka,"width":90,"customTooltip":"Справочная система приложения."}
        ]

        # Создание и размещение кнопок
        for idx, button_info in enumerate(button_data):
            button = customtkinter.CTkButton(master=self, text=button_info["text"],
                                             command=lambda command=button_info["command"]: command())
            CTkToolTip(button, message=button_info["text"])  # Всплывающая подсказка
            button.grid(row=0, column=idx, pady=10, padx=10)
            # Применение цветов к кнопкам, если они указаны
            if "fg_color" in button_info:
                button.configure(fg_color=button_info["fg_color"])
            if "hover_color" in button_info:
                button.configure(hover_color=button_info["hover_color"])
            if "text_color" in button_info:
                button.configure(text_color=button_info["text_color"])
            if "width" in button_info:
                button.configure(width=button_info["width"])
            if "customTooltip" in button_info:
                CTkToolTip(button, message=button_info["customTooltip"])

        # Кнопка для смены темы приложения
        self.AppearanceButton = customtkinter.CTkOptionMenu(
            self, values=["Тёмная", "Светлая"], command=self.change_appearance_mode_event)
        CTkToolTip(self.AppearanceButton, message="Смена темы приложения")
        self.AppearanceButton.grid(
            row=0, column=len(button_data), padx=20, pady=(10, 10))

    def change_appearance_mode_event(self,new_appearance_mode: str):
        """Метод для смены цветовой темы"""
        if new_appearance_mode == "Светлая":
            customtkinter.set_appearance_mode("Light")
        elif new_appearance_mode == "Тёмная":
            customtkinter.set_appearance_mode("Dark")

    def AddPc(self):
        """Открывает окно добавления устройства"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AddDevice_(self,db_manager=self.db_manager)
        else:
            self.toplevel_window.focus()

    def EditBranch(self):
        """Открывает окно редактирования филиалов"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AioBranchOfficeStructuralUnit(self,db_manager=self.db_manager)
        else:
            self.toplevel_window.focus()

    def Repairs(self):
        """Открывает окно ремонтов"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Repair(self,db_manager=self.db_manager)
        else:
            self.toplevel_window.focus()

    def ImportFromExcel(self):
        """Открывает окно импорта данных из Excel"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ImportDataFromExcel(self,db_manager=self.db_manager)
        else:
            self.toplevel_window.focus()

    def ExportPc(self):
        """Открывает окно экспорта данных"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Reports(self,db_manager=self.db_manager)
        else:
            self.toplevel_window.focus()
    def OpenConnectionString(self):
        """Открывает файл с cтрокой для подключения к базе данных"""
        os.startfile("resources\\database_info.txt")
    def OpenSpravka(self):
        """Открывает файл справки"""
        os.startfile("resources\\Справочная система приложения.pdf")



class MiddleFrame(customtkinter.CTkFrame):
    """Класс для среднего фрейма, содержащего элементы для выбора филиала и структурного подразделения."""

    def __init__(self, master, downframeInstance,db_manager=None):
        """Инициализация среднего фрейма."""
        super().__init__(master)
        self.db_manager = db_manager
        self.DownFrame = downframeInstance
        customtkinter.CTkLabel(master=self, text="Выберите филиал").grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        customtkinter.CTkLabel(master=self, text="Выберите структурное подразделение").grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        data = self.db_manager.get_data("branch_office", "name", "")
        data = [str(row[0]) for row in data]
        self.combobox1_branch_office = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly", command=self.load_data)
        self.combobox1_branch_office.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        CTkToolTip(self.combobox1_branch_office, message="Выберите филиал.")
        self.FillComboBox(self.combobox1_branch_office, data)

        self.combobox2_structural_unit = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly", command=self.load_main_data)
        self.combobox2_structural_unit.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        CTkToolTip(self.combobox2_structural_unit, message="Выберите структурное подразделение.")
        reload_data_button = customtkinter.CTkButton(master=self, text="Обновить", hover_color="green", command=lambda: self.reload_all())
        reload_data_button.grid(row=0, column=4, padx=10, pady=10, rowspan=2, sticky='nsew', columnspan=2)
        CTkToolTip(reload_data_button, message="Для обновления заново выберите нужный филиал и структурное подразделение.")

    def load_main_data(self, choice):
        """Загружает данные основной информации по выбранному филиалу и структурному подразделению."""
        self.DownFrame.clear_frame()

        branch_id = self.db_manager.get_data("branch_office", "id", f"name = '{self.combobox1_branch_office.get()}'")[0][0]
        structural_unit_id = self.db_manager.get_data("structural_unit", "id", f"name = '{choice}'")[0][0]
        result = self.db_manager.exec_procedure("GetInfoByBranchAndStructuralUnit", branch_id, structural_unit_id)
        str_data_for_tabs = list()
        for data in result:
            str_data_for_tabs.append(data)
        unique_cabinets = set()  # Создаем множество для хранения уникальных номеров кабинетов

        for row in result:
            unique_cabinets.add(row[5])  # Дёбавляем номер кабинета в множество
        unique_cabinets = sorted(unique_cabinets)
        self.tabview = customtkinter.CTkTabview(master=self.DownFrame)
        customtkinter.CTkLabel(master=self.DownFrame, text="Место установки").grid(row=0, column=0)
        self.tabview.grid(row=1, column=0)
        self.tabs = list()

        for cabinet_number in unique_cabinets:
            tab = self.tabview.add(cabinet_number)
            CTkToolTip(tab, message="Выбор места установки")
            self.tabs.append(tab)
        for tab in self.tabs:
            self.DownFrame.create_lables(tab)

        for cabinet_number in unique_cabinets:
            tab = self.tabview.tab(cabinet_number)  # Получаем вкладку по номеру кабинета
            for row in range(len(str_data_for_tabs)):
                getted_numb = str_data_for_tabs[row][5]
                if getted_numb == cabinet_number:  # Сравниваем номер кабинета с данными из результата запроса
                    data = str_data_for_tabs[row]
                    self.DownFrame.create_str(tab, data, row)

    def reload_all(self):
        """Обновляет данные в комбо-боксах и нижнем фрейме."""
        try:
            data = self.db_manager.get_data("branch_office", "name", "")
            data = [str(row[0]) for row in data]
            self.FillComboBox(self.combobox1_branch_office, data)
        except Exception as e:
            CTkMessagebox(title="Ошибка", message=f"Произошла ошбика при обновлении филиалов и структурных подразделений!\n{e}", icon="warning")
            return 0
        try:

            branch_id = self.db_manager.get_data("branch_office", "id", f"name = '{self.combobox1_branch_office.get()}'")[0][0]
            structural_unit_id = self.db_manager.get_data("structural_unit", "id", f"name = '{self.combobox2_structural_unit.get()}'")[0][0]
            result = self.db_manager.exec_procedure("GetInfoByBranchAndStructuralUnit", branch_id, structural_unit_id)
            all_ips = list()
            for row in result:
                all_ips.append(row[1])
            self.check_connections(all_ips)
            CTkMessagebox(title="Успех", message="Статусы успешно обновлены! \nДля обновления заново выберите нужный филиал и структурное подразделение.",
                          icon="info")
        except Exception as e:
            CTkMessagebox(title="Ошибка", message=f"Произошла ошбика при обновлении статусов!\n{e}", icon="warning")
            return 0

    def FillComboBox(self, combobox, data_):
        """Заполняет комбо-бокс данными."""
        data__ = [str(data) for data in data_]
        combobox.configure(values=data__)
        self.update()

    def load_data(self, choice):
        """Загружает данные о структурных подразделениях для выбранного филиала."""
        data = self.db_manager.exec_procedure("GetStructuralUnits", choice)
        data = [str(row[0]) for row in data]
        self.FillComboBox(self.combobox2_structural_unit, data)

    def check_connection(self, ip):
        """
                Метод для проверки соединения с указанным IP-адресом.

                Параметры:
                ip (строка): IP-адрес для проверки соединения.

                Возвращает:
                bool: True, если удалось установить соединение с указанным IP, иначе False.
                """
        try:
            ping_file = f"ping_{ip}.txt"
            os.system(f'ping -n 1 {ip} > "{ping_file}"')
            with open(ping_file, 'r', encoding='cp866') as file:
                ping = file.read()

            if f"Ответ от {ip}:" in ping:
                self.db_manager.add_status(ip, True)
                # print(f"{ip}")
                os.remove(ping_file)
                return True
            else:
                # print(f"Устройство с IP {ip} не доступно.")
                self.db_manager.add_status(ip, False)
                os.remove(ping_file)
                return False
        except Exception as e:
            # print(f"Error: {e}")
            return False

    def check_connections(self, ip_list):
        """
        Проверяет доступность списка IP-адресов с использованием многопоточности.

        Аргументы:
        ip_list (list): Список IP-адресов для проверки.

        Возвращает:
        None
        """
        ip_list.insert(0, "1.1.1.1")
        print(ip_list)
        # Создание пула потоков
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Запуск задач для каждого IP-адреса
            future_to_ip = {executor.submit(self.check_connection, ip): ip for ip in ip_list}
            # Ожидание завершения задач
            for future in concurrent.futures.as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    # Получение результата задачи (если есть)
                    result = future.result()

                except Exception as e:
                    print(f"Task for IP {ip} encountered an error: {e}")


class DownFrame(customtkinter.CTkScrollableFrame):
    """"Класс для нижнего фрейма, содержащего информацию о устройствах."""
    def __init__(self, master,db_manager=None):
        """Инициализация нижнего фрейма."""
        super().__init__(master)
        self.db_manager = db_manager
        self.toplevel_window = None
        self.grid_columnconfigure(0, weight=1)

    def create_lables(self, tab):
        """Создание меток для отображения заголовков столбцов."""
        labels_text = ["Ip", "Название", "Название в сети", "Тип устройства", "Место установки", "Мат. отв.", "Описание", "Фото",
                       "Статус", "Последний ремонт", "VNC", "Редактировать"]
        for idx, text in enumerate(labels_text):
            tab.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)
            label = customtkinter.CTkLabel(master=tab, text=text, font=("Arial", 14))
            label.grid(row=0, column=idx, padx=10, pady=10, sticky="ew")

    def create_str(self, tab, data, row):
        """Создание строки с данными об устройстве."""

        def run_vnc_exe(ip_address):
            """Запуск VNC"""
            subprocess.run(["resources\\VNC.exe", ip_address])

        data_with_id = data
        data = data[1:]

        for index, item in enumerate(data):
            if index < 6:
                customtkinter.CTkLabel(master=tab, text=item, font=("Arial", 12)).grid(row=row + 2, column=index,
                                                                                       padx=10, pady=10)

        customtkinter.CTkButton(master=tab, text="Описание", width=85,
                                command=lambda: self.description_open(data_with_id[0])).grid(row=row + 2, column=6,
                                                                                             pady=10, padx=10)
        customtkinter.CTkButton(master=tab, text="Фото", width=75,
                                command=lambda: self.photo_open(data_with_id[0])).grid(row=row + 2, column=7, pady=10,
                                                                                       padx=10)
        customtkinter.CTkButton(master=tab, text="VNC", width=55,
                                command=lambda: threading.Thread(target=run_vnc_exe, args=(data[0],)).start()).grid(
            row=row + 2, column=10, pady=10, padx=10)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        customtkinter.CTkButton(master=tab, text="", image=customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "resources\\edit_ico.png")), size=(20, 20)), width=30,
                                command=lambda: self.edit_pc(data_with_id[0])).grid(row=row + 2, column=11, pady=10,
                                                                                    padx=10)

        if data[8] is None:
            customtkinter.CTkLabel(master=tab, text="-------").grid(row=row + 2, column=9, padx=10, pady=10)
        else:
            try:
                date_str = data[8]
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d.%m.%Y")
            except Exception as e:
                print(f"Ошибка при преобразовании даты: {e}")
                formatted_date = date_str  # На случай ошибки, оставим исходную дату

            customtkinter.CTkLabel(master=tab, text=formatted_date, font=("Arial", 12)).grid(row=row + 2, column=9,
                                                                                             padx=10, pady=10)

        if data[6] == 0:
            customtkinter.CTkLabel(master=tab, text="          ", bg_color="red").grid(row=row + 2, column=8, padx=10,
                                                                                       pady=10)
        else:
            customtkinter.CTkLabel(master=tab, text="          ", bg_color="green").grid(row=row + 2, column=8, padx=10,
                                                                                         pady=10)
    def clear_frame(self):
        """Удаление всех виджетов из фрейма."""
        # Уничтожаем все дочерние виджеты фрейма
        for widget in self.winfo_children():
            widget.destroy()

    def edit_pc(self, bas):
        """Метод для открытия окна редактирования устройства"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = EditDevice_(self, basic_id=bas,db_manager=self.db_manager)
        else:
            self.toplevel_window.focus()

    def description_open(self, bas):
        """Метод для открытия окна описания устройства"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = DescriptionViewer(self, basic_id=bas,db_manager=self.db_manager)
        else:
            self.toplevel_window.focus()

    def photo_open(self, bas):
        """Метод для открытия окна фотографий."""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = PhotoViewer(self, basic_id=bas,db_manager=self.db_manager)
        else:
            self.toplevel_window.focus()


class FrameConn(customtkinter.CTkFrame):
    def __init__(self, *args,method=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.meth=method
        # Создаем лейблы и привязываем их к соответствующим полям ввода
        label1 = customtkinter.CTkLabel(self, text="Имя сервера:")
        label1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry1 = customtkinter.CTkEntry(self, placeholder_text="Введите Server Name")
        self.entry1.grid(row=0, column=1, padx=10, pady=5)

        label2 = customtkinter.CTkLabel(self, text="Имя базы данных:")
        label2.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry2 = customtkinter.CTkEntry(self, placeholder_text="Введите Database Name")
        self.entry2.grid(row=1, column=1, padx=10, pady=5)

        self.button = customtkinter.CTkButton(self, text="Принять", command=self.handle_button_click)
        self.button.grid(row=2, column=1,  padx=10, pady=5)

        customtkinter.CTkButton(self, text="Справка", command=self.open_help).grid(row=2, column=0,  padx=10, pady=5)

    def open_help(self):
        """Открывает файл справки"""
        os.startfile("resources\\Справочная система приложения.pdf")
    def handle_button_click(self):
        # Получаем введенные значения
        server_name = self.entry1.get()
        database_name = self.entry2.get()


        # Пытаемся подключиться к базе данных
        try:
            conn = pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};Trusted_Connection=yes;'
            )
            # Если подключение успешно, записываем данные в файл
            with open('resources/database_info.txt', 'w') as file:
                file.write(f"{server_name}, {database_name}")
            # Закрываем соединение
            conn.close()
            print("Successfully connected to the database and wrote to file.")
            self.success_("Подключение успешно создано! Пожалуйста, перезапустите приложение!","Успех","check")

        except pyodbc.Error as e:
            # Если произошла ошибка подключения, выводим сообщение
            print(f"Failed to connect to the database: {e}")
            CTkMessagebox(title="Ошибка", message=f"Не удалось подключится к базе данныйх! :(\n{e}", icon="cancel")


    def success_(self, message_,title_,icon_):
        """Метод для закрытия окна при нажатии кнопки "ОК"\
            :arg message_ - сообщение для показа в messagebox
        """
        # get yes/no answers
        msg = CTkMessagebox(title=title_, cancel_button=None, message=message_, icon=icon_, option_1="Ok")
        response = msg.get()

        if response == "Ok":
            self.destroy()
            self.meth()
        else:
            pass


class App(customtkinter.CTk):
    """Класс приложения"""
    WIDTH = 1610
    HEIGHT = 500

    def __init__(self):
        """Инициализация главного окна приложения."""
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.db_manager = None


        # Создаем файл с информацией о базе данных, если его нет
        self.create_database_info_file()

        # Читаем информацию о базе данных из файла
        database_info_path = self.resource_path('resources/database_info.txt')
        db_info = self.read_database_info_file()

        # Разделение информации для подключения
        db_info_parts = db_info.split(', ')
        try:
            # Пытаемся подключиться к базе данных и создать таблицы
            self.db_manager = DatabaseManager(db_info_parts[0], db_info_parts[1])
            if self.db_manager is not None:
                self.db_manager.create_tables()
            else:
                self.db_manager=None
                print("Failed to create DatabaseManager object.")
                # Возможно, здесь нужно показать пользователю сообщение об ошибке
        except Exception as e:
            # Обрабатываем ошибку подключения к базе данных
            print(f"Failed to connect to the database: {e}")
            # Здесь можно добавить код для вывода окна с сообщением об ошибке, например:
            CTkMessagebox(title="Ошибка",
                          message=f"Не удалось подключиться к базе данных!\n{e}",
                          icon="warning")
            self.title("Подключение к БД")
            self.frame_conn = FrameConn(self,method=self.close)
            self.frame_conn.grid(row=0,column=0, padx=10, pady=10, sticky="nsew")
        else:
            self.title("ddAdmin")
            self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
            self.minsize(1300, 300)
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure((1), weight=0)
            self.grid_rowconfigure(2, weight=1)
            # Создание и размещение фреймов
            self.frame_down = DownFrame(self,db_manager=self.db_manager)
            self.frame_down.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

            self.frame_middle = MiddleFrame(self, self.frame_down, db_manager =self.db_manager)
            self.frame_middle.grid(row=1, column=0, padx=10, pady=10)

            self.frame_up = UpperFrame(self,self.db_manager)
            self.frame_up.grid(row=0, column=0, padx=10, pady=10)

    def on_closing(self):
        """Обработчик события закрытия приложения."""
        if messagebox.askokcancel("Выйти", "Вы хотите закрыть приложение?"):
            if self.db_manager is not None and self.db_manager.conn is not None:
                self.db_manager.close_connection()  # Закрываем соединение с базой данных
            self.destroy()
    def close(self):
        self.destroy()

    def create_database_info_file(self):
        filepath = 'resources/database_info.txt'
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as file:
                file.write('DDZEN\\SQLEXPRESS, PCC')

    def read_database_info_file(self):
        filepath = 'resources/database_info.txt'
        with open(filepath, 'r') as file:
            db_info = file.read().strip()
        return db_info

    def resource_path(self,relative_path):
        """ Получить абсолютный путь к ресурсу, работает для разработки и для PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    app = App()
    app.mainloop()
