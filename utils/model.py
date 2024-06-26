from mysql import connector

class Database(object):
    def __init__(self, user, password="",host='localhost', databaseName="leaveManagement") -> None:
        self.host=host
        self.user=user
        self.password=password
        self.databaseName=databaseName
        
    def connectDB(self):
        try:
            database=connector.connect(host=self.host,
                                   user=self.user,
                                   password=self.password,
                                   database=self.databaseName)
            return database
        except Exception as e:
            raise e
        
    def createDatabaseStructure(self):
        try:
            database=connector.connect(host=self.host,
                                   user=self.user,
                                   password=self.password)
            cursor=database.cursor()
            cursor.execute(f'CREATE IF NOT EXISTS DATABASE {self.databaseName}')
            
            database=self.connectDB()
            
            cursor=database.cursor()
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INT PRIMARY KEY,
                    employee_number INT UNIQUE,
                    password TEXT,
                    annual_leaves INT,
                    casual_leaves INT,
                    short_leaves INT,
                    roster_start_time DATETIME,
                    roster_end_time DATETIME
            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS leaves (
                                id INT PRIMARY KEY,
                                employee_id INT,
                                leave_type VARCHAR(10),
                                start_date DATETIME,
                                end_date DATETIME,
                                short_leave_time DATETIME,
                                status VARCHAR(10),
                                FOREIGN KEY(employee_id) REFERENCES employees(id)
            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                                id INT PRIMARY KEY,
                                username VARCHAR(20) UNIQUE,
                                password VARCHAR(20)
            )''')
            
        except Exception as e:
            raise e

        finally:
            cursor.close()
            
        
        
            
        

