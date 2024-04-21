import customtkinter

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

        self.first = FirstFrameForChoose(self.frame)
        self.first.grid(row=0, column=0, padx=10, pady=10, sticky="ew")


class FirstFrameForChoose(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure((0,1),weight=1)
        self.configure(border_color="dodgerblue", border_width=3)
        customtkinter.CTkLabel(master=self, text="Филиал").grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        customtkinter.CTkLabel(master=self, text="Cтруктурное подразделение").grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        customtkinter.CTkLabel(master=self, text="Тип устройства").grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        data = db_manager.get_data("branch_office", "name", "")
        data = [str(row[0]) for row in data]
        self.combobox1_branch_office = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly", command=self.load_data)
        self.combobox1_branch_office.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        CTkToolTip(self.combobox1_branch_office, message="Выберите филиал.")
        self.FillComboBox(self.combobox1_branch_office, data)

        self.combobox2_structural_unit = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly", command=self.load_second_data)
        self.combobox2_structural_unit.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        CTkToolTip(self.combobox2_structural_unit, message="Выберите структурное подразделение.")

        self.combobox3_type_of_device = customtkinter.CTkComboBox(master=self, values=[" "], state="readonly", command=self.load_main_data)
        self.combobox3_type_of_device.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        CTkToolTip(self.combobox3_type_of_device, message="Выберите тип устройства.")

    def load_main_data(self, choice):
        type_of_device_id = db_manager.get_data("type_of_device", "id", f"name = '{choice}'")[0][0]
        all_basic_info = db_manager.get_data("basic_info", "*", f"type_of_device_id = {type_of_device_id}")
        print(all_basic_info)


        #all_repairs_id = db_manager.get_data("repair", "id", f"basic_info_id = {type_of_device_id}")[0][0]



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


if __name__ == "__main__":
    app = Repair()
    app.mainloop()
