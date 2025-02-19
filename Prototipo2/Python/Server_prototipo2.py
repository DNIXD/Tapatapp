import Prototipo2.Python.Server_prototipo2_datos as dades
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
        self.children = dades.children  # Lista de niños

    def getChildbyUser_ID(self, user_id):
        child_ids = [rel["child_id"] for rel in dades.relation_user_child if rel["user_id"] == user_id]

        if not child_ids: 
            return None

        children_info = [child for child in self.children if child.id in child_ids] 
        return children_info

class DAOTaps:
    def __init__(self):
        self.taps = dades.taps

    def getTapByChild_ID(self, child_id):
        taps_info = [tap for tap in self.taps if tap.child_id == child_id]
        return taps_info if taps_info else None