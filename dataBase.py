from datetime import datetime
import random

import pyodbc


class DatabaseManager:
    def __init__(self, server_name, database_name):
        self.server_name = server_name
        self.database_name = database_name
        self.conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};Trusted_Connection=yes;')
        self.cur = self.conn.cursor()

    def create_tables(self):
        """Метод для проверки наличия таблиц и их создания"""
        try:
            # Создание таблицы branch_office
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[branch_office]') AND type in (N'U'))
                                CREATE TABLE branch_office (
                                    id INT PRIMARY KEY IDENTITY(1,1),
                                    name NVARCHAR(255) UNIQUE
                                )''')

            # Создание таблицы structural_unit
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[structural_unit]') AND type in (N'U'))
                                CREATE TABLE structural_unit (
                                    id INT PRIMARY KEY IDENTITY(1,1),
                                    name NVARCHAR(255) UNIQUE
                                )''')

            # Создание таблицы branch_structural_unit
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[branch_structural_unit]') AND type in (N'U'))
                                            CREATE TABLE branch_structural_unit (
                                                id INT PRIMARY KEY IDENTITY(1,1),
                                                branch_office_id INT,
                                                structural_unit_id INT,
                                                FOREIGN KEY(branch_office_id) REFERENCES branch_office(id) ON DELETE CASCADE ON UPDATE CASCADE,
                                                FOREIGN KEY(structural_unit_id) REFERENCES structural_unit(id) ON DELETE CASCADE ON UPDATE CASCADE
                                            )''')

            # Создание таблицы type_of_device
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[type_of_device]') AND type in (N'U'))
                                            CREATE TABLE type_of_device (
                                                id INT PRIMARY KEY IDENTITY(1,1),
                                                name NVARCHAR(255) UNIQUE
                                            )''')

            # Создание таблицы place_of_installation
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[place_of_installation]') AND type in (N'U'))
                                                        CREATE TABLE place_of_installation (
                                                            id INT PRIMARY KEY IDENTITY(1,1),
                                                            name NVARCHAR(255) UNIQUE
                                                        )''')

            # Создание таблицы component
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[component]') AND type in (N'U'))
                                CREATE TABLE component (
                                    id INT PRIMARY KEY IDENTITY(1,1),
                                    processor NVARCHAR(MAX),
                                    ram NVARCHAR(MAX),
                                    motherboard NVARCHAR(MAX),
                                    gpu NVARCHAR(MAX),
                                    psu NVARCHAR(MAX),
                                    networkCard NVARCHAR(MAX),
                                    cooler NVARCHAR(MAX),
                                    chasis NVARCHAR(MAX),
                                    hdd NVARCHAR(MAX),
                                    ssd NVARCHAR(MAX),
                                    monitor NVARCHAR(MAX),
                                    keyboard NVARCHAR(MAX),
                                    mouse NVARCHAR(MAX),
                                    audio NVARCHAR(MAX)
                                )''')

            # Создание таблицы detail_info
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[detail_info]') AND type in (N'U'))
                                CREATE TABLE detail_info (
                                    id INT PRIMARY KEY IDENTITY(1,1),
                                    component_id INT,
                                    inventory_number NVARCHAR(MAX),
                                    serial_number NVARCHAR(MAX),
                                    mac_address NVARCHAR(MAX),
                                    oper_system NVARCHAR(MAX),
                                    year_of_purchase INT,
                                    month_of_warranty INT,
                                    FOREIGN KEY(component_id) REFERENCES component(id) ON DELETE CASCADE ON UPDATE CASCADE
                                )''')

            # Создание таблицы basic_info
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[basic_info]') AND type in (N'U'))
                                CREATE TABLE basic_info (
                                    id INT PRIMARY KEY IDENTITY(1,1),
                                    ip NVARCHAR(15),
                                    name NVARCHAR(MAX),
                                    network_name NVARCHAR(MAX),
                                    type_of_device_id INT,
                                    place_of_installation_id INT,
                                    description NVARCHAR(MAX),
                                    material_resp_person NVARCHAR(MAX),
                                    last_status BIT,
                                    data_status DATE,
                                    last_repair DATE,
                                    detail_info_id INT,
                                    branch_id INT,
                                    structural_unit_id INT,
                                    FOREIGN KEY(detail_info_id) REFERENCES detail_info(id) ON DELETE CASCADE ON UPDATE CASCADE,
                                    FOREIGN KEY(branch_id) REFERENCES branch_office(id) ON DELETE CASCADE ON UPDATE CASCADE,
                                    FOREIGN KEY(structural_unit_id) REFERENCES structural_unit(id) ON DELETE CASCADE ON UPDATE CASCADE,
                                    FOREIGN KEY(type_of_device_id) REFERENCES type_of_device(id) ON DELETE CASCADE ON UPDATE CASCADE,
                                    FOREIGN KEY(place_of_installation_id) REFERENCES place_of_installation(id) ON DELETE CASCADE ON UPDATE CASCADE
                                )''')

            # Создание таблицы repair
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[repair]') AND type in (N'U'))
                                CREATE TABLE repair (
                                    id INT PRIMARY KEY IDENTITY(1,1),
                                    basic_info_id INT,
                                    description NVARCHAR(100),
                                    repair_date DATE,
                                    document_path NVARCHAR(100),
                                    FOREIGN KEY(basic_info_id) REFERENCES basic_info(id) ON DELETE CASCADE ON UPDATE CASCADE
                                )''')

            # Создание таблицы photo
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[photo]') AND type in (N'U'))
                                CREATE TABLE photo (
                                    id INT PRIMARY KEY IDENTITY(1,1),
                                    basic_info_id INT,
                                    path NVARCHAR(MAX),
                                    FOREIGN KEY(basic_info_id) REFERENCES basic_info(id) ON DELETE CASCADE ON UPDATE CASCADE
                                )''')

            # Создание таблицы status
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[status]') AND type in (N'U'))
                                CREATE TABLE status (
                                    id INT PRIMARY KEY IDENTITY(1,1),
                                    basic_info_id INT,
                                    status_ INT,
                                    status_date DATE,
                                    FOREIGN KEY(basic_info_id) REFERENCES basic_info(id) ON DELETE CASCADE ON UPDATE CASCADE
                                )''')

            self.conn.commit()

        except pyodbc.Error as e:
            print("An error occurred:", e)
            self.conn.rollback()
            raise

    def close_connection(self):
        """Метод для закрытия соединения с базой данных"""
        self.conn.close()
        print("suck")

    def get_data(self, table_name, columns='*', condition=''):
        """
        Универсальный метод для получения данных из таблицы.

        Args:
            table_name (str): Название таблицы, из которой нужно получить данные.
            columns (str, optional): Строка с именами столбцов, которые требуется получить. По умолчанию '*' - все столбцы.
            condition (str, optional): Условие для фильтрации данных. По умолчанию '' - без условия.

        Returns:
            list: Список кортежей с данными из таблицы, удовлетворяющих условию.
        """
        try:
            query = f'SELECT {columns} FROM {table_name}'
            if condition:
                query += f' WHERE {condition}'
            self.cur.execute(query)
            return self.cur.fetchall()
        except pyodbc.Error as e:
            print("An error occurred:", e)
            return []

    def insert_data(self, table_name, columns, values):
        """
        Универсальный метод для добавления данных в таблицу.

        Args:
            table_name (str): Название таблицы, в которую нужно добавить данные.
            columns (str): Строка с именами столбцов, в которые будут вставляться данные.
            values (str): Строка с значениями, которые нужно вставить.

        Returns:
            bool: True, если данные были успешно добавлены, в противном случае - False.
        """
        try:
            query = f'INSERT INTO {table_name} ({columns}) VALUES ({values})'
            self.cur.execute(query)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            print("An error occurred:", e)
            self.conn.rollback()
            return False

    def delete_data(self, table_name, condition=''):
        """
        Универсальный метод для удаления данных из таблицы.

        Args:
            table_name (str): Название таблицы, из которой нужно удалить данные.
            condition (str, optional): Условие для фильтрации данных. По умолчанию '' - без условия.

        Returns:
            bool: True, если данные были успешно удалены, в противном случае - False.
        """
        try:
            query = f'DELETE FROM {table_name}'
            if condition:
                query += f' WHERE {condition}'
            self.cur.execute(query)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            print("An error occurred:", e)
            self.conn.rollback()
            return False

    def insert_data_basic_info(self, ip, name, network_name, type_of_device_id, place_of_installation_id,
                               description, material_resp_person,
                               detail_info_id, branch_id, structural_unit_id):
        try:
            query = f"INSERT INTO basic_info (ip, name, network_name, type_of_device_id, place_of_installation_id, " \
                    f"description, material_resp_person, last_status, data_status, last_repair, detail_info_id, " \
                    f"branch_id, structural_unit_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            self.cur.execute(query, (ip, name, network_name, type_of_device_id, place_of_installation_id,
                                     description, material_resp_person,
                                     detail_info_id, branch_id, structural_unit_id))
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            print("An error occurred:", e)
            self.conn.rollback()
            return False

    def get_last_id(self,table):
        try:
            # Получаем последний добавленный идентификатор
            self.cur.execute(f"SELECT IDENT_CURRENT('{table}')")
            last_id = self.cur.fetchone()[0]
            return last_id
        except Exception as e:
            print(f"Error retrieving last basic_info id: {str(e)}")
            return None
    def insert_data_detail_info(self, component_id, inventory_number, serial_number, mac_address, oper_system,
                                year_of_purchase, month_of_warranty):
        try:
            query = f"INSERT INTO detail_info (component_id, inventory_number, serial_number, mac_address, oper_system, " \
                    f"year_of_purchase, month_of_warranty) VALUES (?, ?, ?, ?, ?, ?, ?)"
            self.cur.execute(query, (component_id, inventory_number, serial_number, mac_address, oper_system,
                                     year_of_purchase, month_of_warranty))
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            print("An error occurred:", e)
            self.conn.rollback()
            return False

    def insert_data_component(self, processor, ram, motherboard, gpu, psu, networkCard, cooler, chasis,
                              hdd, ssd, monitor, keyboard, mouse, audio):
        try:
            query = "INSERT INTO component (processor, ram, motherboard, gpu, psu, networkCard, cooler, chasis, " \
                    "hdd, ssd, monitor, keyboard, mouse, audio) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            self.cur.execute(query, (processor, ram, motherboard, gpu, psu, networkCard, cooler, chasis,
                                     hdd, ssd, monitor, keyboard, mouse, audio))
            self.conn.commit()

            return True
        except pyodbc.Error as e:
            print("An error occurred:", e)
            self.conn.rollback()
            return False

    def get_unique_branch_struct(self):
        """
        Метод для получения уникальных пар филиалов и подразделений.

        Returns:
            tuple: Кортеж из двух списков, первый содержит названия филиалов, второй - названия подразделений.
        """
        try:
            query = '''
                SELECT DISTINCT branch_office.name AS branch_name, structural_units.name AS structural_name
                FROM basic_info
                JOIN branch_office ON basic_info.branch_id = branch_office.id
                JOIN structural_units ON basic_info.structural_units_id = structural_units.id
            '''
            self.cur.execute(query)
            results = self.cur.fetchall()

            branch_names = []
            structural_names = []
            for result in results:
                branch_names.append(result[0])  # Добавить название филиала в список
                structural_names.append(result[1])  # Добавить название подразделения в список
            return branch_names, structural_names
        except pyodbc.Error as e:
            print("Произошла ошибка:", e)
            return [], []

    def get_column_names(self, table_name):
        """
        Метод для получения имен всех столбцов в указанной таблице.

        Args:
            table_name (str): Название таблицы.

        Returns:
            list: Список с именами всех столбцов в таблице.
        """
        try:
            self.cur.execute(f"SELECT TOP 1 * FROM {table_name}")
            columns = [column[0] for column in self.cur.description]
            return columns
        except pyodbc.Error as e:
            print("An error occurred:", e)
            return []


