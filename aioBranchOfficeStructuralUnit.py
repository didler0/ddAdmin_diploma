import customtkinter
import tkinter
from dataBase import DatabaseManager
from CTkMessagebox import CTkMessagebox
import CTkAddDelCombobox

# Инициализация менеджера базы данных
with open('database_info.txt', 'r') as file:
    db_info = file.read().strip()
db_info_parts = db_info.split(', ')
db_manager = DatabaseManager(db_info_parts[0], db_info_parts[1])


class AioBranchOfficeStructuralUnit(customtkinter.CTkToplevel):
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

        self.branch_office_combob = CTkAddDelCombobox.ComboBoxWithButtons
        self.list_widgets = []
        self.list_widgets_only_entry = []

        self.frame_ = None
        self.frame_for_entry = None  # Added to store the frame for entry widgets
        self.create_window()

    def create_window(self):
        """
        Создание окна добавления компьютера.
        """
        self.title("Добавление/Редактирование | филиалов/структурных подразделений")
        self.geometry("900x500")
        self.minsize(900, 500)
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.frame_ = customtkinter.CTkScrollableFrame(master=self)
        self.frame_.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_.grid_columnconfigure(0, weight=0)
        self.frame_.grid_columnconfigure(1, weight=1)

        data = db_manager.get_data("branch_office", '*')
        #преобразование кортежа списков в список
        data = [str(row[1]) for row in data]
        label = customtkinter.CTkLabel(master=self.frame_, text="Выберите филиал", font=("Arial", 12))
        label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.branch_office_combob = CTkAddDelCombobox.ComboBoxWithButtons(table="branch_office", master=self.frame_, values=data,
                                                                          command_=lambda choice: self.callback_(choice))
        self.branch_office_combob.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Кнопка для добавления данных
        add_new_structural_units_to_branch_button = customtkinter.CTkButton(master=self, text="Закрепить внесенные структурные подразделения за филиалом",
                                                                            command=lambda: self.add_new_structural_units_to_branch())
        add_new_structural_units_to_branch_button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

    def add_new_structural_units_to_branch(self):
        list_of_str_units = []
        branch_office = self.branch_office_combob.get_current_value()

        # Получение списка введенных структурных подразделений
        for widget in self.list_widgets_only_entry:
            if isinstance(widget, customtkinter.CTkEntry) and widget.get() != '':
                list_of_str_units.append(widget.get())
        print(branch_office)
        print(list_of_str_units)

        try:
            # Получение идентификатора филиала
            id_branch = db_manager.get_data("branch_office", "id", f"name = '{branch_office}'")[0][0]
            print(id_branch)
        except IndexError:
            CTkMessagebox(title="Ошибка", message="Выбранный филиал не найден в базе данных.", icon="cancel")
            return

        # Проверка и добавление отсутствующих структурных подразделений
        try:
            for text in list_of_str_units:
                # Проверяем, существует ли структурное подразделение в базе данных
                if not db_manager.check_structural_unit_exists(text):
                    # Если структурное подразделение отсутствует, добавляем его
                    db_manager.insert_data("structural_unit", "name", f"'{text}'")
        except Exception as e:
            CTkMessagebox(title="Ошибка", message=f"Ошибка при добавлении структурного подразделения: {str(e)}", icon="cancel")
            return

        # Получение идентификаторов структурных подразделений и их добавление к филиалу
        try:
            for text in list_of_str_units:
                # Проверяем, привязано ли структурное подразделение к филиалу
                if not db_manager.check_structural_unit_assigned_to_branch(text, branch_office):
                    # Если структурное подразделение не привязано к филиалу, добавляем его привязку
                    structural_unit_id = db_manager.get_data("structural_unit", "id", f"name = '{text}'")[0][0]
                    db_manager.insert_data("branch_structural_unit", "branch_office_id, structural_unit_id", f"'{id_branch}', '{structural_unit_id}'")

            print("Добавлены новые структурные подразделения к филиалу.")
        except Exception as e:
            CTkMessagebox(title="Ошибка", message=f"Ошибка при привязке структурного подразделения к филиалу: {str(e)}", icon="cancel")
            return

    def callback_(self, choice):
        assigned_structural_units = db_manager.exec_procedure("GetStructuralUnits", choice)
        assigned_structural_units = [item[0] for item in assigned_structural_units]
        print(assigned_structural_units)

        # Удаление всех виджетов с формы
        for widget in self.list_widgets:
            widget.destroy()
        for widget in self.list_widgets_only_entry:
            widget.destroy()
        self.list_widgets = []
        self.list_widgets_only_entry = []

        if assigned_structural_units:
            # Добавление виджетов для каждого структурного подразделения
            for i, text in enumerate(assigned_structural_units):
                label = customtkinter.CTkLabel(master=self.frame_, text=f"Структурное подразделение {i + 1}", font=("Arial", 12))
                label.grid(row=i + 1, column=0, padx=10, pady=10, sticky="w")
                self.list_widgets.append(label)
                entry = customtkinter.CTkEntry(master=self.frame_)
                entry.grid(row=i + 1, column=1, padx=10, pady=10, sticky="nsew", columnspan=2)
                entry.insert(0, text)
                entry.configure(state="disabled")
                self.list_widgets_only_entry.append(entry)

                # Добавление кнопки редактирования
                edit_button = customtkinter.CTkButton(master=self.frame_, text="Редактировать", command=lambda idx=i: self.edit_entry(idx))
                edit_button.grid(row=i + 1, column=3, padx=5, pady=5)
                self.list_widgets.append(edit_button)

                # Добавление кнопки удаления
                delete_button = customtkinter.CTkButton(master=self.frame_, text="Удалить", command=lambda idx=i: self.delete_entry(idx))
                delete_button.grid(row=i + 1, column=4, padx=5, pady=5)
                self.list_widgets.append(delete_button)

            # Добавление кнопки "+" для добавления новой строки
            add_button = customtkinter.CTkButton(master=self.frame_, text="+", command=lambda idx=i + 2: self.add_new_entry(idx))
            add_button.grid(row=len(assigned_structural_units) + 1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            self.list_widgets.append(add_button)
            print(self.list_widgets)
        else:
            print("Нет данных для отображения")
            CTkMessagebox(title="Ошибка", message="Нет данных для отображения!", icon="warning")
            # Добавление кнопки "+" для возможности добавления данных
            add_button = customtkinter.CTkButton(master=self.frame_, text="+", command=lambda: self.add_new_entry(1))
            add_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            self.list_widgets.append(add_button)

    def edit_entry(self, idx):
        try:
            print(idx)
            old_value = self.list_widgets_only_entry[idx].get()

            dialog = customtkinter.CTkInputDialog(text="Введите новое значение для структурного подразделения:", title="Test")
            new_value = dialog.get_input()  # waits for input
            print(new_value)

            # Проверяем, если новое значение не равно None (значение, когда пользователь нажимает Cancel)
            if new_value is not None and new_value.strip():  # Проверка на пустую строку или строку пробелов
                # Приводим к нижнему регистру для игнорирования регистра при сравнении
                new_value_lower = new_value.lower()
                old_value_lower = old_value.lower()

                # Проверяем, есть ли новое значение в других элементах списка
                for i, entry in enumerate(self.list_widgets_only_entry):
                    if i != idx and entry.get().lower() == new_value_lower:
                        CTkMessagebox(title="Ошибка", message="Это значение уже используется в другой строке.", icon="cancel")
                        return

                # Проверяем, если новое значение совпадает со старым значением
                if new_value_lower == old_value_lower:
                    CTkMessagebox(title="Ошибка", message="Новое значение совпадает со старым значением.", icon="cancel")
                    return

                # Обновляем текущий элемент
                self.list_widgets_only_entry[idx].configure(state="normal")
                self.list_widgets_only_entry[idx].delete(0, customtkinter.END)
                self.list_widgets_only_entry[idx].insert(0, new_value)
                self.list_widgets_only_entry[idx].configure(state="disabled")
                try:
                    old = f"name = '{old_value}'"
                    new = f"name = '{new_value}'"
                    if db_manager.update("structural_unit", f"{new}", f"{old}"):
                        CTkMessagebox(title="Успех", message="Наименование успешно изменено!", icon="check", option_1="Ok")
                except Exception as e:
                    CTkMessagebox(title="Ошибка", message="Ошибка при обновлении наименования структурного подразделения: " + str(e), icon="cancel")
            else:
                CTkMessagebox(title="Ошибка", message="Ничего не введено/введены пробелы.", icon="cancel")
                return
        except Exception as e:
            CTkMessagebox(title="Ошибка", message="Редактирование для новых элементов не доступно! После ввода и добавления выберите филиал заново!", icon="cancel")
            return

    def delete_entry(self, idx):
        try:
            # Получаем значение структурного подразделения, которое нужно удалить
            value_to_delete = self.list_widgets_only_entry[idx].get()
            # Удаляем структурное подразделение из базы данных
            try:
                if db_manager.delete_data("structural_unit", f"name = '{value_to_delete}'"):
                    CTkMessagebox(title="Успех", message="Структурное подразделение успешно удалено!", icon="check", option_1="Ok")
                    # Удаляем виджеты строки из интерфейса
                    for widget in self.list_widgets[idx * 3:idx * 3 + 3]:
                        widget.destroy()
                        self.list_widgets_only_entry[idx].destroy()
                    # Удаляем виджеты из списков
                    del self.list_widgets[idx * 3:idx * 3 + 3]
                    del self.list_widgets_only_entry[idx]
            except Exception as e:
                CTkMessagebox(title="Ошибка", message="Ошибка при удалении структурного подразделения: " + str(e), icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Ошибка", message="Удаление не доступно для элементов не добавленных в базу данных! Пустые строки при добавлении в базу данных ИГНОРИРУЮТСЯ!", icon="cancel")
    def add_new_entry(self, new_row_index):
        # Remove the "+" button
        add_button = self.list_widgets.pop()
        add_button.destroy()

        # Create a new row for the entry
        new_row_index = new_row_index
        print(new_row_index)
        label = customtkinter.CTkLabel(master=self.frame_, text=f"Структурное подразделение {new_row_index}", font=("Arial", 12))
        label.grid(row=new_row_index, column=0, padx=10, pady=10, sticky="w")
        self.list_widgets.append(label)
        entry = customtkinter.CTkEntry(master=self.frame_)
        entry.grid(row=new_row_index, column=1, padx=10, pady=10, sticky="nsew")

        self.list_widgets_only_entry.append(entry)
        self.update()

        # Добавление кнопки редактирования
        edit_button = customtkinter.CTkButton(master=self.frame_, text="Редактировать", command=lambda idx=new_row_index: self.edit_entry(idx))
        edit_button.grid(row=new_row_index, column=3, padx=5, pady=5)
        self.list_widgets.append(edit_button)

        # Добавление кнопки удаления
        delete_button = customtkinter.CTkButton(master=self.frame_, text="Удалить", command=lambda idx=new_row_index: self.delete_entry(idx))
        delete_button.grid(row=new_row_index, column=4, padx=5, pady=5)
        self.list_widgets.append(delete_button)

        # Add a new "+" button below the new row
        add_button = customtkinter.CTkButton(master=self.frame_, text="+", command=lambda idx=new_row_index + 1: self.add_new_entry(idx))
        add_button.grid(row=new_row_index + 1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.list_widgets.append(add_button)


if __name__ == "__main__":
    root = customtkinter.CTkToplevel()
    app = AioBranchOfficeStructuralUnit(root)
    root.mainloop()
