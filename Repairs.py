from datetime import datetime
import os
import tkinter
import shutil
import customtkinter
from PIL import Image
from hPyT import maximize_minimize_button
from tkcalendar import Calendar
from dataBase import DatabaseManager
from CTkToolTip import *

from CTkMessagebox import CTkMessagebox



class Repair(customtkinter.CTkToplevel):
    """
    Класс для создания окна управления ремонтами.

    Attributes:
        second (customtkinter.CTkFrame): Фрейм для второй части окна.
        last (customtkinter.CTkFrame): Фрейм для последней части окна.
        first (customtkinter.CTkFrame): Фрейм для первой части окна.

    Methods:
        __init__: Инициализация объекта Repair.
        create_window: Создание и настройка окна ремонтов.
    """

    def __init__(self, *args, db_manager=None, **kwargs):
        """
        Инициализирует объект Repair.

        Args:
            *args: Позиционные аргументы.
            **kwargs: Именованные аргументы.
        """
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager

        self.second = customtkinter.CTkFrame
        self.last = customtkinter.CTkFrame
        self.first = customtkinter.CTkFrame
        self.create_window()

    def create_window(self):
        """
        Создает и настраивает окно Ремонтов.
        """
        self.title("Ремонты")
        self.geometry("600x650")
        self.minsize(600, 650)
        self.maxsize(600,650)

        self.frame = customtkinter.CTkFrame(self, height=490)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.second = SecondFrame(self.frame, db_manager=self.db_manager)
        self.second.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.first = FirstFrame(self.frame, self.second, db_manager=self.db_manager)
        self.first.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.last = ThirdFrame(self.frame, self.second, self.first, db_manager=self.db_manager)
        self.last.grid(row=2, column=0, padx=10, pady=10, sticky="ew")


