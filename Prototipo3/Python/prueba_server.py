import requests
import json
import os
from pathlib import Path

BASE_URL = "http://127.0.0.1:5000"
TOKEN_FILE = Path.home() / ".childapp_token.json"

# ======================
# FUNCIONES AUXILIARES
# ======================

def guardar_token(token_data):
    """Guarda el token de forma segura manteniendo todos los campos necesarios"""
    try:
        with open(TOKEN_FILE, 'w') as f:
            json.dump({
                'token': token_data['token'],
                'user_id': token_data['user_id'],
                'username': token_data['username'],
                'email': token_data.get('email', '')
            }, f)
        os.chmod(TOKEN_FILE, 0o600)  # Permisos seguros (rw solo para el usuario)
        return True
    except Exception as e:
        print(f"[!] Error guardando token: {str(e)}")
        return False

def cargar_token():
    """Carga el token con validación robusta"""
    try:
        if not TOKEN_FILE.exists():
            return None
            
        with open(TOKEN_FILE, 'r') as f:
            data = json.load(f)
            # Validación de campos esenciales
            if all(key in data for key in ['token', 'user_id', 'username']):
                return data
            # print("[!] Token corrupto - faltan campos esenciales")
            return None
    except json.JSONDecodeError:
        print("[!] Token corrupto - formato JSON inválido")
    except Exception as e:
        print(f"[!] Error cargando token: {str(e)}")
    return None

def eliminar_token():
    """Elimina el token de forma segura"""
    try:
        if TOKEN_FILE.exists():
            os.remove(TOKEN_FILE)
            return True
    except Exception as e:
        print(f"[!] Error eliminando token: {str(e)}")
    return False

def mostrar_info_ninos(children):
    """Muestra la información de los niños de forma clara"""
    if not children:
        print("\n[!] No hay niños registrados")
        return
    
    print("\n=== INFORMACIÓN DE NIÑOS ===")
    for child in children:
        print(f"\n• ID: {child['id']}")
        print(f"• Nombre: {child['name']}")
        print(f"• Horas de sueño: {child['sleep_average']}")
        
        if child["taps"]:
            print("\n  Taps registrados:")
            for tap in child["taps"]:
                print(f"  - Inicio: {tap['init']}")
                print(f"    Fin: {tap.get('end', 'En progreso')}")
        else:
            print("\n  No hay taps registrados")

# ======================
# FUNCIONES PRINCIPALES
# ======================

def registrar_usuario():
    """Registra un nuevo usuario en el sistema"""
    print("\n=== REGISTRO DE USUARIO ===")
    username = input("Usuario: ").strip()
    password = input("Contraseña: ").strip()
    email = input("Email: ").strip()

    try:
        response = requests.post(
            f"{BASE_URL}/register",
            json={"username": username, "password": password, "email": email},
            timeout=5
        )
        
        if response.status_code == 201:
            print("\n[+] ¡Usuario registrado exitosamente!")
        else:
            error_msg = response.json().get('error', 'Error desconocido')
            print(f"\n[!] Error en el registro: {error_msg}")
    except requests.exceptions.RequestException as e:
        print(f"\n[!] Error de conexión: {str(e)}")

def iniciar_sesion():
    """Maneja todo el proceso de autenticación"""
    saved_token = cargar_token()
    
    # Opción para continuar sesión existente
    if saved_token:
        print("\n[!] Sesión guardada encontrada")
        print(f"Usuario: {saved_token.get('username')}")
        
        opcion = input("\n1. Continuar con esta sesión\n2. Iniciar con otra cuenta\nOpción: ").strip()
        
        if opcion == "1":
            try:
                response = requests.post(
                    f"{BASE_URL}/login",
                    json={"token": saved_token['token']},
                    timeout=5
                )
                
                if response.status_code == 200:
                    new_data = response.json()
                    if guardar_token(new_data):
                        print("\n[+] Sesión reanudada correctamente")
                        return True
                    else:
                        print("\n[!] No se pudo guardar el nuevo token")
                else:
                    error_msg = response.json().get('error', 'Error validando token')
                    print(f"\n[!] {error_msg}")
            except requests.exceptions.RequestException as e:
                print(f"\n[!] Error de conexión: {str(e)}")
    
    # Login tradicional
    print("\n=== INICIO DE SESIÓN ===")
    username = input("Usuario: ").strip()
    password = input("Contraseña: ").strip()
    
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            json={"username": username, "password": password},
            timeout=5
        )
        
        if response.status_code == 200:
            if guardar_token(response.json()):
                print("\n[+] Sesión iniciada correctamente")
                return True
            else:
                print("\n[!] No se pudo guardar el token")
        else:
            error_msg = response.json().get('error', 'Credenciales incorrectas')
            print(f"\n[!] {error_msg}")
    except requests.exceptions.RequestException as e:
        print(f"\n[!] Error de conexión: {str(e)}")
    
    return False

