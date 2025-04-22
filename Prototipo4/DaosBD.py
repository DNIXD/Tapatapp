import mysql.connector

class DAOUserMysql:
    def __init__(self):
        self.coneccion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="tapatapp"
        )
        self.cursor = self.coneccion.cursor(dictionary=True)  # Usar dictionary=True para obtener resultados como diccionarios

    def get_all_users(self):
        """Obtiene todos los usuarios de la tabla User"""
        try:
            query = "SELECT * FROM User"
            self.cursor.execute(query)
            users = self.cursor.fetchall()  # Obtener todos los resultados
            return users
        except mysql.connector.Error as err:
            print(f"Error al obtener usuarios: {err}")
            return None

    def close_connection(self):
        """Cierra la conexión a la base de datos"""
        if self.cursor:
            self.cursor.close()
        if self.coneccion:
            self.coneccion.close()

# Ejemplo de uso
if __name__ == "__main__":
    dao = DAOUserMysql()
    users = dao.get_all_users()
    if users:
        for user in users:
            print(user)
    dao.close_connection()