class SecondFrame(customtkinter.CTkFrame):
    """
    Класс для создания и управления второй частью окна управления ремонтами.

    Attributes:
        combobox1_repair (customtkinter.CTkComboBox): Комбобокс для выбора ремонта.
        DecriptiontextBox (customtkinter.CTkTextbox): Поле для ввода описания ремонта.
        DataOfRepaor_entry (customtkinter.CTkEntry): Поле для ввода даты ремонта.
        CalendarOpenButton (customtkinter.CTkButton): Кнопка для открытия календаря выбора даты.
        OpenFolderRepairButton (customtkinter.CTkButton): Кнопка для открытия папки с документами ремонта.

    Methods:
        clear_whole_data: Очищает все данные в элементах интерфейса.
        open_folder: Открывает папку с документами выбранного ремонта.
        load_repair: Загружает информацию о выбранном ремонте.
        select_date: Открывает календарь для выбора даты ремонта.
    """
    def __init__(self, *args, db_manager=None, **kwargs):
        """
                Инициализирует объект SecondFrame.

                Args:
                    *args: Позиционные аргументы.
                    db_manager: экземпляр коннекта
                    **kwargs: Именованные аргументы.
                """
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.grid_columnconfigure((0, 1), weight=1)
        self.configure(border_color="dodgerblue", border_width=3)
        customtkinter.CTkLabel(master=self, text="Ремонты", fg_color="gray30", font=("Arial", 14)).grid(row=0, columnspan=3, column=0, padx=10, pady=10, sticky="ew")

        self.combobox1_repair = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly", command=self.load_repair)
        self.combobox1_repair.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        CTkToolTip(self.combobox1_repair, message="Выберите ремонт. Для обновления заново выберите устройство!")

        customtkinter.CTkLabel(master=self, text="Описание").grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.DecriptiontextBox = customtkinter.CTkTextbox(master=self, height=90)
        self.DecriptiontextBox.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="ew")
        CTkToolTip(self.DecriptiontextBox, message="Введите описание")

        customtkinter.CTkLabel(master=self, text="Дата ремонта").grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.DataOfRepaor_entry = customtkinter.CTkEntry(master=self, placeholder_text="ДД-ММ-ГГГГ")
        self.DataOfRepaor_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        CTkToolTip(self.DataOfRepaor_entry, message="Введите дату ремонта")

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "resources\\calendarICO.png")), size=(20, 20))
        self.CalendarOpenButton = customtkinter.CTkButton(master=self, text="Выбрать дату", image=self.image_icon_image, command=lambda: [self.select_date()])
        self.CalendarOpenButton.grid(row=3, column=2, pady=5, padx=10, sticky="ew")
        CTkToolTip(self.CalendarOpenButton, message="Открыть окно для выбора даты")

        customtkinter.CTkLabel(master=self, text="Открыть папку с документами к выбранному ремонту:").grid(row=4, columnspan=2, column=0, padx=10, pady=10, sticky="ew")
        self.OpenFolderRepairButton = customtkinter.CTkButton(master=self, text="Открыть папку", command=lambda: self.open_folder())
        self.OpenFolderRepairButton.grid(row=4, column=2, pady=5, padx=10, sticky="ew")
        CTkToolTip(self.OpenFolderRepairButton, message="Открыть папку с документами к выбранному ремонту.")

    def clear_whole_data(self):
        """
                Очищает все данные в элементах интерфейса.
                """
        self.DataOfRepaor_entry.delete(0, tkinter.END)
        self.DecriptiontextBox.delete("1.0", tkinter.END)

    def open_folder(self):
        """
                Открывает папку с документами выбранного ремонта.
                """
        currVal = self.combobox1_repair.get()
        parts = currVal.split('|')  # Разделить строку на подстроки по символу '|'
        if len(parts) > 0:
            repair_id = parts[0].strip()  # Получить первую подстроку и удалить лишние пробелы

            try:
                repair_id = int(repair_id)  # Преобразовать строку в целое число
                repair_path = self.db_manager.get_data("repair", "document_path", f"id = {repair_id}")[0][0]
                # Формирование пути к папке ремонта
                print(str(repair_path))
                repair_folder_path = os.path.join(str(repair_path))

                # Проверка существования папки
                if os.path.exists(repair_folder_path):
                    # Открытие папки в системном проводнике
                    os.startfile(repair_folder_path)
                else:
                    CTkMessagebox(title="Ошибка", message="Папка ремонта не существует!", icon="cancel")

            except ValueError:
                CTkMessagebox(title="Ошибка", message="Возможно папка была создана некорректно!", icon="cancel")

    def load_repair(self, choice):
        """
                Загружает информацию о выбранном ремонте и отображает её в соответствующих полях.

                Args:
                    choice (str): Выбранный ремонт в комбобоксе.
                """
        self.clear_whole_data()
        parts = choice.split('|')
        repair_id = [part.strip() for part in parts][0]
        data = self.db_manager.get_data("repair", "*", f"id = {repair_id}")
        data_for_inset = list(data[0])

        # Преобразование даты из формата "YYYY-MM-DD" в формат "DD.MM.YYYY"
        date_str = data_for_inset[3]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d.%m.%Y")

        self.DecriptiontextBox.insert(tkinter.END, data_for_inset[2])
        self.DataOfRepaor_entry.insert(0, formatted_date)



    def select_date(self):
        """
        Открывает календарь для выбора даты ремонта.

        Если окно календаря уже существует, оно будет фокусироваться.
        При выборе даты, дата будет вставлена в соответствующее поле и окно календаря закроется.
        В случае возникновения исключения, оно будет выведено в консоль.

        Attributes:
            additionalWIN (customtkinter.CTkToplevel): Окно календаря.
        """

        try:
            if hasattr(self, 'additionalWIN') and self.additionalWIN.winfo_exists():
                self.additionalWIN.focus()
                return
            self.additionalWIN = customtkinter.CTkToplevel(self)
            self.additionalWIN.geometry("260x200")
            self.additionalWIN.focus()
            self.additionalWIN.title(f"Calendar")
            self.additionalWIN.focus()
            maximize_minimize_button.hide(self.additionalWIN)
            cal = Calendar(self.additionalWIN, selectmode='day', date_pattern="dd.mm.yyyy")

            def set_date():
                """
                Устанавливает выбранную дату в энтри
                """
                selected_date = cal.get_date()
                self.DataOfRepaor_entry.delete(0, 'end')
                self.DataOfRepaor_entry.insert(0, selected_date)
                self.additionalWIN.destroy()

            cal.pack()
            cal.bind('<<CalendarSelected>>', lambda event: set_date())
        except Exception as e:
            print(f"Exception in SelecTData: {e}")


