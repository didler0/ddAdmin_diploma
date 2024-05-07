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
                                    name NVARCHAR(255) UNIQUE NOT NULL
                                )''')

            # Создание таблицы structural_unit
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[structural_unit]') AND type in (N'U'))
                                CREATE TABLE structural_unit (
                                    id INT PRIMARY KEY IDENTITY(1,1),
                                    name NVARCHAR(255) UNIQUE NOT NULL
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
                                                name NVARCHAR(255) UNIQUE NOT NULL
                                            )''')

            # Создание таблицы place_of_installation
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[place_of_installation]') AND type in (N'U'))
                                                        CREATE TABLE place_of_installation (
                                                            id INT PRIMARY KEY IDENTITY(1,1),
                                                            name NVARCHAR(255) UNIQUE NOT NULL
                                                        )''')
            # Создание таблицы material_resp_person
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[material_resp_person]') AND type in (N'U'))
                                                                    CREATE TABLE material_resp_person (
                                                                        id INT PRIMARY KEY IDENTITY(1,1),
                                                                        name NVARCHAR(255) UNIQUE NOT NULL
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
                                    component_id INT NOT NULL,
                                    inventory_number NVARCHAR(MAX) NOT NULL,
                                    serial_number NVARCHAR(MAX) NOT NULL,
                                    mac_address NVARCHAR(MAX) NOT NULL,
                                    oper_system NVARCHAR(MAX) NOT NULL,
                                    year_of_purchase INT NOT NULL,
                                    month_of_warranty INT NOT NULL,
                                    FOREIGN KEY(component_id) REFERENCES component(id) ON DELETE CASCADE ON UPDATE CASCADE
                                )''')

            # Создание таблицы basic_info
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[basic_info]') AND type in (N'U'))
                                CREATE TABLE basic_info (
                                    id INT PRIMARY KEY IDENTITY(1,1),
                                    ip NVARCHAR(15) NOT NULL,
                                    name NVARCHAR(MAX) NOT NULL,
                                    network_name NVARCHAR(MAX) NOT NULL,
                                    type_of_device_id INT NOT NULL,
                                    place_of_installation_id INT NOT NULL,
                                    description NVARCHAR(MAX)NOT NULL,
                                    material_resp_person_id INT NOT NULL,
                                    last_status BIT,
                                    data_status datetime,
                                    last_repair DATE,
                                    detail_info_id INT NOT NULL,
                                    branch_id INT NOT NULL,
                                    structural_unit_id INT NOT NULL,
                                    FOREIGN KEY(detail_info_id) REFERENCES detail_info(id) ON DELETE CASCADE ON UPDATE CASCADE,
                                    FOREIGN KEY(branch_id) REFERENCES branch_office(id) ON DELETE CASCADE ON UPDATE CASCADE,
                                    FOREIGN KEY(structural_unit_id) REFERENCES structural_unit(id) ON DELETE CASCADE ON UPDATE CASCADE,
                                    FOREIGN KEY(type_of_device_id) REFERENCES type_of_device(id) ON DELETE CASCADE ON UPDATE CASCADE,
                                    FOREIGN KEY(place_of_installation_id) REFERENCES place_of_installation(id) ON DELETE CASCADE ON UPDATE CASCADE,
                                    FOREIGN KEY(material_resp_person_id) REFERENCES material_resp_person(id) ON DELETE CASCADE ON UPDATE CASCADE
                                )''')

            # Создание таблицы repair
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[repair]') AND type in (N'U'))
                                CREATE TABLE repair (
                                    id INT PRIMARY KEY IDENTITY(1,1),
                                    basic_info_id INT NOT NULL,
                                    description NVARCHAR(100) NOT NULL,
                                    repair_date DATE NOT NULL,
                                    document_path NVARCHAR(100),
                                    FOREIGN KEY(basic_info_id) REFERENCES basic_info(id) ON DELETE CASCADE ON UPDATE CASCADE
                                )''')

            # Создание таблицы photo
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[photo]') AND type in (N'U'))
                                CREATE TABLE photo (
                                    id INT PRIMARY KEY IDENTITY(1,1),
                                    basic_info_id INT NOT NULL,
                                    path NVARCHAR(MAX) NOT NULL,
                                    FOREIGN KEY(basic_info_id) REFERENCES basic_info(id) ON DELETE CASCADE ON UPDATE CASCADE
                                )''')

            # Создание таблицы status
            self.cur.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[status]') AND type in (N'U'))
                                CREATE TABLE status (
                                    id INT PRIMARY KEY IDENTITY(1,1),
                                    basic_info_id INT ,
                                    status_ INT ,
                                    status_date DATETIME ,
                                    FOREIGN KEY(basic_info_id) REFERENCES basic_info(id) ON DELETE CASCADE ON UPDATE CASCADE
                                )''')

            self.conn.commit()

            self.create_stored_procedure_get_structural_units()
            self.create_stored_procedure_get_info_by_branch_and_structural_unit()
            self.create_stored_procedure_GetBasicInfoStatusBetweenDates()
            self.create_trigger()
            self.create_trigger_last_repair()
        except pyodbc.Error as e:
            print("An error occurred:", e)
            self.conn.rollback()
            raise

    def create_stored_procedure_get_structural_units(self):
        """
        Метод для создания хранимой процедуры GetStructuralUnits.

        Returns:
            bool: True, если процедура была успешно создана, в противном случае - False.
        """
        try:
            procedure_query = """
                CREATE PROCEDURE GetStructuralUnits @branchOfficeName NVARCHAR(255)
                AS
                BEGIN
                    DECLARE @branchOfficeId INT

                    -- Получить идентификатор филиала по его имени
                    SELECT @branchOfficeId = id
                    FROM branch_office
                    WHERE name = @branchOfficeName

                    -- Получить структурные подразделения для данного филиала
                    SELECT su.name
                    FROM branch_structural_unit bsu
                    JOIN structural_unit su ON bsu.structural_unit_id = su.id
                    WHERE bsu.branch_office_id = @branchOfficeId
                END
            """
            self.cur.execute(procedure_query)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            print("An error occurred while creating stored procedure:", e)
            self.conn.rollback()
            return False

    def create_stored_procedure_GetBasicInfoStatusBetweenDates(self):
        """
        Метод для создания хранимой процедуры GetBasicInfoStatusBetweenDates.

        Returns:
            bool: True, если процедура была успешно создана, в противном случае - False.
        """
        try:
            procedure_query = """
                            CREATE PROCEDURE GetBasicInfoStatusBetweenDates
                @date_start DATE,
                @date_end DATE
            AS
            BEGIN
                SELECT S.basic_info_id,
                       S.status_,
                       S.status_date,
                       B.name AS basic_info_name,
                       P.name AS place_of_installation_name
                FROM status S
                JOIN basic_info B ON B.id = S.basic_info_id
                JOIN place_of_installation P ON P.id = B.place_of_installation_id
                WHERE S.status_date BETWEEN @date_start AND @date_end;
            END
            """
            self.cur.execute(procedure_query)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            print("An error occurred while creating stored procedure:", e)
            self.conn.rollback()
            return False

    def create_stored_procedure_get_info_by_branch_and_structural_unit(self):
        """
                Метод для создания хранимой процедуры GetInfoByBranchAndStructuralUnit.

                Returns:
                    bool: True, если процедура была успешно создана, в противном случае - False.
                """
        try:
            procedure_query = """
                        CREATE PROCEDURE GetInfoByBranchAndStructuralUnit
    @branch_id INT,
    @structural_unit_id INT
AS
BEGIN
    SELECT 
        bi.id,
        bi.ip,
        bi.name,
        bi.network_name,
        td.name AS type_of_device_name,
        pi.name AS place_of_installation_name,
        mrp.name AS material_resp_person_name,
        bi.last_status,
        bi.data_status,
        bi.last_repair,
		bi.detail_info_id
    FROM 
        [dbo].[basic_info] bi
    LEFT JOIN 
        [dbo].[type_of_device] td ON bi.type_of_device_id = td.id
    LEFT JOIN 
        [dbo].[place_of_installation] pi ON bi.place_of_installation_id = pi.id
    LEFT JOIN 
        [dbo].[material_resp_person] mrp ON bi.material_resp_person_id = mrp.id
    WHERE 
        bi.branch_id = @branch_id
        AND bi.structural_unit_id = @structural_unit_id;
END

                    """
            self.cur.execute(procedure_query)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            print("An error occurred while creating stored procedure:", e)
            self.conn.rollback()
            return False

    def create_trigger_last_repair(self):
        try:
            # Проверка наличия триггера trg_StatusUpdate
            self.cur.execute("SELECT COUNT(*) FROM sys.triggers WHERE name = 'update_last_repair'")
            if self.cur.fetchone()[0] == 0:
                # Создание триггера trg_StatusUpdate (если его нет)
                self.cur.execute('''
                    CREATE TRIGGER update_last_repair
                    ON repair
                    AFTER INSERT
                    AS
                    BEGIN
                        SET NOCOUNT ON;
                    
                        -- Обновляем значение поля last_repair в таблице basic_info для каждой вставленной записи в repair
                        UPDATE basic_info
                        SET last_repair = i.repair_date
                        FROM basic_info b
                        INNER JOIN inserted i ON b.id = i.basic_info_id;
                    END;

                ''')
                self.conn.commit()
                print("Trigger update_last_repair created successfully.")
        except Exception as e:
            print(f"Error creating trigger: {str(e)}")

    def create_trigger(self):
        try:
            # Проверка наличия триггера trg_StatusUpdate
            self.cur.execute("SELECT COUNT(*) FROM sys.triggers WHERE name = 'trg_StatusUpdate'")
            if self.cur.fetchone()[0] == 0:
                # Создание триггера trg_StatusUpdate (если его нет)
                self.cur.execute('''
                    CREATE TRIGGER trg_StatusUpdate
                    ON basic_info
                    AFTER INSERT, UPDATE
                    AS
                    BEGIN
                        DECLARE @ip VARCHAR(15)
                        DECLARE @last_status BIT
                        DECLARE @data_status DATETIME

                        SELECT @ip = inserted.ip, @last_status = inserted.last_status, @data_status = inserted.data_status
                        FROM inserted

                        INSERT INTO status (basic_info_id, status_, status_date)
                        SELECT id, @last_status, @data_status
                        FROM basic_info
                        WHERE ip = @ip
                    END
                ''')
                self.conn.commit()
                print("Trigger trg_StatusUpdate created successfully.")
        except Exception as e:
            print(f"Error creating trigger: {str(e)}")

    def exec_procedure(self, procedure_name, *args):
        """
        Метод для выполнения хранимой процедуры с передачей аргументов.

        Args:
            procedure_name (str): Имя хранимой процедуры.
            *args: Аргументы, передаваемые в хранимую процедуру.

        Returns:
            list: Результат выполнения процедуры.
        """
        try:
            # Создаем строку для вызова процедуры с переданными аргументами
            placeholders = ', '.join('?' for _ in args)
            query = f"EXEC {procedure_name} {placeholders}"
            # Выполняем процедуру и возвращаем результат
            self.cur.execute(query, args)
            return self.cur.fetchall()
        except pyodbc.Error as e:
            print("An error occurred while executing stored procedure:", e)
            return []

    def check_structural_unit_exists(self, str_unit):
        query = "SELECT COUNT(*) FROM structural_unit WHERE name = ?"
        self.cur.execute(query, (str_unit,))
        result = self.cur.fetchone()[0]
        return result > 0

    def check_structural_unit_assigned_to_branch(self, str_unit, branch_office):
        query = "SELECT COUNT(*) FROM branch_structural_unit bsu \
                 JOIN branch_office bo ON bsu.branch_office_id = bo.id \
                 JOIN structural_unit su ON bsu.structural_unit_id = su.id \
                 WHERE bo.name = ? AND su.name = ?"
        self.cur.execute(query, (branch_office, str_unit))
        result = self.cur.fetchone()[0]
        return result > 0

    def close_connection(self):
        """Метод для закрытия соединения с базой данных"""
        self.conn.close()
        print("closed")

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
            bla = self.cur.fetchall()
            return bla
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
            print(f"успещно добавлено {values}")
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
                               description, material_resp_person_id, branch_id, structural_unit_id, detail_info_id):
        try:
            query = f"INSERT INTO basic_info (ip, name, network_name, type_of_device_id, place_of_installation_id, " \
                    f"description, material_resp_person_id,detail_info_id, " \
                    f"branch_id, structural_unit_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            self.cur.execute(query, (ip, name, network_name, type_of_device_id, place_of_installation_id,
                                     description, material_resp_person_id,
                                     detail_info_id, branch_id, structural_unit_id))
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            print("An error occurred:", e)
            self.conn.rollback()
            return False

    def get_last_id(self, table):
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

    def get_data_by_branch_and_structural_unit(self, branch_name, structural_unit_name):
        """
        Получение данных по филиалу и структурному подразделению.

        Args:
            branch_name (str): Название филиала.
            structural_unit_name (str): Название структурного подразделения.

        Returns:
            list: Список данных, соответствующих указанным филиалу и структурному подразделению.
        """
        try:
            # SQL-запрос для получения данных
            query = """
                    SELECT * FROM basic_info
                    INNER JOIN branch_office ON basic_info.branch_id = branch_office.id
                    INNER JOIN structural_unit ON basic_info.structural_unit_id = structural_unit.id
                    WHERE branch_office.name = ? AND structural_unit.name = ?
                    """

            # Выполнение SQL-запроса с передачей параметров
            self.cur.execute(query, (branch_name, structural_unit_name))

            # Получение результатов запроса
            data = self.cur.fetchall()

            return data

        except pyodbc.Error as e:
            print("An error occurred:", e)
            return []

    def get_basic_info_by_branch_and_structural_unit(self, branch_name, unit_name):
        """
        Получение данных из таблицы basic_info по заданному филиалу и структурному подразделению.

        Args:
            branch_name: Название филиала.
            unit_name: Название структурного подразделения.

        Returns:
            list: Список кортежей с данными из таблицы basic_info.
        """
        try:
            # Выполнение запроса SQL для получения данных
            query = """
                SELECT * FROM basic_info
                INNER JOIN branch_office ON basic_info.branch_id = branch_office.id
                INNER JOIN structural_unit ON basic_info.structural_unit_id = structural_unit.id
                WHERE branch_office.name = ? AND structural_unit.name = ?
            """
            self.cur.execute(query, (branch_name, unit_name))
            data = self.cur.fetchall()
            return data
        except pyodbc.Error as e:
            print("An error occurred:", e)
            raise

    def update(self, table_name, set_clause, where_clause):
        """
        Метод для обновления данных в таблице.

        Args:
            table_name (str): Имя таблицы, в которой нужно обновить данные.
            set_clause (str): Выражение SET для обновления значений.
            where_clause (str): Условие WHERE для выбора строк для обновления.

        Returns:
            bool: True, если обновление прошло успешно, False в противном случае.
        """
        try:
            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
            self.cur.execute(query)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            print("An error occurred while updating data:", e)
            self.conn.rollback()
            return False

    def add_status(self, ip_address, last_status):
        try:
            # Выполняем SQL-запрос для добавления нового статуса
            query = f'''
            UPDATE basic_info
            SET last_status = {int(last_status)}, data_status = GETDATE()
            WHERE ip = '{ip_address}'
            '''
            self.cur.execute(query)
            self.conn.commit()
            print(f"Status for IP {ip_address} updated successfully.")
            self.conn.commit()
        except Exception as e:
            print(f"Error adding status: {str(e)}")

    def update_basic_info(self, ip, name, network_name, type_of_device_id, place_of_installation_id, description,
                          material_resp_person_id, branch_id,
                          structural_unit_id, id_value):
        """
        Метод для обновления данных в таблице basic_info.

        Args:
            ip (str): IP-адрес.
            name (str): Название.
            network_name (str): Сетевое название.
            type_of_device_id (int): ID типа устройства.
            place_of_installation_id (int): ID места установки.
            description (str): Описание.
            material_resp_person_id (int): ID материально ответственного лица.
            branch_id (int): ID филиала.
            structural_unit_id (int): ID структурного подразделения.
            id_value (int): Значение id для условия WHERE.

        Returns:
            bool: True, если обновление прошло успешно, False в противном случае.
        """
        try:
            # Формирование запроса на обновление
            set_clause = f"ip = '{ip}', name = '{name}', network_name = '{network_name}', type_of_device_id = {type_of_device_id}, place_of_installation_id = {place_of_installation_id}, description = '{description}', material_resp_person_id = {material_resp_person_id}, branch_id = {branch_id}, structural_unit_id = {structural_unit_id}"
            query = f"UPDATE basic_info SET {set_clause} WHERE id = {id_value}"

            # Выполнение запроса
            self.cur.execute(query)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            print("An error occurred while updating data in basic_info:", e)
            self.conn.rollback()
            return False

    def update_detail_info(self, inventory_number, serial_number, mac_address, oper_system, year_of_purchase,
                           month_of_warranty, id_value):
        """
        Метод для обновления данных в таблице values_details.

        Args:
            inventory_number (str): Инвентарный номер.
            serial_number (str): Серийный номер.
            mac_address (str): MAC-адрес.
            oper_system (str): Операционная система.
            year_of_purchase (int): Год покупки.
            month_of_warranty (int): Месяц гарантии.
            id_value (int): Значение id для условия WHERE.

        Returns:
            bool: True, если обновление прошло успешно, False в противном случае.
        """
        try:
            # Формирование запроса на обновление
            set_clause = f"inventory_number = '{inventory_number}', serial_number = '{serial_number}', mac_address = '{mac_address}', oper_system = '{oper_system}', year_of_purchase = {year_of_purchase}, month_of_warranty = {month_of_warranty}"
            query = f"UPDATE detail_info SET {set_clause} WHERE id = {id_value}"

            # Выполнение запроса
            self.cur.execute(query)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            print("An error occurred while updating data in values_details:", e)
            self.conn.rollback()
            return False

    def update_component(self, processor, ram, motherboard, gpu, psu, networkCard, cooler, chasis, hdd, ssd, monitor,
                         keyboard, mouse, audio, id_value):
        """
        Метод для обновления данных в таблице component.

        Args:
            processor (str): Процессор.
            ram (str): Оперативная память.
            motherboard (str): Материнская плата.
            gpu (str): Видеокарта.
            psu (str): Блок питания.
            networkCard (str): Сетевая карта.
            cooler (str): Система охлаждения.
            chasis (str): Корпус.
            hdd (str): Жесткий диск.
            ssd (str): SSD-накопитель.
            monitor (str): Монитор.
            keyboard (str): Клавиатура.
            mouse (str): Мышь.
            audio (str): Аудиоустройство.
            id_value (int): Значение id для условия WHERE.

        Returns:
            bool: True, если обновление прошло успешно, False в противном случае.
        """
        try:
            # Формирование запроса на обновление
            set_clause = f"processor = '{processor}', ram = '{ram}', motherboard = '{motherboard}', gpu = '{gpu}', psu = '{psu}', networkCard = '{networkCard}', cooler = '{cooler}', chasis = '{chasis}', hdd = '{hdd}', ssd = '{ssd}', monitor = '{monitor}', keyboard = '{keyboard}', mouse = '{mouse}', audio = '{audio}'"
            set_clause = f"processor = '{processor}', ram = '{ram}', motherboard = '{motherboard}', gpu = '{gpu}', psu = '{psu}', networkCard = '{networkCard}', cooler = '{cooler}', chasis = '{chasis}', hdd = '{hdd}', ssd = '{ssd}', monitor = '{monitor}', keyboard = '{keyboard}', mouse = '{mouse}', audio = '{audio}'"
            query = f"UPDATE component SET {set_clause} WHERE id = {id_value}"

            # Выполнение запроса
            self.cur.execute(query)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            print("An error occurred while updating data in component:", e)
            self.conn.rollback()
            return False
