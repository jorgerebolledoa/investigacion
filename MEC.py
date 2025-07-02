import random
import math
import time

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def contains(self, p):
        if p is None:
            return False
        return (self.center[0] - p[0])**2 + (self.center[1] - p[1])**2 <= self.radius**2

def getCircleCenter(bx, by, cx, cy):
    b = bx * bx + by * by
    c = cx * cx + cy * cy
    d = bx * cy - by * cx
    if d == 0:
        return None
    return [(cy * b - by * c) / (2 * d), (bx * c - cx * b) / (2 * d)]

def circleFrom(a, b, c):
    i = getCircleCenter(b[0] - a[0], b[1] - a[1], c[0] - a[0], c[1] - a[1])
    if i is None:
        return trivial([a, b, c], 2)
    i[0] += a[0]
    i[1] += a[1]
    radius = math.dist(i, a)
    return Circle(i, radius)

def trivial(P, k):
    if k == 0 or not P:
        return Circle((0, 0), 0)
    elif k == 1:
        return Circle(P[0], 0)
    elif k == 2:
        center = ((P[0][0] + P[1][0]) / 2, (P[0][1] + P[1][1]) / 2)
        radius = math.dist(P[0], P[1]) / 2
        return Circle(center, radius)
    elif k == 3:
        return circleFrom(P[0], P[1], P[2])

def MEC(P, k=None, R=None):
    if k is None:
        k = len(P)
    if R is None:
        R = []
    
    if k == 0 or len(P) == 0:
        return trivial(R, len(R))
    
    if k == 1 or len(R) == 3:
        return trivial(P, k)
    
    i = random.randint(0, k-1)
    p = P[i]
    P[i], P[k-1] = P[k-1], P[i]
    
    D = MEC(P, k-1, R)
    if D is None:
        return MEC(P, k-1, R + [p])
    
    if D.contains(p):
        return D
    else:
        return MEC(P, k-1, R + [p])

def read_points_from_file(filename):
    """Lee puntos desde un archivo txt en formato (x, y)"""
    points = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    # Remover paréntesis y dividir por coma
                    line = line.replace('(', '').replace(')', '')
                    x, y = map(float, line.split(', '))
                    points.append((x, y))
        return points
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {filename}")
        return []
    except Exception as e:
        print(f"Error al leer el archivo {filename}: {e}")
        return []

if __name__ == "__main__":
    # Leer puntos desde archivo
    points = read_points_from_file('puntos.txt')
    
    if not points:
        print("No se pudieron cargar puntos del archivo.")
        exit(1)
    
    print(f"Calculando círculo mínimo para {len(points)} puntos...")
    
    # Ejecutar algoritmo MEC
    start_time = time.time()
    circle = MEC(points)
    execution_time = (time.time() - start_time) * 1000
    
    # Mostrar resultados
    if circle is not None:
        print(f"Tiempo de ejecución: {execution_time:.2f} ms")
        print(f"Centro: ({circle.center[0]:.2f}, {circle.center[1]:.2f})")
        print(f"Radio: {circle.radius:.2f}")
        
        # Verificar que todos los puntos están dentro del círculo
        points_inside = sum(1 for p in points if circle.contains(p))
        print(f"Puntos dentro del círculo: {points_inside}/{len(points)}")
    else:
        print("Error: No se pudo calcular el círculo mínimo")
