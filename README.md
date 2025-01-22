# Tapatapp

Hola!!

[Descripcion del Proyecto](desTapatapp.md)

[Receriemitnos Tecnicos](RequerimientosTecnicos.md)

[Diagram del prototipo 1](Prototipo1_diagrama.mermaid)

[HTTP Request](httpRequest.md)
[HTTP Response](httpResponse.md)

## Definicion de los EndPoints del WebService

Definicion de los EndPoints del Servicio Web:

Que necesitaremos para cada EndPoint

Descripció: Un servico que consultara si exixte un usuario por su nombre de usuario
HOST: 192.168.144.161:10050
End-point (URL): http://192.168.144.161:10050/users/getUser
Method: GET
Tipus de petició (headers): Devolvera un html si el usuario exsite y otro si no existe
Parametres que necessita la petició: (identifica els paràmetres i posa exemples en el cas de peticions GET) El nombre del usuario y algo mas especial o especifico como el correo o la contraseña.
Resposta: Si existe el usaurio seria algo como, "Bienvenido de vuelta (Nombre de usuario)" si no existe diria algo como "No se ha encontrado al usuario (Nombre de suaurio)"