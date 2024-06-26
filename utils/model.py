from mysql import connector

class Database(object):
    def __init__(self, user, password="",host='localhost', databaseName="leaveManagement") -> None:
        self.host=host
        self.user=user
        self.password=password
        self.database=databaseName
        
    def connectDB(self):
        try:
            database=connector.connect(host=self.host,
                                   user=self.user,
                                   password=self.password,
                                   database=self.database)
        except Exception as e:
            raise e
        
            
        

