from flask import Flask, request, jsonify

app = Flask(__name__)

class User:
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
    
    def __str__(self):
        return "User:" + self.username + " pass:" + self.password + " email:" + self.email

class DAOUsers:
    def _init_(self):
        self.users=listUsers

    def getUserByUsername(self, username):
        for u in listUsers:
            if username == u.username:
                return u


listUsers = [
    User(id=1, username="usuari1", password="12345", email="usuari1@gmail.com"),
    User(id=2, username="usuari2", password="54321", email="usuari2@gmail.com"),
    User(id=3, username="usuari3", password="54321", email="usuari3@gmail.com"),
    User(id=4, username="usuari4", password="67890", email="usuari4@gmail.com")
    ]
for u in listUsers:
    print(u)

daousers = DAOUsers()

print(daousers.getUserByUsername("usuari4"))
u=daousers.getUserByUsername("notrobat")

if(u):
    print(u)
else:
    print("No encontrad")

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="10028")