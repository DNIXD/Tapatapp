from flask import Flask, request, jsonify
from Server_prototipo4_daos import DAOUsers, DAOChilds, DAOTaps
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_ultra_segura'  # Cambiar en producción

# Inicialización de DAOs
dao_users = DAOUsers()
dao_childs = DAOChilds()
dao_taps = DAOTaps()

# ======================
# FUNCIONES AUXILIARES
# ======================

def generar_token(user_id):
    """Genera un token JWT válido"""
    try:
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow(),
            'iss': 'childapp_server'
        }
        return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    except Exception as e:
        raise ValueError(f"Error generando token: {str(e)}")

# ======================
# MIDDLEWARES
# ======================

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Token requerido (cabecera Authorization faltante)"}), 401
        
        try:
            token = auth_header.split()[1]  # Formato: Bearer <token>
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"], issuer="childapp_server")
            current_user = dao_users.getUserByID(data['user_id'])
            if not current_user:
                raise ValueError("Usuario no existe")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({"error": f"Token inválido: {str(e)}"}), 401
        except Exception as e:
            return jsonify({"error": f"Error de autenticación: {str(e)}"}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# ======================
# ENDPOINTS
# ======================

@app.route('/login', methods=['POST'])
def login():
    """Inicio de sesión"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Usuario y contraseña requeridos"}), 400

        user = dao_users.getUserByUsernameAndPassword(username, password)
        if not user:
            return jsonify({"error": "Credenciales incorrectas"}), 401

        token = generar_token(user['id'])
        return jsonify({
            "token": token,
            "user_id": user['id'],
            "username": user['username'],
            "email": user['email'],
            "message": "Sesión iniciada exitosamente"
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500


@app.route('/register', methods=['POST'])
def register():
    """Registro de nuevos usuarios"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not all([username, password, email]):
            return jsonify({"error": "Todos los campos son requeridos"}), 400

        existing_user = dao_users.getUserByUsername(username)
        if existing_user:
            return jsonify({"error": "El usuario ya existe"}), 400

        user_id = dao_users.addUser(username, password, email)
        return jsonify({
            "message": "Usuario registrado exitosamente",
            "user_id": user_id
        }), 201

    except Exception as e:
        return jsonify({"error": f"Error en el registro: {str(e)}"}), 500


@app.route('/children', methods=['POST'])
@token_required
def add_child(current_user):
    """Añade un nuevo niño asociado al usuario actual"""
    try:
        data = request.json
        name = data.get('name')
        sleep_average = data.get('sleep_average')

        if not name or not sleep_average:
            return jsonify({"error": "Nombre y promedio de sueño requeridos"}), 400

        child_id = dao_childs.addChild(current_user['id'], name, sleep_average)
        return jsonify({
            "message": "Niño añadido exitosamente",
            "child_id": child_id
        }), 201

    except Exception as e:
        return jsonify({"error": f"Error añadiendo niño: {str(e)}"}), 500


@app.route('/taps', methods=['POST'])
@token_required
def add_tap(current_user):
    """Añade un nuevo tap asociado a un niño del usuario"""
    try:
        data = request.json
        child_id = data.get('child_id')
        init = data.get('init')
        end = data.get('end')

        if not child_id or not init or not end:
            return jsonify({"error": "child_id, init y end son requeridos"}), 400

        tap_id = dao_taps.addTap(child_id, init, end)
        return jsonify({
            "message": "Tap añadido exitosamente",
            "tap_id": tap_id
        }), 201

    except Exception as e:
        return jsonify({"error": f"Error añadiendo tap: {str(e)}"}), 500


@app.route('/getchildren', methods=['GET'])
@token_required
def get_children(current_user):
    """Obtiene los niños asociados al usuario actual"""
    try:
        children = dao_childs.getChildbyUser_ID(current_user['id'])
        if not children:
            return jsonify({"message": "No hay niños asociados a este usuario"}), 404

        for child in children:
            child['taps'] = dao_taps.getTapByChild_ID(child['id'])

        return jsonify(children), 200

    except Exception as e:
        return jsonify({"error": f"Error obteniendo niños: {str(e)}"}), 500


@app.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """Cierra la sesión del usuario"""
    return jsonify({"message": "Sesión cerrada exitosamente"}), 200

# ======================
# INICIO DEL SERVIDOR
# ======================

if __name__ == '__main__':
    app.run(debug=True, port=5000)