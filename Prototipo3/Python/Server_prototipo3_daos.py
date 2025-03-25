import Server_prototipo3_datos as dades

class DAOUsers:
    def __init__(self):
        self.users = dades.users

    def getUserByID(self, id):
        for u in self.users:
            if id == u.id:
                return u
        return None

    def addUser(self, user):
        self.users.append(user)

class DAOChilds:
    def __init__(self):
        self.children = dades.children

    def getChildbyUser_ID(self, user_id):
        child_ids = [rel["child_id"] for rel in dades.relation_user_child if rel["user_id"] == user_id]
        return [child for child in self.children if child.id in child_ids] or None

    def addChild(self, child):
        self.children.append(child)

class DAOTaps:
    def __init__(self):
        self.taps = dades.taps

    def getTapByChild_ID(self, child_id):
        taps_info = [tap for tap in self.taps if tap.child_id == child_id]
        return taps_info if taps_info else None

    def addTap(self, tap):
        self.taps.append(tap)