import customtkinter
import tkinter
from dataBase import DatabaseManager
from CTkMessagebox import CTkMessagebox
import CTkAddDelCombobox

# Загрузка информации о базе данных из файла
with open('database_info.txt', 'r') as file:
    db_info = file.read().strip()

# Разделение информации о базе данных на части
db_info_parts = db_info.split(', ')

# Создание экземпляра менеджера базы данных
db_manager = DatabaseManager(db_info_parts[0], db_info_parts[1])

class DescriptionViewer(customtkinter.CTkToplevel):
    def __init__(self, *args, basic_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabview = None
        self.widgetsBasic = []
        self.widgetsDetail = []
        self.widgetsComponents = []
        self.basic_id_ = basic_id
        self.create_window()

    def create_window(self):
        """
        Создание окна добавления компьютера.
        """
        self.title("Редактирование устройства")
        self.geometry("600x650")
        self.minsize(600, 650)
        self.maxsize(5000,650)

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

        self.grid_columnconfigure(1, weight=1)
        self.frame = customtkinter.CTkScrollableFrame(self, height=620)
        self.frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)

        self.tabview = customtkinter.CTkTabview(master=self.frame, height=515, width=550)
        self.tabview.pack()

        # Добавление вкладок для разных секций информации
        self.tabview.add("Базовая информация")
        self.create_basic_info_tab(labels_basic)
        self.tabview.add("Детальное описание")
        self.create_detail_info_tab(labels_detail)
        self.tabview.add("Компоненты")
        self.create_components_info_tab(labels_components)

        self.load_dataALL()

    def set_data_to_basic(self, values_basic):
        """
        Установка данных в раздел базовой информации.

        Args:
            values_basic (list): Список значений для установки в раздел базовой информации.
        """
        try:
            # Удаление ненужных элементов из списка
            values_basic.pop(0)
            values_basic.pop(7)
            values_basic.pop(7)
            values_basic.pop(7)
            values_basic.pop(7)

            # Итерация по виджетам и значениям для установки данных
            for widget, value in zip(self.widgetsBasic, values_basic):
                if isinstance(widget, customtkinter.CTkEntry):
                    widget.insert(0, value)
                elif isinstance(widget, customtkinter.CTkTextbox):
                    widget.insert("1.0", value)
                elif isinstance(widget, customtkinter.CTkComboBox):
                    widget.set(value)
                elif isinstance(widget, CTkAddDelCombobox.ComboBoxWithButtons):
                    widget.set_current_value(value)
        except IndexError as e:
            print(f"Произошла ошибка при установке данных в раздел базовой информации: {e}")

    def set_data_to_detail(self, values_detail):
        """
        Установка данных в раздел детальной информации.

        Args:
            values_detail (list): Список значений для установки в раздел детальной информации.
        """
        try:
            # Удаление ненужных элементов из списка
            values_detail.pop(0)
            values_detail.pop(0)

            # Итерация по виджетам и значениям для установки данных
            for widget, value in zip(self.widgetsDetail, values_detail):
                if isinstance(widget, customtkinter.CTkEntry):
                    widget.insert(0, value)
        except IndexError as e:
            print(f"Произошла ошибка при установке данных в раздел детальной информации: {e}")

    def set_data_to_component(self, values_component):
        """
        Установка данных в раздел информации о компонентах.

        Args:
            values_component (list): Список значений для установки в раздел информации о компонентах.
        """
        try:
            # Удаление ненужных элементов из списка
            values_component.pop(0)

            # Итерация по виджетам и значениям для установки данных
            for widget, value in zip(self.widgetsComponents, values_component):
                if isinstance(widget, customtkinter.CTkEntry):
                    widget.insert(0, value)
        except IndexError as e:
            print(f"Произошла ошибка при установке данных в раздел информации о компонентах: {e}")

    def load_dataALL(self):
        """
        Загрузка данных во все разделы.
        """
        try:
            # Получение данных базовой информации из базы данных
            data_basic = db_manager.get_data("basic_info", "*", f"id = {self.basic_id_}")
            if not data_basic:
                print("Данные для указанного базового идентификатора не найдены.")
                return
            data_basic = list(data_basic[0])

            # Словарь для сопоставления индекса столбца с названием таблицы
            column_to_table = {
                4: "type_of_device",
                5: "place_of_installation",
                7: "material_resp_person",
                12: "branch_office",
                13: "structural_unit"
            }

            # Замена идентификаторов соответствующими значениями
            for column_index, table_name in column_to_table.items():
                value = data_basic[column_index]  # Получение значения из списка
                name_result = db_manager.get_data(table_name, "name", f"id = '{value}'")  # Получение соответствующего имени по идентификатору
                if name_result:
                    data_basic[column_index] = name_result[0][0]  # Замена идентификатора на имя в списке
                else:
                    print(f"Не удалось найти имя для идентификатора {value} в таблице {table_name}")

            # Установка данных в раздел базовой информации
            self.set_data_to_basic(data_basic[:])

            # Установка данных в раздел детальной информации
            data_detail = db_manager.get_data("detail_info", "*", f"id = {data_basic[11]}")
            if not data_detail:
                print("Данные для указанного идентификатора деталей не найдены.")
                return
            data_detail = list(data_detail[0])
            self.set_data_to_detail(data_detail[:])

            # Установка данных в раздел информации о компонентах
            data_component = db_manager.get_data("component", "*", f"id = {data_detail[1]}")
            if not data_component:
                print("Данные для указанного идентификатора компонентов не найдены.")
                return
            data_component = list(data_component[0])
            self.set_data_to_component(data_component)

        except Exception as e:
            print(f"Произошла ошибка при загрузке данных: {e}")

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
            elif text == "Материально ответственный":
                data = db_manager.get_data("material_resp_person", "name", "")
                data = [str(row[0]) for row in data]
                structural_unit = CTkAddDelCombobox.ComboBoxWithButtons(table="material_resp_person", master=self.tabview.tab("Базовая информация"), values=data)
                structural_unit.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(structural_unit)
            elif text == "Филиал":
                data = db_manager.get_data("branch_office", "name", "")
                data = [str(row[0]) for row in data]
                self.combobox1_branch_office = customtkinter.CTkComboBox(master=self.tabview.tab("Базовая информация"), values=data, state="readonly",
                                                                         command=self.load_data)
                self.combobox1_branch_office.grid(row=i, column=1, padx=10, pady=10, sticky="nsew")
                self.widgetsBasic.append(self.combobox1_branch_office)
            elif text == "Структурное подразделение":
                data = db_manager.get_data("structural_unit", "name", "")
                data = [str(row[0]) for row in data]
                self.combobox2_structural_unit = customtkinter.CTkComboBox(master=self.tabview.tab("Базовая информация"), values=[" "], state="readonly")
                self.combobox2_structural_unit.grid(row=i, column=1, padx=10, pady=10, sticky="nsew")
                self.widgetsBasic.append(self.combobox2_structural_unit)
            else:
                textBox = customtkinter.CTkTextbox(master=self.tabview.tab("Базовая информация"), height=90)
                textBox.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsBasic.append(textBox)

    def load_data(self, choice):
        data = db_manager.exec_procedure("GetStructuralUnits", choice)
        data = [str(row[0]) for row in data]
        self.FillComboBox(self.combobox2_structural_unit, data)

    def FillComboBox(self, combobox, data_):
        data__ = [str(data) for data in data_]
        combobox.configure(values=data__)
        self.update()

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
