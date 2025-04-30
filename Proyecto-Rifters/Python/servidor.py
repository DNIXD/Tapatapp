from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps
from daos import DAOUsers, DAOCards, DAODecks, DAOMatches

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_juego_cartas'

# Inicialización de DAOs
dao_users = DAOUsers()
dao_cards = DAOCards()
dao_decks = DAODecks()
dao_matches = DAOMatches()

# ======================
# MIDDLEWARES
# ======================

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Token requerido"}), 401
        
        try:
            token = auth_header.split()[1]  # Formato: Bearer <token>
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
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

def generar_token(user_id):
    try:
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }
        return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    except Exception as e:
        raise ValueError(f"Error generando token: {str(e)}")

# ======================
# ENDPOINTS
# ======================

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not all([username, password, email]):
            return jsonify({"error": "Todos los campos son requeridos"}), 400

        user_id = dao_users.addUser(username, password, email)
        if not user_id:
            return jsonify({"error": "Error al registrar usuario"}), 400

        return jsonify({
            "message": "Usuario registrado exitosamente",
            "user_id": user_id
        }), 201

    except Exception as e:
        return jsonify({"error": f"Error en el registro: {str(e)}"}), 500

@app.route('/login', methods=['POST'])
def login():
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
            "message": "Sesión iniciada exitosamente"
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500

@app.route('/decks', methods=['GET'])
@token_required
def get_decks(current_user):
    try:
        decks = dao_decks.getDecksByUser(current_user['id'])
        if not decks:
            return jsonify({"message": "No tienes mazos creados"}), 404

        # Obtener cartas para cada mazo
        for deck in decks:
            deck['cards'] = dao_decks.getCardsByDeck(deck['id'])

        return jsonify(decks), 200

    except Exception as e:
        return jsonify({"error": f"Error obteniendo mazos: {str(e)}"}), 500

@app.route('/decks', methods=['POST'])
@token_required
def create_deck(current_user):
    try:
        data = request.json
        name = data.get('name')

        if not name:
            return jsonify({"error": "Nombre del mazo requerido"}), 400

        deck_id = dao_decks.addDeck(current_user['id'], name)
        if not deck_id:
            return jsonify({"error": "Error al crear mazo"}), 400

        return jsonify({
            "message": "Mazo creado exitosamente",
            "deck_id": deck_id
        }), 201

    except Exception as e:
        return jsonify({"error": f"Error creando mazo: {str(e)}"}), 500

@app.route('/decks/<int:deck_id>/cards', methods=['POST'])
@token_required
def add_card_to_deck(current_user, deck_id):
    try:
        data = request.json
        card_id = data.get('card_id')
        quantity = data.get('quantity', 1)

        if not card_id:
            return jsonify({"error": "ID de carta requerido"}), 400

        # Verificar que el mazo pertenece al usuario
        deck = dao_decks.getDeckByID(deck_id)
        if not deck or deck['user_id'] != current_user['id']:
            return jsonify({"error": "Mazo no válido"}), 403

        success = dao_decks.addCardToDeck(deck_id, card_id, quantity)
        if not success:
            return jsonify({"error": "Error al añadir carta al mazo"}), 400

        return jsonify({"message": "Carta añadida al mazo exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error añadiendo carta: {str(e)}"}), 500

@app.route('/matches', methods=['GET'])
@token_required
def get_matches(current_user):
    try:
        # Partidas en espera
        waiting_matches = dao_matches.getWaitingMatches()
        
        # Partidas del jugador
        player_matches = dao_matches.getPlayerMatches(current_user['id'])

        return jsonify({
            "waiting_matches": waiting_matches or [],
            "player_matches": player_matches or []
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error obteniendo partidas: {str(e)}"}), 500

@app.route('/matches', methods=['POST'])
@token_required
def create_match(current_user):
    try:
        data = request.json
        deck_id = data.get('deck_id')

        if not deck_id:
            return jsonify({"error": "ID de mazo requerido"}), 400

        # Verificar que el mazo pertenece al usuario
        deck = dao_decks.getDeckByID(deck_id)
        if not deck or deck['user_id'] != current_user['id']:
            return jsonify({"error": "Mazo no válido"}), 403

        match_id = dao_matches.createMatch(current_user['id'], deck_id)
        if not match_id:
            return jsonify({"error": "Error al crear partida"}), 400

        return jsonify({
            "message": "Partida creada exitosamente",
            "match_id": match_id
        }), 201

    except Exception as e:
        return jsonify({"error": f"Error creando partida: {str(e)}"}), 500

@app.route('/matches/<int:match_id>/join', methods=['POST'])
@token_required
def join_match(current_user, match_id):
    try:
        data = request.json
        deck_id = data.get('deck_id')

        if not deck_id:
            return jsonify({"error": "ID de mazo requerido"}), 400

        # Verificar que el mazo pertenece al usuario
        deck = dao_decks.getDeckByID(deck_id)
        if not deck or deck['user_id'] != current_user['id']:
            return jsonify({"error": "Mazo no válido"}), 403

        success = dao_matches.joinMatch(match_id, current_user['id'], deck_id)
        if not success:
            return jsonify({"error": "Error al unirse a partida"}), 400

        return jsonify({"message": "Te has unido a la partida exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error uniéndose a partida: {str(e)}"}), 500

@app.route('/matches/current', methods=['GET'])
@token_required
def get_current_match(current_user):
    try:
        # Obtener partida actual del jugador
        matches = dao_matches.getPlayerMatches(current_user['id'])
        if not matches:
            return jsonify({"message": "No estás en ninguna partida activa"}), 404

        # Por simplicidad, tomamos la primera partida activa
        current_match = matches[0]
        match_state = dao_matches.getMatchState(current_match['id'], current_user['id'])
        
        if not match_state:
            return jsonify({"error": "Error obteniendo estado de partida"}), 400

        return jsonify(match_state), 200

    except Exception as e:
        return jsonify({"error": f"Error obteniendo partida: {str(e)}"}), 500

@app.route('/matches/action', methods=['POST'])
@token_required
def perform_action(current_user):
    try:
        data = request.json
        action = data.get('action')
        card_id = data.get('card_id')

        # Obtener partida actual del jugador
        matches = dao_matches.getPlayerMatches(current_user['id'])
        if not matches:
            return jsonify({"error": "No estás en ninguna partida activa"}), 400

        match_id = matches[0]['id']

        if action == "end_turn":
            success = dao_matches.endTurn(match_id, current_user['id'])
            if not success:
                return jsonify({"error": "Error al pasar turno"}), 400
            
            return jsonify({"message": "Turno pasado exitosamente"}), 200

        elif action == "play_card" and card_id:
            success = dao_matches.playCard(match_id, current_user['id'], card_id)
            if not success:
                return jsonify({"error": "Error al jugar carta"}), 400
            
            return jsonify({"message": "Carta jugada exitosamente"}), 200

        else:
            return jsonify({"error": "Acción no válida"}), 400

    except Exception as e:
        return jsonify({"error": f"Error realizando acción: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)