import customtkinter
import tkinter
from dataBase import DatabaseManager
from CTkMessagebox import CTkMessagebox
import CTkAddDelCombobox

with open('database_info.txt', 'r') as file:
    db_info = file.read().strip()
db_info_parts = db_info.split(', ')
db_manager = DatabaseManager(db_info_parts[0], db_info_parts[1])

class EditDevice_(customtkinter.CTkToplevel):
    def __init__(self, *args, basic_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabview = None
        self.widgetsBasic = []
        self.widgetsDetail = []
        self.widgetsComponents = []
        self.basic_id_ = basic_id
        print(self.basic_id_)
        self.create_window()

    def create_window(self):
        """
        Создание окна добавления компьютера.
        """
        self.title("Редактирование устройства")
        self.geometry("600x700")
        self.minsize(600, 700)

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
        self.frame = customtkinter.CTkScrollableFrame(self, height=520)
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

        # Кнопка для обновления данных
        add_data_button = customtkinter.CTkButton(master=self, text="Обновить", command=lambda: self.update_all_data())
        add_data_button.grid(row=2, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)

        # Кнопка для удаления данных
        del_data_button = customtkinter.CTkButton(master=self, text="Удалить", hover_color="red", command=lambda: self.delete_all_data())
        del_data_button.grid(row=3, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)
        self.grid_rowconfigure(0, weight=0)
        self.load_dataALL()
    def update_all_data(self):
        data_basic = db_manager.get_data("basic_info", "*", f"id = {self.basic_id_}")
        """
        Обновление всех данных в базе данных.
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
            try:
                db_manager.insert_data_component(*values_component)
            except Exception as e:
                # Отображение окна с сообщением об ошибке
                CTkMessagebox(title="Ошибка", message="Ошибка при добавлении компьютера: " + str(e), icon="cancel")
                print(f"An error occurred while adding computer: {e}")
            try:
                db_manager.insert_data_detail_info(*values_details)
            except Exception as e:
                # Отображение окна с сообщением об ошибке
                CTkMessagebox(title="Ошибка", message="Ошибка при добавлении компьютера: " + str(e), icon="cancel")
                print(f"An error occurred while adding computer: {e}")

            last_details_id = db_manager.get_last_id("detail_info")
            try:
                values_basic.append(last_details_id)
                db_manager.insert_data_basic_info(*values_basic)
            except Exception as e:
                # Отображение окна с сообщением об ошибке
                CTkMessagebox(title="Ошибка", message="Ошибка при добавлении компьютера: " + str(e), icon="cancel")
                print(f"An error occurred while adding computer: {e}")

            # Отображение окна с сообщением об успешном добавлении
            CTkMessagebox(title="Успех",
                          message="Компьютер успешно добавлен!\n Если была добавлена новое место расположения или был добавлен ПЕРВЫЙ компьютер - перезапустите приложение",
                          icon="check", option_1="Ok")

        except Exception as e:
            # Отображение окна с сообщением об ошибке
            CTkMessagebox(title="Ошибка", message="Ошибка при добавлении компьютера: " + str(e), icon="cancel")
            print(f"An error occurred while adding computer: {e}")

    def delete_all_data(self):
        pass

    def set_data_to_basic(self, values_basic):
        """
        Установка данных в раздел базовой информации.

        Args:
            values_basic (list): Список значений для установки в раздел базовой информации.
        """
        try:
            # Remove unwanted elements from the list
            values_basic.pop(0)
            values_basic.pop(7)
            values_basic.pop(7)
            values_basic.pop(7)
            values_basic.pop(7)

            # Iterate through widgets and values to set data
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
            print(f"An error occurred while setting data to the basic section: {e}")

    def set_data_to_detail(self, values_detail):
        """
        Установка данных в раздел детальной информации.

        Args:
            values_detail (list): Список значений для установки в раздел детальной информации.
        """
        try:
            # Remove unwanted elements from the list
            values_detail.pop(0)
            values_detail.pop(0)

            # Iterate through widgets and values to set data
            for widget, value in zip(self.widgetsDetail, values_detail):
                if isinstance(widget, customtkinter.CTkEntry):
                    widget.insert(0, value)
        except IndexError as e:
            print(f"An error occurred while setting data to the detail section: {e}")

    def set_data_to_component(self, values_component):
        """
        Установка данных в раздел информации о компонентах.

        Args:
            values_component (list): Список значений для установки в раздел информации о компонентах.
        """
        try:
            # Remove unwanted elements from the list
            values_component.pop(0)

            # Iterate through widgets and values to set data
            for widget, value in zip(self.widgetsComponents, values_component):
                if isinstance(widget, customtkinter.CTkEntry):
                    widget.insert(0, value)
        except IndexError as e:
            print(f"An error occurred while setting data to the component section: {e}")

    def load_dataALL(self):
        """
        Загрузка данных во все разделы.

        """
        try:
            self.clear_whole_data()

            data_basic = db_manager.get_data("basic_info", "*", f"id = {self.basic_id_}")
            if not data_basic:
                print("No data found for the specified basic ID.")
                return
            data_basic = list(data_basic[0])
            qwe = data_basic

            # Dictionary to map column index to table name
            column_to_table = {
                4: "type_of_device",
                5: "place_of_installation",
                7: "material_resp_person",
                12: "branch_office",
                13: "structural_unit"
            }
            # Replace IDs with corresponding values
            for column_index, table_name in column_to_table.items():
                value = data_basic[column_index]  # Get the value from the list
                name_result = db_manager.get_data(table_name, "name", f"id = '{value}'")  # Fetch the name associated with the ID
                if name_result:
                    data_basic[column_index] = name_result[0][0]  # Replace the ID with the name in the list
                else:
                    print(f"Could not find name for ID {value} in table {table_name}")

            # Set data to basic section
            self.set_data_to_basic(data_basic[:])

            # Set data to detail section
            data_detail = db_manager.get_data("detail_info", "*", f"id = {data_basic[11]}")
            if not data_detail:
                print("No data found for the specified detail ID.")
                return
            data_detail = list(data_detail[0])
            self.set_data_to_detail(data_detail[:])
            # Set data to component section
            data_component = db_manager.get_data("component", "*", f"id = {data_detail[1]}")
            if not data_component:
                print("No data found for the specified component ID.")
                return
            data_component = list(data_component[0])
            self.set_data_to_component(data_component)

        except Exception as e:
            print(f"An error occurred while loading data: {e}")

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
                self.combobox1_branch_office = customtkinter.CTkComboBox(master=self.tabview.tab("Базовая информация"), values=data, state="readonly", command=self.load_data)
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
    def load_data(self,choice):
        print(choice)
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


if __name__ == "__main__":
    root = tkinter.Tk()
    app = EditDevice_(root)
    root.mainloop()
