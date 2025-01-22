# HTTP Request

## GET request:
GET /index.html HTTP/1.1
Host: www.example.com

## POST request:
POST /api/login HTTP/1.1
Host: www.example.com
Content-Type: application/json
Content-Length: 45

{
  "username": "usuari",
  "password": "1234"
}

### Exemple petició Http  POST:

POST /submit HTTP/1.1
Host: example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 27


username=John+Doe&age=30&city=New+York


## Com funciona un HTTP request en un entorn real?
El client (navegador o aplicació) inicia una sol·licitud HTTP enviant-la a un servidor.
El servidor processa la sol·licitud i respon amb un HTTP response, que pot incloure dades (com una pàgina HTML) o un estat de confirmació (com 200 OK o 404 Not Found).

## curl
(acrònim de Client URL) és una eina de línia de comandes utilitzada per transferir dades des d'un client fins a un servidor, o viceversa, a través de diferents protocols de xarxa, com ara HTTP, HTTPS, FTP, SFTP, SMTP, POP3, i molts més.