class FirstFrame(customtkinter.CTkFrame):
    """
        Класс для создания и управления первой частью окна управления ремонтами.

        Attributes:
            secondFrameInstance (SecondFrame): Экземпляр второго фрейма для взаимодействия.
            combobox1_branch_office (customtkinter.CTkComboBox): Комбобокс для выбора филиала.
            combobox2_structural_unit (customtkinter.CTkComboBox): Комбобокс для выбора структурного подразделения.
            combobox3_type_of_device (customtkinter.CTkComboBox): Комбобокс для выбора типа устройства.
            combobox4_device (customtkinter.CTkComboBox): Комбобокс для выбора устройства.

        Methods:
            load_third_data: Загружает данные о типе устройства.
            load_main_data: Загружает основную информацию о ремонте.
            load_second_data: Загружает данные о структурных подразделениях.
            load_data: Загружает данные о филиалах.
            FillComboBox: Заполняет комбобокс данными.
        """
    def __init__(self, master, secondFrameInstance, db_manager=None):
        """
                Инициализирует объект FirstFrame.

                Args:
                    master: Родительский виджет.
                    secondFrameInstance (SecondFrame): Экземпляр второго фрейма для взаимодействия.
                """
        super().__init__(master)
        self.db_manager = db_manager
        self.secondFrameInstance = secondFrameInstance

        self.grid_columnconfigure((0, 1), weight=1)
        self.configure(border_color="dodgerblue", border_width=3)
        customtkinter.CTkLabel(master=self, text="Загрузка данных", fg_color="gray30", font=("Arial", 14)).grid(row=0, columnspan=2, column=0, padx=10,
                                                                                                                pady=10, sticky="ew")

        customtkinter.CTkLabel(master=self, text="Филиал").grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        customtkinter.CTkLabel(master=self, text="Cтруктурное подразделение").grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        customtkinter.CTkLabel(master=self, text="Тип устройства").grid(row=3, column=0, padx=10, pady=10, sticky='nsew')
        customtkinter.CTkLabel(master=self, text="Устройство").grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
        data = self.db_manager.get_data("branch_office", "name", "")
        data = [str(row[0]) for row in data]
        self.combobox1_branch_office = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly", command=self.load_data)
        self.combobox1_branch_office.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        CTkToolTip(self.combobox1_branch_office, message="Выберите филиал.")
        self.FillComboBox(self.combobox1_branch_office, data)

        self.combobox2_structural_unit = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly", command=self.load_second_data)
        self.combobox2_structural_unit.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        CTkToolTip(self.combobox2_structural_unit, message="Выберите структурное подразделение.")

        self.combobox3_type_of_device = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly", command=self.load_third_data)
        self.combobox3_type_of_device.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        CTkToolTip(self.combobox3_type_of_device, message="Выберите тип устройства.")

        self.combobox4_device = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly", command=self.load_main_data)
        self.combobox4_device.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")
        CTkToolTip(self.combobox4_device, message="Выберите устройствo.")

    def load_third_data(self, choice):
        """
                Загружает данные о типе устройства и заполняет комбобокс устройств.

                Args:
                    choice (str): Выбранный тип устройства.
                """
        type_of_device_id = self.db_manager.get_data("type_of_device", "id", f"name = '{choice}'")[0][0]

        branch_id = self.db_manager.get_data("branch_office", "id", f"name = '{self.combobox1_branch_office.get()}'")[0][0]
        structural_unit_id = self.db_manager.get_data("structural_unit", "id", f"name = '{self.combobox2_structural_unit.get()}'")[0][0]

        all_basic_info = self.db_manager.get_data("basic_info", "*", f"type_of_device_id = {type_of_device_id} AND branch_id = {branch_id} AND structural_unit_id = {structural_unit_id}")

        str_data_combobox4 = list()
        for data in all_basic_info:
            str_data_combobox4.append(f"{data[0]} | {data[1]} | {data[2]} | {data[3]}")
        self.FillComboBox(self.combobox4_device, str_data_combobox4)

    def load_main_data(self, choice):
        """
                Загружает основную информацию о ремонте и заполняет комбобокс ремонтов.

                Args:
                    choice (str): Выбранное устройство.
                """
        parts = choice.split('|')
        result_list = [part.strip() for part in parts]
        print(result_list[0])
        try:
            all_repairs = self.db_manager.get_data("repair", "*", f"basic_info_id = {result_list[0]}")
            print(all_repairs)
            str_data_combobox1_repair = list()
            for data in all_repairs:
                date_str = data[3]
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d.%m.%Y")
                str_data_combobox1_repair.append(f"{data[0]} | {formatted_date}")
            self.FillComboBox(self.secondFrameInstance.combobox1_repair, str_data_combobox1_repair)

            if not all_repairs:
                CTkMessagebox(title="Уведомление", message=f"Не добавлено ни одного ремонта.\n", icon="warning")
            # self.secondFrameInstance.combobox1_repair.get()

        except Exception as e:
            CTkMessagebox(title="Ошибка", message=f"Возможно не добавлено ни одного ремонта.\n{e}", icon="cancel")

    def load_second_data(self, choice):
        """
                Загружает данные о структурных подразделениях и уникальных типах устройств.

                Args:
                    choice (str): Выбранное структурное подразделение.
                """
        branch_id = self.db_manager.get_data("branch_office", "id", f"name = '{self.combobox1_branch_office.get()}'")[0][0]
        structural_unit_id = self.db_manager.get_data("structural_unit", "id", f"name = '{choice}'")[0][0]
        result = self.db_manager.exec_procedure("GetInfoByBranchAndStructuralUnit", branch_id, structural_unit_id)
        unique_type_of_device = set()
        for row in result:
            unique_type_of_device.add(row[4])
        self.FillComboBox(self.combobox3_type_of_device, unique_type_of_device)

    def load_data(self, choice):
        """
                Загружает данные о филиалах и заполняет комбобокс структурных подразделений.

                Args:
                    choice (str): Выбранный филиал.
                """
        data = self.db_manager.exec_procedure("GetStructuralUnits", choice)
        data = [str(row[0]) for row in data]
        self.FillComboBox(self.combobox2_structural_unit, data)

    def FillComboBox(self, combobox, data_):
        """
               Заполняет комбобокс данными.

               Args:
                   combobox (customtkinter.CTkComboBox): Комбобокс для заполнения.
                   data_ (list): Данные для заполнения комбобокса.
               """
        data__ = [str(data) for data in data_]
        combobox.configure(values=data__)
        self.update()


