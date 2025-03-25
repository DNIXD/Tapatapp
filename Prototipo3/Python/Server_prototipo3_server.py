from flask import Flask, request, jsonify
from Server_prototipo3_daos import DAOUsers, DAOChilds, DAOTaps
from Server_prototipo3_datos import User, Child, Tap
import Server_prototipo3_datos as dades
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_super_segura'

dao_users = DAOUsers()
dao_childs = DAOChilds()
dao_taps = DAOTaps()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token requerido"}), 401
        
        try:
            data = jwt.decode(token.split()[1], app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = dao_users.getUserByID(data['user_id'])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except:
            return jsonify({"error": "Token invalido"}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    
    if 'token' in data:
        try:
            decoded = jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms=["HS256"])
            user = dao_users.getUserByID(decoded['user_id'])
            if not user:
                return jsonify({"error": "Usuario no existe"}), 404
            
            new_token = generate_token(user.id)
            return jsonify({
                "token": new_token,
                "user_id": user.id,
                "username": user.username,
                "email": user.email
            })
        except Exception as e:
            return jsonify({"error": f"Token invalido: {str(e)}"}), 401
    
    username = data.get('username')
    password = data.get('password')
    
    user = next((u for u in dao_users.users if u.username == username and u.password == password), None)
    if not user:
        return jsonify({"error": "Credenciales incorrectas"}), 401
    
    token = generate_token(user.id)
    return jsonify({
        "token": token,
        "user_id": user.id,
        "username": user.username,
        "email": user.email
    })

def generate_token(user_id):
    return jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }, app.config['SECRET_KEY'])

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({"error": "Faltan datos"}), 400
    
    if any(u.username == username for u in dao_users.users):
        return jsonify({"error": "El usuario ya existe"}), 400
    
    new_id = len(dao_users.users) + 1
    new_user = User(id=new_id, username=username, password=password, email=email)
    dao_users.users.append(new_user)
    
    return jsonify({
        "message": "Usuario registrado exitosamente",
        "user_id": new_id
    }), 201

@app.route('/children', methods=['POST'])
@token_required
def add_child(current_user):
    data = request.json
    name = data.get('name')
    sleep_average = data.get('sleep_average', 8)
    treatment_id = data.get('treatment_id', 1)
    time = data.get('time', 6)

    if not name:
        return jsonify({"error": "Nombre del niño requerido"}), 400
    
    new_id = len(dao_childs.children) + 1
    new_child = Child(id=new_id, child_name=name, sleep_average=sleep_average, 
                     treatment_id=treatment_id, time=time)
    dao_childs.children.append(new_child)
    
    dades.relation_user_child.append({
        "user_id": current_user.id,
        "child_id": new_id,
        "rol_id": 2
    })
    
    return jsonify({
        "message": "Niño añadido exitosamente",
        "child_id": new_id
    }), 201

@app.route('/taps', methods=['POST'])
@token_required
def add_tap(current_user):
    data = request.json
    child_id = data.get('child_id')
    init = data.get('init')
    end = data.get('end')
    status_id = data.get('status_id', 1)

    if not child_id or not init:
        return jsonify({"error": "child_id e init son requeridos"}), 400
    
    child = next((c for c in dao_childs.children if c.id == child_id), None)
    if not child:
        return jsonify({"error": "Niño no encontrado"}), 404
    
    user_has_child = any(rel["user_id"] == current_user.id and rel["child_id"] == child_id 
                    for rel in dades.relation_user_child)
    if not user_has_child:
        return jsonify({"error": "No tienes permisos sobre este niño"}), 403
    
    new_id = len(dao_taps.taps) + 1
    new_tap = Tap(id=new_id, child_id=child_id, status_id=status_id, 
                 user_id=current_user.id, init=init, end=end)
    dao_taps.taps.append(new_tap)
    
    return jsonify({
        "message": "Tap añadido exitosamente",
        "tap_id": new_id
    }), 201

@app.route('/getchildren/<int:user_id>', methods=['GET'])
@token_required
def get_children(current_user, user_id):
    if current_user.id != user_id:
        return jsonify({"error": "No autorizado"}), 403
    
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