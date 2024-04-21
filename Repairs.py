import os
import tkinter

import customtkinter
from PIL import Image
from hPyT import maximize_minimize_button
from tkcalendar import Calendar
from dataBase import DatabaseManager
from CTkToolTip import *

from CTkMessagebox import CTkMessagebox

with open('database_info.txt', 'r') as file:
    db_info = file.read().strip()
db_info_parts = db_info.split(', ')
db_manager = DatabaseManager(db_info_parts[0], db_info_parts[1])


class Repair(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.second = customtkinter.CTkFrame
        self.last = customtkinter.CTkFrame
        self.first = customtkinter.CTkFrame
        self.create_window()

    def create_window(self):
        """
        Создание окна Ремонтов.
        """
        self.title("Ремонты")
        self.geometry("600x750")
        self.minsize(600, 750)

        self.frame = customtkinter.CTkFrame(self, height=490)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.second = SecondFrame(self.frame)
        self.second.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.first = FirstFrame(self.frame, self.second)
        self.first.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.last = ThirdFrame(self.frame)
        self.last.grid(row=2, column=0, padx=10, pady=10, sticky="ew")


class SecondFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure((0, 1), weight=1)
        self.configure(border_color="dodgerblue", border_width=3)
        customtkinter.CTkLabel(master=self, text="Ремонты", fg_color="gray30", font=("Arial", 14)).grid(row=0, columnspan=3, column=0, padx=10, pady=10, sticky="ew")

        self.combobox1_repair = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly", command=self.load_repair)
        self.combobox1_repair.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        CTkToolTip(self.combobox1_repair, message="Выберите Ремонт.")

        customtkinter.CTkLabel(master=self, text="Описание").grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.DecriptiontextBox = customtkinter.CTkTextbox(master=self, height=90)
        self.DecriptiontextBox.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        customtkinter.CTkLabel(master=self, text="Дата ремонта").grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.DataOfRepaor_entry = customtkinter.CTkEntry(master=self, placeholder_text="ГГГГ-ММ-ДД")
        self.DataOfRepaor_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "resources\\calendarICO.png")), size=(20, 20))
        self.CalendarOpenButton = customtkinter.CTkButton(master=self, text="Выбрать дату", image=self.image_icon_image,command=lambda: [self.select_date()])
        self.CalendarOpenButton.grid(row=3, column=2, pady=5, padx=10, sticky="ew")

        customtkinter.CTkLabel(master=self, text="Открыть папку с документами к компьютеру").grid(row=4, columnspan=2, column=0, padx=10, pady=10,sticky="ew")
        self.OpenFolderRepairButton = customtkinter.CTkButton(master=self, text="Открыть папку", command=lambda: self.open_folder())
        self.OpenFolderRepairButton.grid(row=4, column=2, pady=5, padx=10, sticky="ew")
    def clear_whole_data(self):
        self.DataOfRepaor_entry.delete(0, tkinter.END)
        self.DecriptiontextBox.delete("1.0", tkinter.END)

    def open_folder(self):
        choice = self.combobox1_repair.get()
        parts = choice.split('|')
        repair_id = [part.strip() for part in parts]
        repair_id = repair_id[0]
        path = db_manager.get_data("repair", "document_path", f"id = {repair_id}")[0][0]


    def load_repair(self,choice):
        self.clear_whole_data()
        parts = choice.split('|')
        repair_id = [part.strip() for part in parts]
        repair_id = repair_id[0]
        data = db_manager.get_data("repair","*",f"id = {repair_id}")
        data_for_inset = list()
        for text in data[0]:
            data_for_inset.append(text)

        self.DecriptiontextBox.insert(tkinter.END, data_for_inset[2])
        self.DataOfRepaor_entry.insert(0, data_for_inset[3])





def select_date(self):
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
            cal = Calendar(self.additionalWIN, selectmode='day', date_pattern="yyyy-mm-dd")

            def set_date():
                selected_date = cal.get_date()
                self.DataOfRepaor_entry.delete(0, 'end')
                self.DataOfRepaor_entry.insert(0, selected_date)
                self.additionalWIN.destroy()

            cal.pack()
            cal.bind('<<CalendarSelected>>', lambda event: set_date())
        except Exception as e:
            print(f"Exception in SelecTData: {e}")


