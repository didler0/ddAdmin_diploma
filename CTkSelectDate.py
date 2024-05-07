import customtkinter
from tkcalendar import Calendar
from hPyT import *
from PIL import Image
import os


class SelectDate(customtkinter.CTkFrame):
    """
        Класс SelectDate представляет виджет выбора даты, основанный на CTkFrame.

        Атрибуты:
            master: Родительский виджет, в котором будет размещен SelectDate.
            label_text (str): Текст для метки, отображаемой над полем выбора даты.
            DataStart_entry: Поле ввода для отображения и ввода выбранной даты.
            image_icon_image: Иконка для кнопки выбора даты.
            CalendarOpenButton: Кнопка для открытия календаря.

        Методы:
            __init__(self, master, label_text, *args, **kwargs): Конструктор класса. Инициализирует виджет выбора даты.
            get_current_date(self): Возвращает текущую выбранную дату.
            clear_entry(self): Очищает поле ввода.
            select_date(self, entry): Открывает календарь для выбора даты и вставляет выбранную дату в поле ввода.
        """

    def __init__(self, master, label_text, *args, **kwargs):
        """
        Инициализация виджета выбора даты.

        Аргументы:
            master: Родительский виджет, в котором будет размещен SelectDate.
            label_text (str): Текст для метки, отображаемой над полем выбора даты.
            *args, **kwargs: Дополнительные аргументы для родительского класса.
        """
        super().__init__(master, *args, **kwargs)
        self.configure(border_color="dodgerblue", border_width=3)
        self.grid_columnconfigure((0, 2), weight=0)  # кнопки не расширяются
        self.grid_columnconfigure(2, weight=1)  # поле ввода расширяется

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))

        customtkinter.CTkLabel(master=self, text=label_text).grid(row=1, column=0, padx=10, columnspan=4, pady=10,
                                                                  sticky="ew")

        self.DataStart_entry = customtkinter.CTkEntry(master=self, placeholder_text="ГГГГ-ММ-ДД")
        self.DataStart_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.image_icon_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "resources/calendarICO.png")),
            size=(20, 20))
        self.CalendarOpenButton = customtkinter.CTkButton(master=self, text="Выбрать дату",
                                                          image=self.image_icon_image,
                                                          command=lambda: self.select_date(self.DataStart_entry))
        self.CalendarOpenButton.grid(row=2, column=2, pady=5, padx=10, sticky="ew")

    def get_current_date(self):
        """
        Возвращает текущую выбранную дату.

        Возвращает:
            str: Текущая выбранная дата в формате строки.
        """
        return self.DataStart_entry.get()

    def clear_entry(self):
        """
               Очищает поле ввода выбранной даты.
        """
        self.DataStart_entry.delete(0, customtkinter.END)

    def select_date(self, entry):
        """
                Открывает календарь для выбора даты и вставляет выбранную дату в поле ввода.

                Аргументы:
                    entry: Поле ввода, в которое будет вставлена выбранная дата.
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
            cal = Calendar(self.additionalWIN, selectmode='day', date_pattern="yyyy-mm-dd")
            def set_date(selected_entry):
                def inner():
                    selected_date = cal.get_date()
                    selected_entry.delete(0, 'end')
                    selected_entry.insert(0, selected_date)
                    self.additionalWIN.destroy()
                return inner
            cal.pack()
            cal.bind('<<CalendarSelected>>', lambda event, entry=entry: set_date(entry)())
        except Exception as e:
            print(f"Exception in SelecTData: {e}")
