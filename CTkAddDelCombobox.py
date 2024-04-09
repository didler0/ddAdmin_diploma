import customtkinter
from CTkMessagebox import CTkMessagebox
from dataBase import *

# Создание экземпляра менеджера базы данных и создание таблиц, если их нет
db_manager = DatabaseManager('DDLAPTOP\\SQLEXPRESS', 'PCC')
db_manager.create_tables()

class ComboBoxWithButtons(customtkinter.CTkFrame):
    """
    Класс ComboBoxWithButtons представляет собой комбинированный виджет, состоящий из выпадающего списка
    и кнопок "+" и "-".
    """

    def __init__(self, master, values=None, table="", *args, **kwargs):
        """
        Инициализация комбинированного виджета.

        Аргументы:
            master: Родительский виджет.
            values (list): Список значений для выпадающего списка.
            table (str) : Таблица для выборки данных
            *args: Позиционные аргументы для родительского класса.
            **kwargs: Именованные аргументы для родительского класса.
        """

        super().__init__(master, *args, **kwargs)
        self.values = values  # Список значений для комбобокса
        self.table = table  # Имя таблицы
        self.grid_columnconfigure((0, 2, 3), weight=0)  # кнопки не расширяются
        self.grid_columnconfigure(1, weight=1)  # поле ввода расширяется

        # Создаем кнопку "-"
        self.remove_button = customtkinter.CTkButton(self, text="-", command=self.remove_value, width=20)
        self.remove_button.grid(row=0, column=2)

        # Создаем выпадающий список
        self.combobox = customtkinter.CTkComboBox(self, values=self.values, state="readonly")
        self.combobox.grid(row=0, column=1, sticky='nsew')

        # Создаем кнопку "+"
        self.add_button = customtkinter.CTkButton(self, text="+", command=self.add_value, width=20)
        self.add_button.grid(row=0, column=0)

        # Создаем кнопку "Применить"
        self.commit_button = customtkinter.CTkButton(self, text="Применить", command=self.commit_value, width=20)
        self.commit_button.grid(row=0, column=3, padx=5)

    def get_all_values(self):
        """
        Метод для получения текущего списка значений комбобокса.
        :return: List[]
        """
        return self.combobox.cget("values")

    def get_current_value(self):
        """
        Метод для получения текущего списка значений комбобокса.

        :return: str
        """
        return self.combobox.get()

    def updateValues(self, new_values):
        """
        Метод для обновления значений комбобокса.

        Аргументы:
            new_values (list): Новый список значений для обновления комбобокса.
        """
        self.values = new_values
        self.combobox.configure(values=self.values)

    def add_value(self):
        """
        Метод для добавления нового значения в выпадающий список.
        """
        # Предложить пользователю ввести новое значение
        value = customtkinter.CTkInputDialog(title="Добавить значение", text="Введите новое значение:").get_input()
        if value:
            # Получить текущие значения выпадающего списка
            current_values = self.combobox.cget("values")
            if current_values:
                # Преобразовать значения в список
                current_values = list(current_values)
                # Добавить новое значение в список
                current_values.append(value)
                # Установить обновленные значения для выпадающего списка
                self.combobox.configure(values=current_values)
            else:
                # Если текущих значений нет, установить новое значение единственным значением
                self.combobox.configure(values=[value])

    def remove_value(self):
        """
        Метод для удаления выбранного значения из выпадающего списка с запросом подтверждения.
        """
        # Получить выбранный элемент
        selected_item = self.combobox.get()
        current_values = self.combobox.cget("values")

        if current_values:
            # Преобразовать значения в список
            current_values = list(current_values)
            # Проверить, существует ли выбранный элемент в текущих значениях списка
            if selected_item in current_values:
                # Показать диалоговое окно с вопросом об удалении
                response = CTkMessagebox(title="Подтверждение удаления",
                                         message=f"Вы действительно хотите удалить элемент '{selected_item}'?",
                                         icon="warning",
                                         option_1="Да",
                                         option_2="Нет").get()
                if response == "Да":
                    # Удалить выбранный элемент из списка
                    current_values.remove(selected_item)
                    # Установить обновленные значения для выпадающего списка
                    self.combobox.configure(values=current_values)
                    self.combobox.set("")  # Очистить текущий выбор
                    self.update()
            else:
                # Если текущих значений нет, ничего не делать
                pass

    def commit_value(self):
        current_values = self.get_all_values()
        print(current_values)
        data = db_manager.get_data(self.table, "name")
        data = [str(row[0]) for row in data]
        initial_set = set(data)
        current_set = set(current_values)

        # Находим добавленные значения
        added_values = current_set - initial_set

        # Находим удаленные значения
        removed_values = initial_set - current_set
        # Проверяем, есть ли уже существующие значения в добавленных значениях
        existing_values = initial_set.intersection(initial_set)
        if existing_values:
            # Выводим сообщение о том, что некоторые значения уже существуют в базе данных
            message = "Некоторые добавленные значения уже существуют в базе данных и не будут добавлены."
            CTkMessagebox(title="Предупреждение", message=message, icon="warning").get()
            # Убираем уже существующие значения из списка добавляемых значений
            added_values = added_values - existing_values
        else:
            pass
        # Выводим добавленные и удаленные значения на консоль
        print("Добавленные значения:", added_values)
        print("Удаленные значения:", removed_values)

        # Добавляем добавленные значения в базу данных
        for value in added_values:
            if not db_manager.insert_data(self.table, "name", f"'{value}'"):
                print(f"Ошибка при добавлении значения '{value}' в базу данных.")

        # Удаляем удаленные значения из базы данных
        for value in removed_values:
            if not db_manager.delete_data(self.table, f"name = '{value}'"):
                print(f"Ошибка при удалении значения '{value}' из базы данных.")
        updated_data=db_manager.get_data(self.table,"name",'')
        updated_data = [str(row[0]) for row in updated_data]
        self.updateValues(updated_data)
        self.combobox.set("")  # Очистить текущий выбор
        self.update()

    def clear_data(self):
        self.combobox.set("")
        
    def set_current_value(self,val):
        self.combobox.set(val)

