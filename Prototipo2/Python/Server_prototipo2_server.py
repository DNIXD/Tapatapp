from flask import Flask, request, jsonify
from Server_prototipo2_daos import DAOUsers, DAOChilds

app = Flask(__name__)

dao_users = DAOUsers()
dao_childs = DAOChilds()

# Ruta para iniciar sesión y obtener información del niño asociado
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Autenticación de usuario
    user = next((u for u in dao_users.users if u.username == username and u.password == password), None)
    if not user:
        return jsonify({"error": "Credenciales incorrectas"}), 401
    
    # Obtener información del niño asociado
    children = dao_childs.getChildbyUser_ID(user.id)
    if not children:
        return jsonify({"message": "No hay niños asociados a este usuario"})
    
    return jsonify({"user": user.__dict__, "children": [child.__dict__ for child in children]})

if __name__ == '__main__':
    app.run(debug=True)