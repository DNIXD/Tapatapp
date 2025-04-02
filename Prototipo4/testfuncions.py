def resta(a, b):
    """Retorna la resta de dos nombres."""
    return a - b

def divideix(a, b):
    """Retorna la divisió de dos nombres. Retorna 'Error' si b és 0."""
    if b == 0:
        return "Error: divisió per zero"
    return a / b

print("Test de la funció divideix")
print("Test 1: ", divideix(10, 2))
print("Test 2: ", divideix(10, 0))

print("Test de la funció resta")
print("Test 1: ", resta(10, 2))