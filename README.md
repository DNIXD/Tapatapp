# Tapatapp

Hola!!

[Descripcion del Proyecto](desTapatapp.md)

[Requeriemitnos Tecnicos](RequerimientosTecnicos.md)

[Diagram del prototipo 1](Prototipo1_diagrama.mermaid)

[HTTP Request](httpRequest.md)
[HTTP Response](httpResponse.md)

## Definicion de los EndPoints del WebService

Definicion de los EndPoints del Servicio Web:

Que necesitaremos para cada EndPoint

Descripció: Un servico que consultara si exixte un usuario por su nombre de usuario <br>
HOST: 192.168.144.161:10050 <br>
End-point (URL): http://192.168.144.161:10050/users/getUser <br>
Method: GET <br>
Tipus de petició: Devolvera un html si el usuario exsite y otro si no existe <br>
Parametres que necessita la petició: El nombre del usuario y algo mas especial o especifico como el correo o la contraseña.<br>
Resposta: Si existe el usaurio seria algo como, "Bienvenido de vuelta (Nombre de usuario)" si no existe diria algo como "No se ha encontrado al usuario (Nombre de usuario)"


| Descripción  | End-point     | Method     |Tipo de petición|Parametros| Respuesta|
| :---        |  :---        |  :---        |  :---         |  :---     |  :--- | 
| Obtener datos de un usuario  | /prototip1/getuser|GET | application/json   |  username (string) |  Codigo 200: {"email": "prueba@gmail.com",   "id": 1,   "password":  "12345",   "username": "usuari1" } Codigo 404: {error: Usuario no encontrado} Codigo 400: {error: Parametro no introducido}     |
<br>


## Prototipo 2
[Prototipo2](prototip2.md)