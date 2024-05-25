import re

import customtkinter
import tkinter
from dataBase import DatabaseManager
from CTkMessagebox import CTkMessagebox
import CTkAddDelCombobox



with open('database_info.txt', 'r') as file:
    db_info = file.read().strip()
db_info_parts = db_info.split(', ')
db_manager = DatabaseManager(db_info_parts[0], db_info_parts[1])


class AddDevice_(customtkinter.CTkToplevel):
    """
    Класс для добавления нового устройства.

    Attributes:
        tabview: Объект вкладок для отображения различных секций информации.
        widgetsBasic: Список виджетов для базовой информации.
        widgetsDetail: Список виджетов для детальной информации.
        widgetsComponents: Список виджетов для информации о компонентах.
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализация окна добавления компьютера.

        Args:
            args: Позиционные аргументы.
            kwargs: Именованные аргументы.
        """
        super().__init__(*args, **kwargs)
        self.combobox_structural_unit = customtkinter.CTkComboBox
        self.tabview = None
        self.widgetsBasic = []
        self.widgetsDetail = []
        self.widgetsComponents = []
        self.create_window()

    def create_window(self):
        """
        Создание окна добавления компьютера.
        """
        self.title("Добавление устройства")
        self.geometry("600x595")
        self.minsize(600,600)

        # Метки для базовой информации
        labels_basic = ["IP Адрес *", "Название *", "Сетевое имя *", "Тип устройства *", "Место установки *", "Описание *",
                        "Материально ответственный *", "Филиал *", "Структурное подразделение *"]

        # Создание виджетов для базовой информации
        self.widgetsBasic = []
        # Метки для детальной информации
        labels_detail = ["Инвентарный № *", "Серийный № *", "MAC - адрес *", "Операционная система *", "Год покупки *", "Месяцы гарантии *"]
        self.widgetsDetail = []
        # Метки для информации о компонентах
        labels_components = ["Процессор", "ОЗУ", "Материнская плата", "Видеокарта", "Блок питания", "Сетевая карта",
                             "Куллер", "Корпус", "HDD", "SSD", "Монитор", "Клавиатура", "Мышь", "Аудио"]
        self.widgetsComponents = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame = customtkinter.CTkScrollableFrame(self, height=520)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew',columnspan=2)
        self.frame.grid_rowconfigure((0,1),weight=1)
        self.frame.grid_columnconfigure(0,weight=1)
        self.tabview = customtkinter.CTkTabview(master=self.frame, height=515, width=550)
        self.tabview.grid(row=1, column=0, padx=10, pady=10, sticky='nsew',columnspan=2)

        # Добавление вкладок для разных секций информации
        self.tabview.add("Базовая информация")
        self.create_basic_info_tab(labels_basic)
        self.tabview.add("Детальное описание")
        self.create_detail_info_tab(labels_detail)
        self.tabview.add("Компоненты")
        self.create_components_info_tab(labels_components)

        # Кнопка для добавления данных
        add_data_button = customtkinter.CTkButton(master=self, text="Добавить", command=lambda: self.add_whole_data_to_bd())
        add_data_button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Кнопка информации
        info_button = customtkinter.CTkButton(master=self, text="ИНФО",width=50, command=lambda: self.open_info_popup())
        info_button.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')


    def open_info_popup(self):
        """Метод для открытия окна с информацией"""
        CTkMessagebox(title="Информация",
                      message=" Поля, требующие заполнения, отмечены символом '*'.\n"
                              " Заполнение всех полей во вкладках 'Базовая информация' и 'Детальное описание' является обязательным.\n"
                              " Поля во вкладке 'Компоненты' не являются обязательными и могут быть оставлены пустыми.",
                      icon="info", option_1="Ok")

    def create_basic_info_tab(self, labels_basic):
        """
        Создание вкладки для базовой информации.

        Args:
            labels_basic: Список меток для базовой информации.
        """
        self.tabview.tab("Базовая информация").grid_columnconfigure(1, weight=1)
        for i, text in enumerate(labels_basic):
            label = customtkinter.CTkLabel(master=self.tabview.tab("Базовая информация"), text=text, font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=10, sticky="ew")

            if text == "IP Адрес *":
                entry = customtkinter.CTkEntry(master=self.tabview.tab("Базовая информация"), placeholder_text="IP Адрес | 255.255.255.255")
                entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(entry)
            elif text == "Место установки *":
                data = db_manager.get_data("place_of_installation", "name", "")
                data = [str(row[0]) for row in data]
                type_of_device = CTkAddDelCombobox.ComboBoxWithButtons(table="place_of_installation", master=self.tabview.tab("Базовая информация"), values=data)
                type_of_device.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(type_of_device)
            elif text == "Сетевое имя *":
                entry = customtkinter.CTkEntry(master=self.tabview.tab("Базовая информация"), placeholder_text="Сетевое имя")
                entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(entry)
            elif text == "Тип устройства *":
                data = db_manager.get_data("type_of_device", "name", "")
                data = [str(row[0]) for row in data]
                type_of_device = CTkAddDelCombobox.ComboBoxWithButtons(table="type_of_device", master=self.tabview.tab("Базовая информация"), values=data)
                type_of_device.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(type_of_device)
            elif text == "Филиал *":
                data = db_manager.get_data("branch_office", "name", "")
                data = [str(row[0]) for row in data]
                combobox1 = customtkinter.CTkComboBox(master=self.tabview.tab("Базовая информация"), values=[" "], state="readonly", command=self.load_data)
                combobox1.grid(row=i, column=1, padx=10, pady=10, sticky="nsew")
                self.FillComboBox(combobox1, data)
                self.widgetsBasic.append(combobox1)
            elif text == "Структурное подразделение *":
                self.combobox_structural_unit = customtkinter.CTkComboBox(master=self.tabview.tab("Базовая информация"), values=[" "], state="readonly")
                self.combobox_structural_unit.grid(row=i, column=1, padx=10, pady=10, sticky="nsew")
                self.widgetsBasic.append(self.combobox_structural_unit)
            elif text == "Материально ответственный *":
                data = db_manager.get_data("material_resp_person", "name", "")
                data = [str(row[0]) for row in data]
                structural_unit = CTkAddDelCombobox.ComboBoxWithButtons(table="material_resp_person", master=self.tabview.tab("Базовая информация"), values=data)
                structural_unit.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(structural_unit)
            else:
                textBox = customtkinter.CTkTextbox(master=self.tabview.tab("Базовая информация"), height=90)
                textBox.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(textBox)
    def load_data(self,choice):
        """Метод для загрузки данных из БД в комбобокс
        Args:
            choice: Выбранный элемент в комбобоксе.
        """
        data= db_manager.exec_procedure("GetStructuralUnits",choice)
        data = [str(row[0]) for row in data]
        self.FillComboBox(self.combobox_structural_unit,data)

    def create_detail_info_tab(self, labels_detail):
        """
        Создание вкладки для детальной информации.
        Args:
            labels_detail: Список меток для детальной информации.
        """
        self.tabview.tab("Детальное описание").grid_columnconfigure(1, weight=1)
        self.tabview.tab("Детальное описание").grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        for i, text in enumerate(labels_detail):
            label = customtkinter.CTkLabel(master=self.tabview.tab("Детальное описание"), text=text, font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=10, sticky="ew")

            entry = customtkinter.CTkEntry(master=self.tabview.tab("Детальное описание"), placeholder_text=text)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
            self.widgetsDetail.append(entry)

    def create_components_info_tab(self, labels_components):
        """
        Создание вкладки для информации о компонентах.

        Args:
            labels_components: Список меток для информации о компонентах.
        """
        self.tabview.tab("Компоненты").grid_columnconfigure(1, weight=1)
        for i, text in enumerate(labels_components):
            label = customtkinter.CTkLabel(master=self.tabview.tab("Компоненты"), text=text, font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=10, sticky="ew")

            entry = customtkinter.CTkEntry(master=self.tabview.tab("Компоненты"), placeholder_text=text)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
            self.widgetsComponents.append(entry)

    def get_data_from_components(self):
        """
        Получение данных из раздела компонентов.

        Returns:
            list: Список значений из раздела компонентов.
        """
        values_component = []
        for widget in self.widgetsComponents:
            if isinstance(widget, customtkinter.CTkEntry):
                value = widget.get()
                # Если значение равно пробелу, установите его на None
                if value.strip() == "":
                    value = None
            else:
                value = None
            values_component.append(value)

        return values_component


    def get_data_from_details(self):
        """
        Получение данных из раздела деталей.

        Returns:
            list: Список значений из раздела деталей.
        """
        values_detail = []
        for widget in self.widgetsDetail:
            if isinstance(widget, customtkinter.CTkEntry):
                value = widget.get()
                # Если значение равно пробелу, установите его на None
                if value.strip() == "":
                    value = None
            else:
                value = None
            values_detail.append(value)
        return values_detail
    def get_data_from_basic(self):
        """
        Получение данных из раздела базовой информации.

        Returns:
            list: Список значений из раздела базовой информации.
        """
        values_basic = []
        for widget in self.widgetsBasic:
            if isinstance(widget, customtkinter.CTkEntry):
                value = widget.get()
                # Если значение равно пробелу, установите его на None
                if value.strip() == "":
                    value = None

            elif isinstance(widget, customtkinter.CTkTextbox):
                value = widget.get("1.0", "end-1c")
                # Если значение равно пробелу, установите его на None
                if value.strip() == "":
                    value = None

            elif isinstance(widget, CTkAddDelCombobox.ComboBoxWithButtons):
                value = widget.get_current_value()
                # Если значение равно пробелу, установите его на None
                if value.strip() == "":
                    value = None

            elif isinstance(widget,customtkinter.CTkComboBox):
                value = widget.get()
                # Если значение равно пробелу, установите его на None
                if value.strip() == "":
                    value = None
            else:
                value = None
            values_basic.append(value)

        return values_basic

    def clear_data_from_section(self, widgets):
        """
        Очистка данных из секции на основе предоставленного списка виджетов.

        Args:
            widgets: Список виджетов.
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
        Очистка всех данных в секциях компонентов, деталей и базовой информации.
        """
        self.clear_data_from_section(self.widgetsBasic)
        self.clear_data_from_section(self.widgetsDetail)
        self.clear_data_from_section(self.widgetsComponents)
    def validate_detail_data(self,values_details):
        print(values_details)
        mac_regex = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')

        # Проверка значения по индексу 2 на MAC-адрес
        if values_details[2] is not None and not mac_regex.match(values_details[2]):
            raise ValueError("Неверный формат MAC-адреса!\n Пример: 00:1A:2B:3C:4D:5E или 00-1A-2B-3C-4D-5E")

        # Проверка значения по индексу 4 на целое число (Год покупки)
        if values_details[4] is not None:
            try:
                values_details[4] = int(values_details[4])
            except ValueError:
                raise ValueError("Год покупки должен быть целым числом!.")

        # Проверка значения по индексу 5 на целое число (Месяцы гарантии)
        if values_details[5] is not None:
            try:
                values_details[5] = int(values_details[5])
            except ValueError:
                raise ValueError("Месяцы гарантии должны быть целым числом!")

    def validate_basic_data(self,values_basic):
        print(values_basic)
        ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        first_element = values_basic[0]
        # Проверяем, является ли первый элемент IP-адресом
        if not ip_pattern.match(first_element):
            raise ValueError(f"IP - '{first_element}' не является допустимым IP-адресом\n Пример: 192.168.100.111")

        # Проверяем, что список не пустой
        if not values_basic or all(element is None for element in values_basic):
            raise ValueError("Вы не заполнили необходимые поля!")

        third_element = values_basic[3]
        fourth_element = values_basic[4]
        sixth_element = values_basic[6]
        if not db_manager.get_data("type_of_device","*",f"name = '{third_element}'"):
            raise ValueError("Выбрано значение, отсутствующее в базе данных! Нажмите кнопку \"Применить\" Возле поля выбора типа устройства.")
        if not db_manager.get_data("place_of_installation", "*", f"name = '{fourth_element}'"):
            raise ValueError(
                "Выбрано значение, отсутствующее в базе данных! Нажмите кнопку \"Применить\" Возле поля выбора места установки.")
        if not db_manager.get_data("material_resp_person", "*", f"name = '{sixth_element}'"):
            raise ValueError(
                "Выбрано значение, отсутствующее в базе данных! Нажмите кнопку \"Применить\" Возле поля выбора материально ответственного.")

    def validate_values(self,values):
        for value in values:
            if value in [None, '']:
                return False
        return True

    def add_whole_data_to_bd(self):
        """
        Добавление всех данных в базу данных.
        """
        try:
            # Получение данных
            values_component = self.get_data_from_components()
            values_details = self.get_data_from_details()
            values_basic = self.get_data_from_basic()

            self.validate_basic_data(values_basic)
            self.validate_detail_data(values_details)
            # Проверка наличия всех необходимых данных
            print(values_details)
            print(values_basic)
            if not self.validate_values(values_details) or not self.validate_values(values_basic):
                raise ValueError("Не все необходимые поля заполнены")

            # Список кортежей, где каждый кортеж представляет столбец, который нужно обновить, и соответствующую таблицу
            columns_to_update = [
                (3, "type_of_device", "id", values_basic),
                (4, "place_of_installation", "id", values_basic),
                (6, "material_resp_person", "id", values_basic),
                (7, "branch_office", "id", values_basic),
                (8, "structural_unit", "id", values_basic)
            ]

            # Обновление значений в values_basic
            for index, table, column, values in columns_to_update:
                value = values[index]  # Значение, которое нужно заменить на id
                id_result = db_manager.get_data(table, "id", f"name = '{value}'")
                if id_result:
                    values[index] = id_result[0][0]  # Обновляем значение на id из таблицы
                else:
                    raise ValueError(f"Вы не применили изменения в следующих полях:Тип устройства, место установки, материально ответственный.\n")

            last_component_id = db_manager.get_last_id("component")
            values_details.insert(0, last_component_id)
            db_manager.insert_data_component(*values_component)
            db_manager.insert_data_detail_info(*values_details)

            last_details_id = db_manager.get_last_id("detail_info")
            values_basic.append(last_details_id)
            db_manager.insert_data_basic_info(*values_basic)

            # Отображение окна с сообщением об успешном добавлении
            CTkMessagebox(title="Успех",
                          message="Компьютер успешно добавлен!\n Если была добавленo новое место расположения или был добавлен ПЕРВЫЙ компьютер - перезапустите приложение",
                          icon="check", option_1="Ok")
            self.clear_whole_data()

        except ValueError as ve:
            # Отображение окна с сообщением об ошибке в случае незаполненных полей
            CTkMessagebox(title="Ошибка", message=str(ve), icon="cancel")


        except Exception as e:
            # Отображение окна с сообщением об общей ошибке
            CTkMessagebox(title="Ошибка", message="Ошибка при добавлении компьютера: " + str(e), icon="cancel")


    def FillComboBox(self, combobox, data_):
        """Заполнение комбобокса данными"""
        sasha = [str(data) for data in data_]
        combobox.configure(values=sasha)
        self.update()


if __name__ == "__main__":
    root = tkinter.Tk()
    app = AddDevice_(root)
    root.mainloop()
