import mysql.connector
from mysql.connector import pooling

class DAOUsers:
    def __init__(self):
        self.connection_pool = pooling.MySQLConnectionPool(
            pool_name="users_pool",
            pool_size=5,
            host="localhost",
            user="root",
            password="root",
            database="rifters"
        )

    def _get_connection(self):
        return self.connection_pool.get_connection()

    def getUserByID(self, user_id):
        """Obtiene un usuario por ID"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM usuarios WHERE id = %s"
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener usuario: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def getUserByUsername(self, username):
        """Obtiene un usuario por username"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM usuarios WHERE username = %s"
            cursor.execute(query, (username,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener usuario por username: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def getUserByUsernameAndPassword(self, username, password):
        """Obtiene un usuario por username y password"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener usuario por username y password: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def addUser(self, username, password, email):
        """Añade un nuevo usuario a la base de datos"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "INSERT INTO usuarios (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, email))
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error al añadir usuario: {err}")
            return None
        finally:
            cursor.close()
            conn.close()


class DAOCards:
    def __init__(self):
        self.connection_pool = pooling.MySQLConnectionPool(
            pool_name="cards_pool",
            pool_size=5,
            host="localhost",
            user="root",
            password="root",
            database="rifters"
        )

    def _get_connection(self):
        return self.connection_pool.get_connection()

    def getCardByID(self, card_id):
        """Obtiene una carta por ID"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM cartas WHERE id = %s"
            cursor.execute(query, (card_id,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener carta: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def getCardsByDeck(self, deck_id):
        """Obtiene las cartas de un mazo"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT c.*, mc.quantity 
                FROM cartas c
                JOIN mazo_cartas mc ON c.id = mc.card_id
                WHERE mc.deck_id = %s
            """
            cursor.execute(query, (deck_id,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al obtener cartas del mazo: {err}")
            return None
        finally:
            cursor.close()
            conn.close()


class DAODecks:
    def __init__(self):
        self.connection_pool = pooling.MySQLConnectionPool(
            pool_name="decks_pool",
            pool_size=5,
            host="localhost",
            user="root",
            password="root",
            database="rifters"
        )

    def _get_connection(self):
        return self.connection_pool.get_connection()

    def getDeckByID(self, deck_id):
        """Obtiene un mazo por ID"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM mazos WHERE id = %s"
            cursor.execute(query, (deck_id,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener mazo: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def getDecksByUser(self, user_id):
        """Obtiene los mazos de un usuario"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM mazos WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al obtener mazos del usuario: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def addDeck(self, user_id, name):
        """Crea un nuevo mazo para un usuario"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "INSERT INTO mazos (user_id, name) VALUES (%s, %s)"
            cursor.execute(query, (user_id, name))
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error al crear mazo: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def addCardToDeck(self, deck_id, card_id, quantity=1):
        """Añade una carta a un mazo"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Verificar si la carta ya está en el mazo
            query = "SELECT id FROM mazo_cartas WHERE deck_id = %s AND card_id = %s"
            cursor.execute(query, (deck_id, card_id))
            if cursor.fetchone():
                query = "UPDATE mazo_cartas SET quantity = quantity + %s WHERE deck_id = %s AND card_id = %s"
            else:
                query = "INSERT INTO mazo_cartas (deck_id, card_id, quantity) VALUES (%s, %s, %s)"
            
            cursor.execute(query, (quantity, deck_id, card_id) if "UPDATE" in query else (deck_id, card_id, quantity))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error al añadir carta al mazo: {err}")
            return False
        finally:
            cursor.close()
            conn.close()


class DAOMatches:
    def __init__(self):
        self.connection_pool = pooling.MySQLConnectionPool(
            pool_name="matches_pool",
            pool_size=5,
            host="localhost",
            user="root",
            password="root",
            database="rifters"
        )

    def _get_connection(self):
        return self.connection_pool.get_connection()

    def getMatchByID(self, match_id):
        """Obtiene una partida por ID"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT p.*, 
                       u1.username AS player1_name, 
                       u2.username AS player2_name,
                       d1.name AS player1_deck_name,
                       d2.name AS player2_deck_name
                FROM partidas p
                LEFT JOIN usuarios u1 ON p.player1_id = u1.id
                LEFT JOIN usuarios u2 ON p.player2_id = u2.id
                LEFT JOIN mazos d1 ON p.player1_deck = d1.id
                LEFT JOIN mazos d2 ON p.player2_deck = d2.id
                WHERE p.id = %s
            """
            cursor.execute(query, (match_id,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener partida: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def getWaitingMatches(self):
        """Obtiene partidas en espera de jugador"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT p.id, p.created_at, u.username AS creator_name
                FROM partidas p
                JOIN usuarios u ON p.player1_id = u.id
                WHERE p.status = 'waiting'
            """
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al obtener partidas en espera: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def getPlayerMatches(self, user_id):
        """Obtiene partidas de un jugador"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT p.*, 
                       u1.username AS player1_name, 
                       u2.username AS player2_name,
                       CASE 
                           WHEN p.player1_id = %s THEN 'player1'
                           WHEN p.player2_id = %s THEN 'player2'
                       END AS player_role
                FROM partidas p
                LEFT JOIN usuarios u1 ON p.player1_id = u1.id
                LEFT JOIN usuarios u2 ON p.player2_id = u2.id
                WHERE (p.player1_id = %s OR p.player2_id = %s) 
                AND p.status != 'finished'
            """
            cursor.execute(query, (user_id, user_id, user_id, user_id))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al obtener partidas del jugador: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def createMatch(self, player1_id, player1_deck):
        """Crea una nueva partida"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Crear partida
            query = """
                INSERT INTO partidas 
                (player1_id, player1_deck, current_player, status) 
                VALUES (%s, %s, %s, 'waiting')
            """
            cursor.execute(query, (player1_id, player1_deck, player1_id))
            match_id = cursor.lastrowid
            
            # Crear estado inicial del jugador
            query = """
                INSERT INTO partida_estado 
                (match_id, player_id, life_points, mana_available, mana_max) 
                VALUES (%s, %s, 30, 1, 1)
            """
            cursor.execute(query, (match_id, player1_id))
            
            conn.commit()
            return match_id
        except mysql.connector.Error as err:
            print(f"Error al crear partida: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def joinMatch(self, match_id, player2_id, player2_deck):
        """Une a un jugador a una partida existente"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Actualizar partida
            query = """
                UPDATE partidas 
                SET player2_id = %s, player2_deck = %s, status = 'active' 
                WHERE id = %s AND status = 'waiting'
            """
            cursor.execute(query, (player2_id, player2_deck, match_id))
            
            if cursor.rowcount == 0:
                return False
                
            # Crear estado inicial del segundo jugador
            query = """
                INSERT INTO partida_estado 
                (match_id, player_id, life_points, mana_available, mana_max) 
                VALUES (%s, %s, 30, 1, 1)
            """
            cursor.execute(query, (match_id, player2_id))
            
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error al unirse a partida: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def getMatchState(self, match_id, player_id=None):
        """Obtiene el estado completo de una partida"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Obtener información básica de la partida
            match = self.getMatchByID(match_id)
            if not match:
                return None
                
            # Obtener estado de los jugadores
            query = """
                SELECT pe.*, u.username
                FROM partida_estado pe
                JOIN usuarios u ON pe.player_id = u.id
                WHERE pe.match_id = %s
            """
            cursor.execute(query, (match_id,))
            players = cursor.fetchall()
            
            # Obtener cartas en juego
            query = """
                SELECT pc.*, c.name, c.type, c.attack, c.defense, c.cost
                FROM partida_cartas pc
                JOIN cartas c ON pc.card_id = c.id
                WHERE pc.match_id = %s
            """
            cursor.execute(query, (match_id,))
            cards = cursor.fetchall()
            
            # Obtener mazo del jugador actual (si se especifica)
            player_deck = None
            if player_id:
                role = 'player1' if match['player1_id'] == player_id else 'player2'
                deck_id = match['player1_deck'] if role == 'player1' else match['player2_deck']
                
                query = """
                    SELECT c.*, mc.quantity
                    FROM cartas c
                    JOIN mazo_cartas mc ON c.id = mc.card_id
                    WHERE mc.deck_id = %s
                """
                cursor.execute(query, (deck_id,))
                player_deck = cursor.fetchall()
            
            return {
                'match_info': match,
                'players': players,
                'cards_in_play': cards,
                'player_deck': player_deck
            }
        except mysql.connector.Error as err:
            print(f"Error al obtener estado de partida: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def endTurn(self, match_id, current_player_id):
        """Finaliza el turno actual y pasa al siguiente jugador"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Obtener información de la partida
            query = "SELECT player1_id, player2_id FROM partidas WHERE id = %s"
            cursor.execute(query, (match_id,))
            match = cursor.fetchone()
            
            if not match:
                return False
                
            # Determinar siguiente jugador
            next_player = match['player2_id'] if current_player_id == match['player1_id'] else match['player1_id']
            
            # Actualizar mana del siguiente jugador (aumenta hasta máximo 10)
            query = """
                UPDATE partida_estado 
                SET mana_max = LEAST(mana_max + 1, 10),
                    mana_available = LEAST(mana_max + 1, 10)
                WHERE match_id = %s AND player_id = %s
            """
            cursor.execute(query, (match_id, next_player))
            
            # Actualizar turno de la partida
            query = """
                UPDATE partidas 
                SET current_player = %s, 
                    current_turn = current_turn + 1
                WHERE id = %s
            """
            cursor.execute(query, (next_player, match_id))
            
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error al pasar turno: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def playCard(self, match_id, player_id, card_id, zone='field'):
        """Juega una carta en la partida"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Verificar que el jugador tiene suficiente mana
            query = """
                SELECT mana_available FROM partida_estado 
                WHERE match_id = %s AND player_id = %s
            """
            cursor.execute(query, (match_id, player_id))
            player_state = cursor.fetchone()
            
            if not player_state:
                return False
                
            # Obtener costo de la carta
            query = "SELECT cost FROM cartas WHERE id = %s"
            cursor.execute(query, (card_id,))
            card = cursor.fetchone()
            
            if not card or player_state['mana_available'] < card['cost']:
                return False
                
            # Insertar carta en juego
            query = """
                INSERT INTO partida_cartas 
                (match_id, player_id, card_id, zone) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (match_id, player_id, card_id, zone))
            
            # Reducir mana del jugador
            query = """
                UPDATE partida_estado 
                SET mana_available = mana_available - %s
                WHERE match_id = %s AND player_id = %s
            """
            cursor.execute(query, (card['cost'], match_id, player_id))
            
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error al jugar carta: {err}")
            return False
        finally:
            cursor.close()
            conn.close()