class FirstFrame(customtkinter.CTkFrame):
    def __init__(self,  master, secondFrameInstance):
        super().__init__(master)
        self.secondFrameInstance = secondFrameInstance

        self.grid_columnconfigure((0, 1), weight=1)
        self.configure(border_color="dodgerblue", border_width=3)
        customtkinter.CTkLabel(master=self, text="Загрузка данных", fg_color="gray30", font=("Arial", 14)).grid(row=0, columnspan=2, column=0, padx=10,
                                                                                                                pady=10, sticky="ew")

        customtkinter.CTkLabel(master=self, text="Филиал").grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        customtkinter.CTkLabel(master=self, text="Cтруктурное подразделение").grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        customtkinter.CTkLabel(master=self, text="Тип устройства").grid(row=3, column=0, padx=10, pady=10, sticky='nsew')
        customtkinter.CTkLabel(master=self, text="Устройство").grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
        data = db_manager.get_data("branch_office", "name", "")
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
        CTkToolTip(self.combobox3_type_of_device, message="Выберите тип устройства.")

    def load_third_data(self, choice):
        type_of_device_id = db_manager.get_data("type_of_device", "id", f"name = '{choice}'")[0][0]
        all_basic_info = db_manager.get_data("basic_info", "*", f"type_of_device_id = {type_of_device_id}")

        str_data_combobox4 = list()
        for data in all_basic_info:
            str_data_combobox4.append(f"{data[0]} | {data[1]} | {data[2]} | {data[3]}")
        self.FillComboBox(self.combobox4_device, str_data_combobox4)

    def load_main_data(self, choice):
        parts = choice.split('|')
        result_list = [part.strip() for part in parts]
        print(result_list[0])
        try:
            all_repairs = db_manager.get_data("repair", "*", f"basic_info_id = {result_list[0]}")
            print(all_repairs)
            str_data_combobox1_repair = list()
            for data in all_repairs:
                str_data_combobox1_repair.append(f"{data[0]} | {data[3]}")
            self.FillComboBox(self.secondFrameInstance.combobox1_repair,str_data_combobox1_repair)
            #self.secondFrameInstance.combobox1_repair.get()

        except Exception as e:
            CTkMessagebox(title="Ошибка", message=f"Возможно не добавлено ни одного ремонта.\n{e}", icon="cancel")

    def load_second_data(self, choice):
        branch_id = db_manager.get_data("branch_office", "id", f"name = '{self.combobox1_branch_office.get()}'")[0][0]
        structural_unit_id = db_manager.get_data("structural_unit", "id", f"name = '{choice}'")[0][0]
        result = db_manager.exec_procedure("GetInfoByBranchAndStructuralUnit", branch_id, structural_unit_id)
        unique_type_of_device = set()
        for row in result:
            unique_type_of_device.add(row[4])
        self.FillComboBox(self.combobox3_type_of_device, unique_type_of_device)

    def load_data(self, choice):
        data = db_manager.exec_procedure("GetStructuralUnits", choice)
        data = [str(row[0]) for row in data]
        self.FillComboBox(self.combobox2_structural_unit, data)

    def FillComboBox(self, combobox, data_):
        data__ = [str(data) for data in data_]
        combobox.configure(values=data__)
        self.update()


class ThirdFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.configure(border_color="red", border_width=1)

        add_repair_button = customtkinter.CTkButton(master=self, text="Добавить", hover_color="green", command=lambda: self.add_repair())
        add_repair_button.grid(row=0, column=0, pady=5, padx=10, sticky="ew")

        save_changes_button = customtkinter.CTkButton(master=self, text="Сохранить", hover_color="green", command=lambda: self.save_changes_repair())
        save_changes_button.grid(row=0, column=1, pady=5, padx=10, sticky="ew")

        del_repair_button = customtkinter.CTkButton(master=self, text="Удалить", hover_color="red", command=lambda: self.delete_repair())
        del_repair_button.grid(row=0, column=2, pady=5, padx=10, sticky="ew")

    def add_repair(self):
        pass

    def save_changes_repair(self):
        pass

    def delete_repair(self):
        pass


if __name__ == "__main__":
    app = Repair()
    app.mainloop()
