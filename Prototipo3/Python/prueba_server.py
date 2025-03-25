import requests
import json
import os
from pathlib import Path

BASE_URL = "http://127.0.0.1:5000"
TOKEN_FILE = Path.home() / ".childapp_token.json"

# --- Funciones de persistencia ---
def guardar_token(token_data):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f)

def cargar_token():
    if not TOKEN_FILE.exists():
        return None
    with open(TOKEN_FILE, 'r') as f:
        return json.load(f)

def eliminar_token():
    if TOKEN_FILE.exists():
        os.remove(TOKEN_FILE)

# --- Página de Login ---
def pagina_login():
    while True:
        print("\n=== INICIO DE SESIÓN ===")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        
        opcion = input("Opción: ").strip()
        
        if opcion == "1":
            username = input("Usuario: ")
            password = input("Contraseña: ")
            
            response = requests.post(
                f"{BASE_URL}/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                guardar_token(data)
                pagina_control_niños(data['user_id'])
            else:
                print("Error:", response.json().get("error"))
        
        elif opcion == "2":
            username = input("Nuevo usuario: ")
            password = input("Contraseña: ")
            email = input("Email: ")
            
            response = requests.post(
                f"{BASE_URL}/register",
                json={"username": username, "password": password, "email": email}
            )
            
            if response.status_code == 201:
                print("¡Registro exitoso! Ahora inicia sesión.")
            else:
                print("Error:", response.json().get("error"))
        
        elif opcion == "3":
            print("Hasta pronto!")
            exit()
        
        else:
            print("Opción no válida")

# --- Página de Control de Niños ---
def pagina_control_niños(user_id):
    while True:
        print("\n=== PANEL DE CONTROL ===")
        print("1. Ver información de niños")
        print("2. Añadir niño")
        print("3. Añadir tap")
        print("4. Cerrar sesión")
        
        opcion = input("Opción: ").strip()
        token_data = cargar_token()
        headers = {'Authorization': f'Bearer {token_data["token"]}'}
        
        if opcion == "1":
            response = requests.get(
                f"{BASE_URL}/getchildren/{user_id}",
                headers=headers
            )
            if response.status_code == 200:
                mostrar_info_ninos(response.json())
            else:
                print("Error:", response.json().get("error"))
        
        elif opcion == "2":
            nombre = input("Nombre del niño: ")
            response = requests.post(
                f"{BASE_URL}/children",
                json={"name": nombre},
                headers=headers
            )
            if response.status_code == 201:
                print("¡Niño añadido exitosamente!")
            else:
                print("Error:", response.json().get("error"))
        
        elif opcion == "3":
            child_id = input("ID del niño: ")
            init = input("Fecha de inicio (YYYY-MM-DDTHH:MM:SS): ")
            end = input("Fecha de fin (opcional): ") or None
            
            data = {"child_id": child_id, "init": init}
            if end:
                data["end"] = end
                
            response = requests.post(
                f"{BASE_URL}/taps",
                json=data,
                headers=headers
            )
            if response.status_code == 201:
                print("¡Tap registrado!")
            else:
                print("Error:", response.json().get("error"))
        
        elif opcion == "4":
            eliminar_token()
            print("Sesión cerrada.")
            break
        
        else:
            print("Opción no válida")

# --- Funciones auxiliares ---
def mostrar_info_ninos(children):
    if not children:
        print("\nNo hay niños asociados.")
        return
    
    print("\n=== INFORMACIÓN DE NIÑOS ===")
    for child in children:
        print(f"\nID: {child['id']} | Nombre: {child['name']}")
        print(f"Horas de sueño promedio: {child['sleep_average']}")
        
        if child["taps"]:
            print("\nTaps registrados:")
            for tap in child["taps"]:
                print(f"- {tap['init']} a {tap['end'] or 'En progreso'}")
        else:
            print("\nNo hay taps registrados.")

# --- Ejecución ---
if __name__ == "__main__":
    pagina_login()