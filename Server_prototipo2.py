import Server_prototipo2_datos as dades

# Exemple d'ús de la llista d'usuaris
#for x in dades.users:
#    print(x)

# Exemple d'ús de la classe User
#a= User(id=1, username="Kurl", password="12345", email="prova2@gmail.com")
#print(a)

class DAOUsers:
    def __init__(self):
        self.users = dades.users

    def getUserByID(self, id):
        for u in self.users:
            if id == u.id:
                return u
        return None

class DAOChilds:
    def __init__(self):
        self.users = dades.children

    def getChildbyUser_ID(self, id):
        for u in self.users:
            if id == u.id:
                for i in dades.relation_user_child{
                    if i[1] = 1:
                        child_id = i[2]
                }
        return None