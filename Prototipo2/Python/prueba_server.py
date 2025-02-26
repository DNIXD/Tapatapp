import requests

url_login = "http://127.0.0.1:5000/login"
url_children = "http://127.0.0.1:5000/getchildren"

def mostrar_info_usuario(user):
    print("Se ha iniciado sesion correctamente")
    print("")
    print("\n🆔 Información del Usuario")
    print(f"  👤 ID: {user['user_id']}")
    print(f"  📛 Usuario: {user['username']}")
    print(f"  📧 Email: {user['email']}")

def mostrar_info_ninos(children):
    if not children:
        print("\n🚸 No hay niños asociados a este usuario.")
        return
    
    print("\n👶 Información de los Niños")
    for child in children:
        print(f"  🆔 ID: {child['id']}")
        print(f"  👦 Nombre: {child['name']}")
        print(f"  🎂 Edad: {child['sleep_average']}")
        if child["taps"]:
            print("  📊 Taps:")
            for tap in child["taps"]:
                print(f"    - 🆔 ID:{tap['id']}, 📅 Fecha init: {tap['init']}, 📅 Fecha end: {tap['end']}")
        else:
            print("  ❌ No hay taps registrados.")

username = input("🔑 Usuario: ")
password = input("🔒 Contraseña: ")

login_response = requests.post(f"{url_login}", json={"username": username, "password": password})
if login_response.status_code != 200:
    print("\n❌ Error: Credenciales incorrectas.")
    exit()

user_data = login_response.json()
mostrar_info_usuario(user_data)

ver_ninos = input("\n👀 ¿Quieres ver la información de los niños? (s/n): ").strip().lower()
if ver_ninos == "s":
    children_response = requests.get(f"{url_children}/{user_data['user_id']}")
    if children_response.status_code == 200:
        children_data = children_response.json()
        mostrar_info_ninos(children_data)
    else:
        print("\n❌ No se encontraron niños asociados.")


