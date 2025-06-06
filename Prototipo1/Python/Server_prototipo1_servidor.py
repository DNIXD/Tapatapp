from flask import Flask, request, jsonify

app = Flask(__name__)

class User:
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email
        }
    
    def __str__(self):
        return "User:" + self.username + " pass:" + self.password + " email:" + self.email


class DAOUsers:
    def __init__(self):
        self.users = listUsers

    def getUserByUsername(self, username):
        for u in self.users:
            if username == u.username:
                return u
        return None


listUsers = [
    User(id=1, username="usuari1", password="12345", email="usuari1@gmail.com"),
    User(id=2, username="usuari2", password="54321", email="usuari2@gmail.com"),
    User(id=3, username="usuari3", password="54321", email="usuari3@gmail.com"),
    User(id=4, username="usuari4", password="67890", email="usuari4@gmail.com")
]

for u in listUsers:
    print(u)

daousers = DAOUsers()

@app.route('/hello', methods=['GET'])
def hello():
    user = daousers.getUserByUsername("usuari1")
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "User not found"}), 404


@app.route('/tapatapp/getuser', methods=['GET'])
def getuser():
    n = str(request.args.get('name'))
    email = str(request.args.get('mail'))
    return "HelloWorld Name = " + n + " Mail = " + email


@app.route('/prototip1/getuser/', defaults={'username': None}, methods=['GET'])
@app.route('/prototip1/getuser/<string:username>', methods=['GET'])
def prototip(username):
    if not username:  # Verifica si es None o una cadena vacía
        return jsonify({"error": "Parametro no introducido"}), 400

    user = daousers.getUserByUsername(username)
    if user:
        return jsonify(user.to_dict())
    
    return jsonify({"error": "Usuario no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="10050")