import customtkinter
from dataBase import *
import os
import shutil
from tkinter import filedialog
from ctkcomponents import *
from CTkMessagebox import CTkMessagebox
from hPyT import *

# Загрузка информации о базе данных из файла
with open('database_info.txt', 'r') as file:
    db_info = file.read().strip()

# Разделение информации о базе данных на части
db_info_parts = db_info.split(', ')

# Создание экземпляра менеджера базы данных
db_manager = DatabaseManager(db_info_parts[0], db_info_parts[1])


class PhotoViewer(customtkinter.CTkToplevel):
    """Класс для просмотра фотографий."""

    def __init__(self, *args, basic_id=None, **kwargs):
        """
                Инициализирует окно просмотра фотографий.

                Args:
                    *args: Позиционные аргументы.
                    basic_id (int): Идентификатор основной информации о фото.
                    **kwargs: Аргументы ключевых слов.
                """
        super().__init__(*args, **kwargs)
        photo_id = basic_id
        self.PhotoView(photo_id)

    def PhotoView(self, photo_id):
        """
        Просмотр фотографий.

        Args:
            photo_id (int): Идентификатор фотографии.
        """
        try:
            if hasattr(self, 'additionalWIN') and self.additionalWIN.winfo_exists():
                self.additionalWIN.focus()
                return

            self.photo_id = photo_id

            self.geometry("460x730")
            self.minsize(460, 730)
            self.maxsize(460, 730)
            maximize_minimize_button.hide(self)
            self.title(f"Просмотр фото для {self.photo_id}")
            self.focus()
            images = db_manager.get_data("photo", "*", f"basic_info_id = {self.photo_id}")
            image_paths = self.get_image_paths(images)
            self.rowconfigure(1, weight=1)
            self.frame_p = customtkinter.CTkFrame(master=self, width=300)
            self.frame_p.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
            self.frame_p.columnconfigure(0, weight=1)
            self.frame_p.rowconfigure(0, weight=1)

            if images:
                self.update_carousel()

            label = customtkinter.CTkLabel(master=self.frame_p, text="Добавить фото", fg_color="gray30", font=("Arial", 12))
            label.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

            AddPhotoButton = customtkinter.CTkButton(master=self.frame_p, text="Выбрать и добавить", hover_color="green",
                                                     command=lambda: self.AddPic())
            AddPhotoButton.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

            self.frame_l = customtkinter.CTkFrame(master=self, width=300)
            self.frame_l.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
            self.frame_l.columnconfigure(0, weight=1)

            label2 = customtkinter.CTkLabel(master=self.frame_l, text="Удалить фото", fg_color="gray30", font=("Arial", 12))
            label2.grid(row=4, column=0, padx=10, columnspan=3, pady=10, sticky="ew")

            label3 = customtkinter.CTkLabel(master=self.frame_l, text="Выберите фото", font=("Arial", 12))
            label3.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

            self.combobox1 = customtkinter.CTkComboBox(master=self.frame_l, values=[" "], state="readonly")
            self.combobox1.grid(row=5, column=1, padx=10, pady=10, sticky="ew")
            self.FillComboBoxes()

            ViewPhotoButton = customtkinter.CTkButton(master=self.frame_l, text="Просмотреть", command=lambda: self.OpenPic())
            ViewPhotoButton.grid(row=5, column=2, pady=10, padx=10, sticky="ew")

            DellPhotoButton = customtkinter.CTkButton(master=self.frame_l, text="Удалить фото", hover_color="red",
                                                      command=lambda: self.DelPic())
            DellPhotoButton.grid(row=6, column=0, pady=10, columnspan=3, padx=10, sticky="ew")

        except Exception as e:
            print(f"Exception in PhotoViewer: {e}")

    def get_image_paths(self, photo_data):
        """
        Получает пути к изображениям.

        Args:
            photo_data (list): Данные о фотографиях.

        Returns:
            list: Пути к изображениям.
        """
        return [os.path.join("images", photo[2]) for photo in photo_data]

    def update_carousel(self):
        """Обновляет карусель изображений."""
        images = db_manager.get_data("photo", "*", f"basic_info_id = {self.photo_id}")
        image_paths = self.get_image_paths(images)
        my_carousel = CTkCarousel(master=self.frame_p, img_list=image_paths, width=400, height=400, img_radius=25)
        my_carousel.grid(row=0, column=0, padx=20, pady=20, columnspan=3)

    def OpenPic(self):
        """Открывает выбранное изображение."""
        curval = self.combobox1.get()
        path = os.path.join("images", curval)
        os.startfile(path)

    def AddPic(self):
        """Добавляет новое изображение."""
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Изображения", "*.jpg;*.jpeg;*.png")]
        )
        if file_path:
            try:
                file_name = os.path.basename(file_path)
                target_file_path = os.path.join("images", file_name)
                shutil.copy(file_path, "images")
                db_manager.insert_data("photo", "basic_info_id, path", f"{self.photo_id}, '{file_name}'")
                self.FillComboBoxes()
                self.update_carousel()
                CTkMessagebox(title="Успех", message="Фото успешно добавлено!", icon="check", option_1="Ok")
            except Exception as e:
                CTkMessagebox(title="Ошибка", message="Ошибка при открытии изображения.", icon="cancel")

    def DelPic(self):
        """Удаляет выбранное изображение."""
        try:
            curval = self.combobox1.get()
            db_manager.delete_data("photo", f"path = '{curval}'")
            path = os.path.join("images", curval)
            os.remove(path)
            CTkMessagebox(title="Успех", message="Фото успешно удалено!", icon="check", option_1="Ok")
            self.FillComboBoxes()
            self.update_carousel()
        except IOError as e:
            CTkMessagebox(title="Ошибка", message="Во время удаления произошла ошибка!", icon="cancel")
            return False

    def FillComboBoxes(self):
        """Заполняет выпадающий список фотографий."""
        ToComboBoxOne = db_manager.get_data("photo", "*", f"basic_info_id = {self.photo_id}")
        if not ToComboBoxOne:
            self.combobox1.configure(values=[" "])
            return
        sasha = [str(data[2]) for data in ToComboBoxOne]
        self.combobox1.configure(values=sasha)
        self.update()
