import random
import math
from mpi4py import MPI
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
        return trivial([a, b, c], 2)  # Devuelve el círculo más pequeño que contiene los 3 puntos
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

def distributed_MEC(points, k):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    if size != k:
        if rank == 0:
            print(f"Error: Se requieren {k} procesos pero hay {size} disponibles")
        return Circle((0,0), 0)
    
    # Dividir los puntos entre los procesos
    chunk_size = len(points) // k
    local_points = points[rank*chunk_size : (rank+1)*chunk_size]
    if rank == k-1:  # El último proceso toma los puntos restantes
        local_points = points[rank*chunk_size:]
    
    # Cada proceso calcula su círculo mínimo local
    local_circle = MEC(local_points)
    
    # Recopilar todos los círculos locales en el proceso 0
    all_circles = comm.gather(local_circle, root=0)
    
    if rank == 0:
        # Filtrar círculos None
        valid_circles = [c for c in all_circles if c is not None]
        
        if not valid_circles:
            return Circle((0,0), 0)
        
        # Recoger puntos de los círculos
        boundary_points = []
        for circle in valid_circles:
            boundary_points.append(circle.center)
            boundary_points.append((circle.center[0] + circle.radius, circle.center[1]))
            boundary_points.append((circle.center[0] - circle.radius, circle.center[1]))
            boundary_points.append((circle.center[0], circle.center[1] + circle.radius))
            boundary_points.append((circle.center[0], circle.center[1] - circle.radius))
        
        # Calcular el círculo mínimo que engloba todos estos puntos
        final_circle = MEC(boundary_points)
        return final_circle if final_circle is not None else Circle((0,0), 0)
    else:
        return None

def load_points_from_file(filename):
    """Carga puntos desde un archivo de texto"""
    points = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                # Formato: (x, y)
                # Remover paréntesis y dividir por coma
                coords = line.replace('(', '').replace(')', '').split(', ')
                x = float(coords[0])
                y = float(coords[1])
                points.append((x, y))
    return points

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    
    # Cargar puntos desde archivo (solo en rank 0 para evitar duplicados)
    if rank == 0:
        points = load_points_from_file('puntos.txt')
        print(f"Calculando círculo mínimo para {len(points)} puntos usando {comm.Get_size()} nodos...")
    else:
        points = None

    # Distribuir los puntos a todos los procesos
    points = comm.bcast(points, root=0)

    resultado_invalido = True
    while(resultado_invalido):
        s = time.time()
        k = comm.Get_size()
        result = distributed_MEC(points, k)
        distributed_time = (time.time() - s) * 1e3
        if result!=None and result.radius != 0:
            resultado_invalido = False
    
    if rank == 0:
        print(f"Tiempo distribuido: {distributed_time} ms")
        print("\nResultado Distribuido:")
        print(f"Centro: {result.center}, Radio: {result.radius}\n")
        #cantidad de puntos fuera de la circunferencia
        puntosdentro = 0
        for i in range(len(points)):
            if result.contains(points[i]):
                puntosdentro += 1
        print(f"Puntos dentro de la circunferencia: {puntosdentro} de {len(points)}\n")
        
        # Ejecutar algoritmo secuencial solo en rank 0
        resultado_invalido = True
        while(resultado_invalido):
            s2 = time.time()
            C = MEC(points)
            sequential_time = (time.time() - s2) * 1e3
            if C!=None and C.radius != 0:
                resultado_invalido = False

        print(f"Tiempo secuencial: {sequential_time} ms")
        print("Resultado Secuencial Emo Welz:")
        print(f"Centro: {C.center}, Radio: {C.radius}\n")
        puntosdentro = 0
        for i in range(len(points)):
            if C.contains(points[i]):
                puntosdentro += 1
        print(f"Puntos dentro de la circunferencia: {puntosdentro} de {len(points)}\n")
        
        print(f"Speedup: {sequential_time / distributed_time:.2f}x")