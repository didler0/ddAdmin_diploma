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

        # Метки для базовой информации
        labels_basic = ["IP Адрес", "Название", "Сетевое имя", "Тип устройства", "Место установки", "Описание",
                        "Материально ответственный", "Филиал", "Структурное подразделение"]

        # Создание виджетов для базовой информации
        self.widgetsBasic = []
        # Метки для детальной информации
        labels_detail = ["Инвентарный №", "Серийный №", "MAC - адрес", "Операционная система", "Год покупки", "Месяцы гарантии"]
        self.widgetsDetail = []
        # Метки для информации о компонентах
        labels_components = ["Процессор", "ОЗУ", "Материнская плата", "Видеокарта", "Блок питания", "Сетевая карта",
                             "Куллер", "Корпус", "HDD", "SSD", "Монитор", "Клавиатура", "Мышь", "Аудио"]
        self.widgetsComponents = []

        self.grid_columnconfigure(0, weight=1)
        self.frame = customtkinter.CTkScrollableFrame(self, height=520)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.tabview = customtkinter.CTkTabview(master=self.frame, height=515, width=550)
        self.tabview.pack()

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

            if text == "IP Адрес":
                entry = customtkinter.CTkEntry(master=self.tabview.tab("Базовая информация"), placeholder_text="IP Адрес | 255.255.255.255")
                entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(entry)
            elif text == "Место установки":
                data = db_manager.get_data("place_of_installation", "name", "")
                data = [str(row[0]) for row in data]
                type_of_device = CTkAddDelCombobox.ComboBoxWithButtons(table="place_of_installation", master=self.tabview.tab("Базовая информация"), values=data)
                type_of_device.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(type_of_device)
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
                combobox1 = customtkinter.CTkComboBox(master=self.tabview.tab("Базовая информация"), values=[" "], state="readonly", command=self.load_data)
                combobox1.grid(row=i, column=1, padx=10, pady=10, sticky="nsew")
                self.FillComboBox(combobox1, data)
                self.widgetsBasic.append(combobox1)
            elif text == "Структурное подразделение":
                self.combobox_structural_unit = customtkinter.CTkComboBox(master=self.tabview.tab("Базовая информация"), values=[" "], state="readonly")
                self.combobox_structural_unit.grid(row=i, column=1, padx=10, pady=10, sticky="nsew")
                self.widgetsBasic.append(self.combobox_structural_unit)
            elif text == "Материально ответственный":
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
        print(choice)

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
                widget.delete(0, customtkinter.END)
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
                widget.delete(0, customtkinter.END)
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
                widget.delete(0, customtkinter.END)
            elif isinstance(widget, customtkinter.CTkTextbox):
                value = widget.get("1.0", "end-1c")
                widget.delete("1.0", "end-1c")
            elif isinstance(widget, CTkAddDelCombobox.ComboBoxWithButtons):
                value = widget.get_current_value()
                widget.clear_data()
            elif isinstance(widget,customtkinter.CTkComboBox):
                value = widget.get()
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

    def add_whole_data_to_bd(self):
        """
        Добавление всех данных в базу данных.
        """
        try:
            # Получение данных
            values_component = self.get_data_from_components()
            values_details = self.get_data_from_details()
            values_basic = self.get_data_from_basic()

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
                    print(f"Could not find id for {table} with name '{value}'")

            last_component_id = db_manager.get_last_id("component")
            values_details.insert(0, last_component_id)
            db_manager.insert_data_component(*values_component)
            db_manager.insert_data_detail_info(*values_details)
            last_details_id = db_manager.get_last_id("detail_info")
            values_basic.append(last_details_id)

            db_manager.insert_data_basic_info(*values_basic)

            # Отображение окна с сообщением об успешном добавлении
            CTkMessagebox(title="Успех",
                          message="Компьютер успешно добавлен!\n Если была добавлена новое место расположения или был добавлен ПЕРВЫЙ компьютер - перезапустите приложение",
                          icon="check", option_1="Ok")

        except Exception as e:
            # Отображение окна с сообщением об ошибке
            CTkMessagebox(title="Ошибка", message="Ошибка при добавлении компьютера: " + str(e), icon="cancel")
            print(f"An error occurred while adding computer: {e}")

    def FillComboBox(self, combobox, data_):
        sasha = [str(data) for data in data_]
        combobox.configure(values=sasha)
        self.update()


if __name__ == "__main__":
    root = tkinter.Tk()
    app = AddDevice_(root)
    root.mainloop()
