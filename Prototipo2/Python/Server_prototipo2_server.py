from flask import Flask, request, jsonify
from Server_prototipo2_daos import DAOUsers, DAOChilds, DAOTaps

app = Flask(__name__)

dao_users = DAOUsers()
dao_childs = DAOChilds()
dao_taps = DAOTaps()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = next((u for u in dao_users.users if u.username == username and u.password == password), None)
    if not user:
        return jsonify({"error": "Credenciales incorrectas"}), 401
    
    return jsonify({"user_id": user.id, "username": user.username, "email": user.email})

@app.route('/getchildren/<int:user_id>', methods=['GET'])
def get_children(user_id):
    children = dao_childs.getChildbyUser_ID(user_id)
    if not children:
        return jsonify({"message": "No hay niños asociados a este usuario"}), 404

    children_info = []
    for child in children:
        taps = dao_taps.getTapByChild_ID(child.id)
        child_data = {
            "id": child.id,
            "name": child.child_name,
            "sleep_average": child.sleep_average,
            "taps": [{"id": tap.id, "init": tap.init, "end": tap.end} for tap in (taps or [])]
        }
        children_info.append(child_data)

    return jsonify(children_info)

if __name__ == '__main__':
    app.run(debug=True)