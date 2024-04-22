import concurrent.futures

import os
import threading
import subprocess
import time
from tkinter import messagebox
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


def change_appearance_mode_event(new_appearance_mode: str):
    """Метод для смены цветовой темы"""
    if new_appearance_mode == "Светлая":
        customtkinter.set_appearance_mode("Light")
    elif new_appearance_mode == "Тёмная":
        customtkinter.set_appearance_mode("Dark")


class UpperFrame(customtkinter.CTkFrame):
    """Класс для верхнего фрейма"""

    def __init__(self, master):
        """Конструктор класса"""
        super().__init__(master)

        self.toplevel_window = None

        button_data = [
            {"text": "Добавить устройство", "command": self.AddPc},
            {"text": "Редактировать филиалы", "command": self.EditBranch},
            {"text": "Формирование отчетов", "command": self.ExportPc},
            {"text": "Ремонты", "command": self.Repairs, "fg_color": "#FF8C19", "hover_color": "#4DFFFF", "text_color": "black"}
        ]

        for idx, button_info in enumerate(button_data):
            button = customtkinter.CTkButton(master=self, text=button_info["text"],
                                             command=lambda command=button_info["command"]: command())
            CTkToolTip(button, message=button_info["text"])
            button.grid(row=0, column=idx, pady=10, padx=10)
            if "fg_color" in button_info:
                button.configure(fg_color=button_info["fg_color"])
            if "hover_color" in button_info:
                button.configure(hover_color=button_info["hover_color"])
            if "text_color" in button_info:
                button.configure(text_color=button_info["text_color"])

        self.AppearanceButton = customtkinter.CTkOptionMenu(
            self, values=["Тёмная", "Светлая"], command=change_appearance_mode_event)
        CTkToolTip(self.AppearanceButton, message="Смена темы приложения")
        self.AppearanceButton.grid(
            row=0, column=len(button_data), padx=20, pady=(10, 10))

    def AddPc(self):
        """Метод для открытия окна добавления устройства"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AddDevice_(self)
        else:
            self.toplevel_window.focus()

    def EditBranch(self):
        """Метод для открытия окна редактирования филиалов"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AioBranchOfficeStructuralUnit(self)
        else:
            self.toplevel_window.focus()

    def Repairs(self):
        """Метод для открытия окна ремонтов"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():

            self.toplevel_window = Repair(self)
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

    def __init__(self, master, downframeInstance):
        super().__init__(master)

        self.DownFrame = downframeInstance
        customtkinter.CTkLabel(master=self, text="Выберите филиал").grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        customtkinter.CTkLabel(master=self, text="Выберите структурное подразделение").grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        data = db_manager.get_data("branch_office", "name", "")
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
        self.DownFrame.clear_frame()

        branch_id = db_manager.get_data("branch_office", "id", f"name = '{self.combobox1_branch_office.get()}'")[0][0]
        structural_unit_id = db_manager.get_data("structural_unit", "id", f"name = '{choice}'")[0][0]
        result = db_manager.exec_procedure("GetInfoByBranchAndStructuralUnit", branch_id, structural_unit_id)
        str_data_for_tabs = list()
        for data in result:
            str_data_for_tabs.append(data)
        unique_cabinets = set()  # Создаем множество для хранения уникальных номеров кабинетов

        for row in result:
            unique_cabinets.add(row[5])  # Добавляем номер кабинета в множество
        unique_cabinets = sorted(unique_cabinets)
        self.tabview = customtkinter.CTkTabview(master=self.DownFrame)
        self.tabview.grid(row=0, column=0)
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
        try:
            branch_id = db_manager.get_data("branch_office", "id", f"name = '{self.combobox1_branch_office.get()}'")[0][0]
            structural_unit_id = db_manager.get_data("structural_unit", "id", f"name = '{self.combobox2_structural_unit.get()}'")[0][0]
            result = db_manager.exec_procedure("GetInfoByBranchAndStructuralUnit", branch_id, structural_unit_id)
            all_ips = list()
            for row in result:
                all_ips.append(row[1])
            self.check_connections(all_ips)
            CTkMessagebox(title="Успех", message="Статусы успешно обновлены! \nДля обновления заново выберите нужный филиал и структурное подразделение.",
                          icon="info")
        except Exception as e:
            CTkMessagebox(title="Ошибка", message=f"Произошла ошбика!\n{e}", icon="warning")
            return 0

    def FillComboBox(self, combobox, data_):
        data__ = [str(data) for data in data_]
        combobox.configure(values=data__)
        self.update()

    def load_data(self, choice):
        data = db_manager.exec_procedure("GetStructuralUnits", choice)
        data = [str(row[0]) for row in data]
        self.FillComboBox(self.combobox2_structural_unit, data)

    def check_connection(self, ip):
        try:
            ping_file = f"ping_{ip}.txt"
            os.system(f'ping -n 1 {ip} > "{ping_file}"')
            with open(ping_file, 'r', encoding='cp866') as file:
                ping = file.read()

            if f"Ответ от {ip}:" in ping:
                db_manager.add_status(ip, True)
                # print(f"{ip}")
                os.remove(ping_file)
                return True
            else:
                # print(f"Устройство с IP {ip} не доступно.")
                db_manager.add_status(ip, False)
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
    """"Класс для нижнего фрейма"""

    def __init__(self, master):
        super().__init__(master)
        self.toplevel_window = None
        self.grid_columnconfigure(0, weight=1)

    def create_lables(self, tab):
        labels_text = ["Ip", "Название", "Название в сети", "Тип устройства", "Место установки", "Мат. отв.", "Описание", "Фото",
                       "Статус", "Последний ремонт", "VNC", "Редактировать"]
        for idx, text in enumerate(labels_text):
            tab.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)
            label = customtkinter.CTkLabel(master=tab, text=text, font=("Arial", 14))
            label.grid(row=0, column=idx, padx=10, pady=10, sticky="ew")

    def create_str(self, tab, data, row):
        def run_vnc_exe(ip_address):
            subprocess.run(["resources\\VNC.exe", ip_address])

        data_with_id = data
        data = data[1:]

        for index, item in enumerate(data):
            if index < 6:
                customtkinter.CTkLabel(master=tab, text=item, font=("Arial", 12)).grid(row=row + 2, column=index, padx=10, pady=10)

        customtkinter.CTkButton(master=tab, text="Описание", width=85, command=lambda: self.description_open(data_with_id[0])).grid(row=row + 2, column=6, pady=10,
                                                                                                                                    padx=10)

        customtkinter.CTkButton(master=tab, text="Фото", width=75, command=lambda: self.photo_open(data_with_id[0])).grid(row=row + 2, column=7, pady=10, padx=10)

        customtkinter.CTkButton(master=tab, text="VNC", width=55, command=lambda: threading.Thread(target=run_vnc_exe, args=(data[0],)).start()).grid(row=row + 2,
                                                                                                                                                      column=10,
                                                                                                                                                      pady=10,
                                                                                                                                                      padx=10)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        customtkinter.CTkButton(master=tab, text="", image=customtkinter.CTkImage(Image.open(os.path.join(image_path, "resources\\edit_ico.png")), size=(20, 20)),
                                width=30, command=lambda: self.edit_pc(data_with_id[0])).grid(row=row + 2, column=11, pady=10, padx=10)

        if data[8] == None:
            customtkinter.CTkLabel(master=tab, text="-------", ).grid(row=row + 2, column=9, padx=10, pady=10)
        if data[6] == 0:
            customtkinter.CTkLabel(master=tab, text="          ", bg_color="red").grid(row=row + 2, column=8, padx=10, pady=10)
        else:
            customtkinter.CTkLabel(master=tab, text="          ", bg_color="green").grid(row=row + 2, column=8, padx=10, pady=10)
        customtkinter.CTkLabel(master=tab, text=data[8], font=("Arial", 12)).grid(row=row + 2, column=9, padx=10, pady=10)

    def clear_frame(self):
        # Уничтожаем все дочерние виджеты фрейма
        for widget in self.winfo_children():
            widget.destroy()

    def edit_pc(self, bas):

        """Метод для открытия окна редактирования устройства"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = EditDevice_(self, basic_id=bas)
        else:
            self.toplevel_window.focus()

    def description_open(self, bas):
        """Метод для открытия окна описания устройства"""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = DescriptionViewer(self, basic_id=bas)
        else:
            self.toplevel_window.focus()

    def photo_open(self, bas):
        """Метод для открытия окна фотографий."""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = PhotoViewer(self, basic_id=bas)
        else:
            self.toplevel_window.focus()


class App(customtkinter.CTk):
    """Класс приложения"""
    WIDTH = 1610
    HEIGHT = 500

    def __init__(self):
        """Инициализация главного окна приложения."""
        super().__init__()

        self.title("ddAdmin")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1), weight=0)

        self.grid_rowconfigure(2, weight=1)
        self.frame_down = DownFrame(self)
        self.frame_down.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")


        self.frame_middle = MiddleFrame(self, self.frame_down)
        self.frame_middle.grid(row=1, column=0, padx=10, pady=10)
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
