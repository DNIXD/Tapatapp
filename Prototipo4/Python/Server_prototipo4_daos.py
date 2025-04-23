import mysql.connector

class DAOUsers:
    def __init__(self):
        self.coneccion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="tapatapp"
        )
        self.cursor = self.coneccion.cursor(dictionary=True)

    def getUserByID(self, user_id):
        """Obtiene un usuario por ID"""
        try:
            query = "SELECT * FROM User WHERE id = %s"
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener usuario: {err}")
            return None

    def getUserByUsername(self, username):
        """Obtiene un usuario por username"""
        try:
            query = "SELECT * FROM User WHERE username = %s"
            self.cursor.execute(query, (username,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener usuario por username: {err}")
            return None

    def getUserByUsernameAndPassword(self, username, password):
        """Obtiene un usuario por username y password"""
        try:
            query = "SELECT * FROM User WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener usuario por username y password: {err}")
            return None

    def addUser(self, username, password, email):
        """Añade un nuevo usuario a la base de datos"""
        try:
            query = "INSERT INTO User (username, password, email) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (username, password, email))
            self.coneccion.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error al añadir usuario: {err}")
            return None


class DAOChilds:
    def __init__(self):
        self.coneccion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="tapatapp"
        )
        self.cursor = self.coneccion.cursor(dictionary=True)

    def getChildbyUser_ID(self, user_id):
        """Obtiene los niños asociados a un usuario usando la tabla RelationUserChild"""
        try:
            query = """
                SELECT c.* 
                FROM Child c
                JOIN RelationUserChild ruc ON c.id = ruc.child_id
                WHERE ruc.user_id = %s AND ruc.rol_id = 2
            """
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al obtener niños: {err}")
            return None

    def addChild(self, user_id, child_name, sleep_average):
        """Añade un nuevo niño a la base de datos y lo relaciona con un usuario"""
        try:
            # Insertar el niño en la tabla Child
            query = "INSERT INTO Child (child_name, sleep_average) VALUES (%s, %s)"
            self.cursor.execute(query, (child_name, sleep_average))
            child_id = self.cursor.lastrowid

            # Relacionar el niño con el usuario en la tabla RelationUserChild
            relation_query = "INSERT INTO RelationUserChild (user_id, child_id) VALUES (%s, %s)"
            self.cursor.execute(relation_query, (user_id, child_id))
            self.coneccion.commit()

            return child_id
        except mysql.connector.Error as err:
            print(f"Error al añadir niño: {err}")
            return None


class DAOTaps:
    def __init__(self):
        self.coneccion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="tapatapp"
        )
        self.cursor = self.coneccion.cursor(dictionary=True)

    def getTapByChild_ID(self, child_id):
        """Obtiene los taps asociados a un niño"""
        try:
            query = "SELECT * FROM Tap WHERE child_id = %s"
            self.cursor.execute(query, (child_id,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al obtener taps: {err}")
            return None

    def addTap(self, child_id, init, end):
        """Añade un nuevo tap a la base de datos"""
        try:
            query = "INSERT INTO Tap (child_id, init, end) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (child_id, init, end))
            self.coneccion.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error al añadir tap: {err}")
            return None