class ThirdFrame(customtkinter.CTkFrame):
    """
        Класс для создания и управления третьей частью окна управления ремонтами.

        Attributes:
            secondFrameInstance (SecondFrame): Экземпляр второго фрейма для взаимодействия.
            firstFrameInstance (FirstFrame): Экземпляр первого фрейма для взаимодействия.

        Methods:
            add_repair: Добавляет новый ремонт.
            save_changes_repair: Сохраняет изменения в ремонте.
            delete_repair: Удаляет выбранный ремонт.
            create_repair_folder: Создает папку для нового ремонта.
        """
    def __init__(self, master, secondFrameInstance,firstFrameInstance, db_manager=None):
        """
                Инициализирует объект ThirdFrame.

                Args:
                    master: Родительский виджет.
                    secondFrameInstance (SecondFrame): Экземпляр второго фрейма для взаимодействия.
                    firstFrameInstance (FirstFrame): Экземпляр первого фрейма для взаимодействия.
                """
        super().__init__(master)
        self.db_manager = db_manager
        self.secondFrameInstance = secondFrameInstance
        self.firstFrameInstance = firstFrameInstance


        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.configure(border_color="red", border_width=1)

        add_repair_button = customtkinter.CTkButton(master=self, text="Добавить", hover_color="green", command=lambda: self.add_repair())
        add_repair_button.grid(row=0, column=0, pady=5, padx=10, sticky="ew")

        save_changes_button = customtkinter.CTkButton(master=self, text="Сохранить", hover_color="green", command=lambda: self.save_changes_repair())
        save_changes_button.grid(row=0, column=1, pady=5, padx=10, sticky="ew")

        del_repair_button = customtkinter.CTkButton(master=self, text="Удалить", hover_color="red", command=lambda: self.delete_repair())
        del_repair_button.grid(row=0, column=2, pady=5, padx=10, sticky="ew")

    def add_repair(self):
        """
                Добавляет новый ремонт, создает соответствующую папку и вносит данные в базу данных.
                """
        descr = self.secondFrameInstance.DecriptiontextBox.get("1.0", "end-1c")
        date = self.secondFrameInstance.DataOfRepaor_entry.get()
        choice = self.firstFrameInstance.combobox4_device.get()

        # Проверка на пустоту полей
        if not descr or not date or not choice:
            CTkMessagebox(title="Предупреждение", message="Необходимо заполнить все поля.", icon="warning")
            return

        parts = choice.split('|')
        result_list = [part.strip() for part in parts]

        try:
            # Создаем путь к папке с данными о ремонте
            branch_office = self.firstFrameInstance.combobox1_branch_office.get()
            structural_unit = self.firstFrameInstance.combobox2_structural_unit.get()
            device_type = self.firstFrameInstance.combobox3_type_of_device.get()

            # Проверяем, что все комбобоксы содержат данные
            if not branch_office or not structural_unit or not device_type:
                CTkMessagebox(title="Предупреждение", message="Необходимо выбрать значения во всех полях.", icon="warning")
                return

            folder_path = os.path.join("repairs", branch_office, structural_unit, device_type)

            # Создаем папку, если она еще не существует
            os.makedirs(folder_path, exist_ok=True)

            # Формируем имя папки для текущего ремонта
            name_for_folder = f"{date}_{result_list[3]}"
            # Создаем папку для текущего ремонта в нужном месте
            repair_folder_path = os.path.join(folder_path, name_for_folder)
            os.makedirs(repair_folder_path)

            # Добавляем данные о ремонте в базу данных
            self.db_manager.insert_data("repair", "basic_info_id, description, repair_date, document_path",
                                   f"'{result_list[0]}', '{descr}', '{date}', '{repair_folder_path}'")


            os.startfile(repair_folder_path)

            # Выводим сообщение об успешном добавлении ремонта
            CTkMessagebox(title="Успех", message="Ремонт успешно добавлен!\n Для обновления заново выберите устройство!", icon="check", option_1="Ok")
            self.secondFrameInstance.clear_whole_data()
        except Exception as e:
            # Выводим сообщение об ошибке с использованием CTkMessagebox
            CTkMessagebox(title="Ошибка", message="Произошла ошибка при добавлении ремонта.", icon="cancel")
            print(f"An error occurred: {e}")

    def save_changes_repair(self):
        """
                Сохраняет изменения в описании и дате ремонта в базе данных.
                """
        try:
            # Получаем описание ремонта и дату
            descr = self.secondFrameInstance.DecriptiontextBox.get("1.0", "end-1c")
            date = self.secondFrameInstance.DataOfRepaor_entry.get()

            # Получаем выбранный ремонт
            choice = self.secondFrameInstance.combobox1_repair.get()
            parts = choice.split('|')
            repair_id = parts[0].strip()

            # Формируем строку для обновления данных
            update_data = f"description = '{descr}', repair_date = '{date}'"

            # Обновляем данные в базе данных
            self.db_manager.update("repair", update_data, f"id = {repair_id}")

            # Выводим сообщение об успешном обновлении ремонта
            CTkMessagebox(title="Успех", message="Информация о ремонте успешно обновлена!", icon="check", option_1="Ok")
        except Exception as e:
            # Выводим сообщение об ошибке с использованием CTkMessagebox
            CTkMessagebox(title="Ошибка", message="Произошла ошибка при сохранении изменений.", icon="cancel")
            print(f"An error occurred: {e}")

    def delete_repair(self):
        choice = self.secondFrameInstance.combobox1_repair.get()
        # Проверяем, не является ли choice пустым
        if not choice:
            CTkMessagebox(title="Предупреждение", message="Выберите ремонт для удаления.", icon="warning")
            return
        """Удаляет выбранный ремонт из базы данных и соответствующую папку на диске."""
        response = CTkMessagebox(title="Подтверждение удаления",
                                 message=f"Вы действительно хотите удалить выбранный ремонт?'?",
                                 icon="warning",
                                 option_1="Да",
                                 option_2="Нет").get()
        if response == "Да":
            try:
                parts = choice.split('|')
                choice = [part.strip() for part in parts]
                repair_folder_path = self.db_manager.get_data("repair", "document_path", f"id = {choice[0]}")[0][0]
                # Проверяем существование папки ремонта перед её удалением
                if os.path.exists(repair_folder_path):
                    # Удаляем папку ремонта
                    shutil.rmtree(repair_folder_path)
                self.db_manager.delete_data("repair", f"id = {choice[0]}")
                # Выводим сообщение об успешном удалении ремонта
                CTkMessagebox(title="Успех", message="Ремонт успешно удален!", icon="check", option_1="Ok")
            except Exception as e:
                # Выводим сообщение об ошибке с использованием CTkMessagebox
                CTkMessagebox(title="Ошибка", message="Произошла ошибка при удалении ремонта.", icon="cancel")
        else:
            pass
    def create_repair_folder(self, name):
        """
                Создает папку для нового ремонта.

                Args:
                    name (str): Имя для новой папки ремонта.

                Returns:
                    str: Путь к созданной папке..
                """
        try:
            # Получите путь к папке repairs
            repairs_folder = "repairs"
            # Проверьте, существует ли папка repairs, и если нет, создайте ее
            if not os.path.exists(repairs_folder):
                os.makedirs(repairs_folder)
            # Создайте папку для нового ремонта на основе его ID
            repair_folder_path = os.path.join(repairs_folder, str(name))
            if not os.path.exists(repair_folder_path):
                os.makedirs(repair_folder_path)
            print(f"Folder for repair {name} created successfully.")
            return repair_folder_path
        except Exception as e:
            CTkMessagebox(title="Ошибка", message="Ошибка создания папки! ", icon="cancel")
            return None


