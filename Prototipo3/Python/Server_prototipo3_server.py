from flask import Flask, request, jsonify
from Server_prototipo3_daos import DAOUsers, DAOChilds, DAOTaps
from Server_prototipo3_datos import User, Child, Tap
import Server_prototipo3_datos as dades
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_ultra_segura'  # ¡Cambiar en producción!

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
        # Verificar cabecera Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Token requerido (cabecera Authorization faltante)"}), 401
        
        # Extraer el token
        try:
            token = auth_header.split()[1]  # Formato: Bearer <token>
        except IndexError:
            return jsonify({"error": "Formato de token inválido. Usa: Bearer <token>"}), 401
        
        # Verificar token
        try:
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
    """Endpoint de login con soporte para token y credenciales"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Datos JSON requeridos"}), 400
        
        # Autenticación por token
        if 'token' in data:
            try:
                decoded = jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms=["HS256"], issuer="childapp_server")
                user = dao_users.getUserByID(decoded['user_id'])
                if not user:
                    return jsonify({"error": "Usuario no existe"}), 404
                
                # Generar nuevo token (renovación)
                nuevo_token = generar_token(user.id)
                return jsonify({
                    "token": nuevo_token,
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "message": "Sesión renovada con token"
                })
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expirado"}), 401
            except jwt.InvalidTokenError as e:
                return jsonify({"error": f"Token inválido: {str(e)}"}), 401
        
        # Autenticación tradicional
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "Usuario y contraseña requeridos"}), 400
        
        user = next((u for u in dao_users.users if u.username == username and u.password == password), None)
        if not user:
            return jsonify({"error": "Credenciales incorrectas"}), 401
        
        token = generar_token(user.id)
        return jsonify({
            "token": token,
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "message": "Sesión iniciada con credenciales"
        })
    
    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500

@app.route('/register', methods=['POST'])
def register():
    """Endpoint de registro de nuevos usuarios"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not all([username, password, email]):
            return jsonify({"error": "Todos los campos son requeridos"}), 400
        
        if any(u.username == username for u in dao_users.users):
            return jsonify({"error": "El usuario ya existe"}), 400
        
        new_id = len(dao_users.users) + 1
        new_user = User(id=new_id, username=username, password=password, email=email)
        dao_users.users.append(new_user)
        
        return jsonify({
            "message": "Usuario registrado exitosamente",
            "user_id": new_id
        }), 201
    
    except Exception as e:
        return jsonify({"error": f"Error en el registro: {str(e)}"}), 500

@app.route('/children', methods=['POST'])
@token_required
def add_child(current_user):
    """Añade un nuevo niño asociado al usuario actual"""
    try:
        data = request.get_json()
        name = data.get('name')
        
        if not name:
            return jsonify({"error": "Nombre del niño requerido"}), 400
        
        new_id = len(dao_childs.children) + 1
        new_child = Child(
            id=new_id,
            child_name=name,
            sleep_average=data.get('sleep_average', 8),
            treatment_id=data.get('treatment_id', 1),
            time=data.get('time', 6)
        )
        dao_childs.children.append(new_child)
        
        # Crear relación usuario-niño
        dades.relation_user_child.append({
            "user_id": current_user.id,
            "child_id": new_id,
            "rol_id": 2  # Tutor por defecto
        })
        
        return jsonify({
            "message": "Niño añadido exitosamente",
            "child_id": new_id
        }), 201
    
    except Exception as e:
        return jsonify({"error": f"Error añadiendo niño: {str(e)}"}), 500

@app.route('/taps', methods=['POST'])
@token_required
def add_tap(current_user):
    """Añade un nuevo tap asociado a un niño del usuario"""
    try:
        data = request.get_json()
        child_id = data.get('child_id')
        init = data.get('init')
        
        if not child_id or not init:
            return jsonify({"error": "child_id e init son requeridos"}), 400
        
        # Verificar permisos sobre el niño
        child_exists = any(
            c.id == child_id and 
            any(rel["user_id"] == current_user.id for rel in dades.relation_user_child if rel["child_id"] == child_id)
            for c in dao_childs.children
        )
        if not child_exists:
            return jsonify({"error": "No tienes permisos sobre este niño"}), 403
        
        new_id = len(dao_taps.taps) + 1
        new_tap = Tap(
            id=new_id,
            child_id=child_id,
            status_id=data.get('status_id', 1),
            user_id=current_user.id,
            init=init,
            end=data.get('end')
        )
        dao_taps.taps.append(new_tap)
        
        return jsonify({
            "message": "Tap añadido exitosamente",
            "tap_id": new_id
        }), 201
    
    except Exception as e:
        return jsonify({"error": f"Error añadiendo tap: {str(e)}"}), 500

@app.route('/getchildren/<int:user_id>', methods=['GET'])
@token_required
def get_children(current_user, user_id):
    """Obtiene los niños asociados al usuario"""
    try:
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
                "taps": [{
                    "id": tap.id,
                    "init": tap.init,
                    "end": tap.end
                } for tap in (taps or [])]
            }
            children_info.append(child_data)

        return jsonify(children_info)
    
    except Exception as e:
        return jsonify({"error": f"Error obteniendo niños: {str(e)}"}), 500

@app.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """Invalidación de token (implementación básica)"""
    # En producción deberías usar una lista negra de tokens
    return jsonify({"message": "Sesión cerrada exitosamente"})

# ======================
# INICIO DEL SERVIDOR
# ======================

if __name__ == '__main__':
    app.run(debug=True, port=5000)