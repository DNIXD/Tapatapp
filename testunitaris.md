# Test Unitarios
## Que son los test unitarios?
Los test unitarios son un codigo que verifica la precision de una pequeña parte de otro codigo<br> ç
normalmente siendo este codigo a comprobar una funcion o metodo<br>

## Herrameintas de test unitario para python 
Unittest (pyTest)<br>

Ventajas<br>

Viene incluido con el lenguaje y es uno de los más usados en los proyectos Python.<br>
Suele tener compatibilidad con el resto de librerías como Pytest, por lo que se recomienda empezar con él.<br>
Tiene incluido un servicio de discovery que permite encontrar y ejecutar lo tests automáticamente.<br>
Muy sencillo de utilizar, tiene algunos métodos que controlan el ciclo de vida de tus tests.<br>

Desventajas<br>

Funcionalidades limitadas para complementar el testing cómo poder saber el coverage de tu aplicación<br>
Sin extensiones o sistema de plugins para completar su funcionalidad cómo tiene pytest.<br>

Pytest<br>

Ventajas<br>

Altamente extensible, tiene un montón de plugins y extensiones desarrolladas por la comunidad, que, si una funcionalidad no está <br>incluida, seguramente habrá un plugin que la implemente.<br>
La curva de aprendizaje no es muy alta, en parte por la buena documentación.<br>
Compatible con la sintaxis de unittest.<br>
Herramienta realmente potente de discovery automático para tus tests.<br>

Desventajas<br>

Ha medida que trabajas con la librería y quieres profundizar, la documentación empieza a ser más confusa.<br>
Muchos plugins en desuso y que no han sido mantenidos por sus autores, por lo que tienes que tener cuidado de cuales utilizas.<br>

Hypothesis<br>

Ventajas<br>

Muy sencillo de utilizar sobre todo para casos de uso básicos.<br>
La comunidad le ha mostrado mucho apoyo, y varias empresas grandes han escrito artículos sobre como la utilizan para añadir <br> resiliencia a sus aplicaciones. <br>

Desventajas <br>

Para probar casuísticas algo complejas, puedes necesitar bastante tiempo preparando el test.<br>
Curva de aprendizaje elevada, debido sobre todo al cambio de paradigma en nuestro testing.<br>

## Funcionamiento de unittest

Qué es:<br>
Framework de pruebas unitarias incluido en Python (inspirado en JUnit).<br>

Estructura básica:<br>

import unittest<br>

class TestEjemplo(unittest.TestCase):<br>
    def test_algo(self):<br>
        self.assertEqual(1 + 1, 2)<br>
3 partes clave:<br>

TestCase: Clases que contienen los tests (heredan de unittest.TestCase)<br>

Assertions: Métodos como assertEqual(), assertTrue(), etc.<br>

Test Runner: Ejecuta los tests y muestra resultados (unittest.main())<br>

Métodos útiles:<br>

setUp()/tearDown(): Preparar/limpiar antes/después de cada test<br>

setUpClass()/tearDownClass(): Para toda la clase de tests<br>

Cómo ejecutar:<br>

python -m unittest archivo_test.py<br>
o desde el código:<br>
if __name__ == '__main__':<br>
    unittest.main()<br>
Ventajas:<br>
Incluido en Python (no requiere instalación extra)<br>
Estructura clara y organizada<br>
Integración con herramientas CI/CD<br>

Ideal para: Proyectos que necesitan pruebas mantenibles y escalables.<br>