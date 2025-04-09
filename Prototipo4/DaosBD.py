import mysql.connector
class DAOUserMysql:
    def __init__(self):
        self.coneccion = mysql.connector.connect(
            host= "localhost",
            user="root",
            password="root",
            database="tapatapp"
        )
        self.cursor = self.coneccion.cursor()