def menu_control_niños():
    """Menú de gestión de niños (requiere sesión activa)"""
    token_data = cargar_token()
    if not token_data:
        print("\n[!] No hay sesión activa")
        return
    
    headers = {'Authorization': f'Bearer {token_data["token"]}'}
    
    while True:
        print("\n=== PANEL DE CONTROL ===")
        print(f"Usuario: {token_data['username']} (ID: {token_data['user_id']})")
        print("\n1. Ver información de niños")
        print("2. Añadir niño")
        print("3. Añadir tap")
        print("4. Cerrar sesión (volver al menú principal)")
        
        opcion = input("\nOpción: ").strip()
        
        try:
            if opcion == "1":
                response = requests.get(
                    f"{BASE_URL}/getchildren/{token_data['user_id']}",
                    headers=headers,
                    timeout=5
                )
                
                if response.status_code == 200:
                    mostrar_info_ninos(response.json())
                else:
                    error_msg = response.json().get('error', 'Error al obtener niños')
                    print(f"\n[!] {error_msg}")
            
            elif opcion == "2":
                print("\n=== AÑADIR NIÑO ===")
                nombre = input("Nombre del niño: ").strip()
                
                response = requests.post(
                    f"{BASE_URL}/children",
                    json={"name": nombre},
                    headers=headers,
                    timeout=5
                )
                
                if response.status_code == 201:
                    print("\n[+] Niño añadido exitosamente")
                else:
                    error_msg = response.json().get('error', 'Error al añadir niño')
                    print(f"\n[!] {error_msg}")
            
            elif opcion == "3":
                print("\n=== AÑADIR TAP ===")
                child_id = input("ID del niño: ").strip()
                init = input("Fecha inicio (YYYY-MM-DDTHH:MM:SS): ").strip()
                end = input("Fecha fin (opcional): ").strip() or None
                
                response = requests.post(
                    f"{BASE_URL}/taps",
                    json={
                        "child_id": child_id,
                        "init": init,
                        "end": end
                    },
                    headers=headers,
                    timeout=5
                )
                
                if response.status_code == 201:
                    print("\n[+] Tap registrado exitosamente")
                else:
                    error_msg = response.json().get('error', 'Error al registrar tap')
                    print(f"\n[!] {error_msg}")
            
            elif opcion == "4":
                print("\n[+] Volviendo al menú principal...")
                break
            
            else:
                print("\n[!] Opción no válida")
        
        except requests.exceptions.RequestException as e:
            print(f"\n[!] Error de conexión: {str(e)}")

def menu_principal():
    """Menú principal de la aplicación"""
    # Verificar token al inicio
    token_data = cargar_token()
    if token_data:
        print(f"\n[!] Token de sesión encontrado para: {token_data['username']}")
    
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir de la aplicación")
        
        opcion = input("\nOpción: ").strip()
        
        if opcion == "1":
            if iniciar_sesion():
                menu_control_niños()
        
        elif opcion == "2":
            registrar_usuario()
        
        elif opcion == "3":
            if eliminar_token():
                print("\n[+] Token eliminado correctamente")
            print("\n[+] ¡Hasta pronto!")
            exit()
        
        else:
            print("\n[!] Opción no válida")

# ======================
# INICIO DE LA APLICACIÓN
# ======================

if __name__ == "__main__":
    # Configuración inicial del archivo de token
    try:
        if not TOKEN_FILE.exists():
            with open(TOKEN_FILE, 'w') as f:
                json.dump({}, f)
            os.chmod(TOKEN_FILE, 0o600)
    except Exception as e:
        print(f"[!] Error inicializando archivo de token: {str(e)}")
    
    menu_principal()