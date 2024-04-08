import customtkinter
import tkinter
import re
from dataBase import *
from CTkMessagebox import CTkMessagebox
from hPyT import *

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

db_manager = DatabaseManager('DDLAPTOP\\SQLEXPRESS', 'PCC')


def switch_event(switch_var):
    print("switch toggled, current value:", switch_var.get())


class AddDevice_(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_device = None
        self.tabview = None
        self.widgetsDescription = []
        self.create_widgets()
        maximize_minimize_button.hide(self)

    def create_widgets(self):
        self.title("Add Computer")
        self.geometry("600x595")
        self.minsize(495, 635)
        self.maxsize(495, 635)

        self.frame = customtkinter.CTkScrollableFrame(self, height=520)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=4)
        self.columnconfigure((0, 1, 2), weight=0)
        self.frame.rowconfigure(0, weight=1)
        self.tabview = customtkinter.CTkTabview(master=self.frame)
        self.tabview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.tabview.add("Базовая информация")
        self.tabview.add("Детальное описание")
        self.tabview.add("Компоненты")

        # Define labels and corresponding widgets
        labels_text_ru = ["IP Адрес", "Название", "Сетевое имя", "Тип устройства", "Место установки", "Описание",
                          "Материально ответственный", "Филиал", "Структурное подразделение"]

        for i, text in enumerate(labels_text_ru):
            label = customtkinter.CTkLabel(master=self.tabview.tab("Базовая информация"), text=text, font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=10, sticky="ew")

            widget = None
            if text in ["IP Адрес", "Сетевое имя"]:
                widget = customtkinter.CTkEntry(master=self.tabview.tab("Базовая информация"), placeholder_text=text)
            elif text == "Тип устройства":
                widget = customtkinter.CTkComboBox(master=self.tabview.tab("Базовая информация"), values=[" "], state="readonly")
                self.FillComboBox(widget, db_manager.get_data("type_of_device", "*", ""))
            else:
                widget = customtkinter.CTkTextbox(master=self.tabview.tab("Базовая информация"), height=50)

            widget.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
            self.widgetsDescription.append(widget)

        # Add type of device entry and buttons
        customtkinter.CTkLabel(master=self, text="Добавить тип устройства").grid(row=2, column=0, pady=5, padx=10,
                                                                                 sticky="ew")
        type_device = customtkinter.CTkEntry(master=self, placeholder_text="Тип устройства")
        type_device.grid(row=2, column=1, pady=5, padx=10, sticky="ew")

        customtkinter.CTkButton(master=self, text="+", command=lambda: self.add_type_of_device(type_device,self.widgetsDescription)).grid(row=2, column=3, pady=5,
                                                                                                                  padx=10, sticky="ew")
        customtkinter.CTkButton(master=self, text="Добавить", command=lambda: self.AddPcAll()).grid(row=3, column=0,
                                                                                                    columnspan=4, pady=5,
                                                                                                    padx=10, sticky="ew")

    def FillComboBox(self, combobox1, ToComboBoxOne):
        if not ToComboBoxOne:
            # Если список пуст, установите пустое значение в combobox
            combobox1.configure(values=[" "])
            return
        data = [str(data[1]) for data in ToComboBoxOne]
        combobox1.configure(values=data)
        self.update()

    def add_type_of_device(self, entry, widgetsDescription):
        data = entry.get()
        print(data)
        for widget in widgetsDescription:
            if isinstance(widget, customtkinter.CTkComboBox) and data!=None:
                self.FillComboBox(widget, db_manager.get_data("type_of_device", "*", ""))
                widget.delete(0,customtkinter.END)
                db_manager.insert_data("type_of_device", "[name]", f"'{data}'")
                CTkMessagebox(title="Успех",message="Новый тип устройства успешно добавлен!",icon="check", option_1="Ok")
                self.update()
            else:
                CTkMessagebox(title="Ошибка", message="Ошибка.", icon="cancel")
                return
    #из вс кода экзмпле там из него изобрести велосипед и будет классно



if __name__ == "__main__":
    root = tkinter.Tk()
    app = AddDevice_(root)
    root.mainloop()
