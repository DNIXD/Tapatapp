import Server_prototipo2_datos as dades
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