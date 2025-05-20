import random
import math

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def contains(self, p):
        return (self.center[0] - p[0])**2 + (self.center[1] - p[1])**2 <= self.radius**2


def getCircleCenter(bx, by, cx, cy):
    b = bx * bx + by * by
    c = cx * cx + cy * cy
    d = bx * cy - by * cx

    centro = [(bx * cy - by * cx) / (2 * d), (bx * cx - by * cy) / (2 * d)]

    return centro



def circleFrom(a, b, c):
    i = getCircleCenter(b[0] - a[0], b[1] - a[1], c[0] - a[0], c[1] - a[1])
    i[0] = a[0]
    i[1] = a[1]
    return Circle(i, math.dist(i, a))


def trivial(P, k):
    if k == 0:
        return Circle((0, 0), 0)
    elif k == 1:
        return Circle(P[0], 0)
    elif k == 2:
        print("P[0]: ", P[0])
        return Circle(((P[0][0] + P[1][0]) / 2, (P[0][1] + P[1][1]) / 2), math.dist(P[0], P[1]) / 2)
    elif k == 3:
        print("P[0]: ", P[0])
        s = circleFrom(P[0], P[1], P[2])
        return s


def MEC(P, k ,R):
    if k == 1 or len(R) == 3:
        return trivial(P, k) 
    i = random.choice(range(k))
    p = P[i]
    P[i], P[k-1] = P[k-1], P[i]
    D = MEC(P, k-1, R)
    print("d momentaneo: ", D.center, D.radius)
    if D.contains(p):
        print("Point", p[0], p[1] ,"is inside the circle")
        return D
    else:
        print("Point", p[0], p[1] ,"is not inside the circle")
        return MEC(P, k-1, R + [p])

P = [(1, 5), (-1, 4), (7, 1)]

solution = MEC(P, len(P), [])
print("Minimum Enclosing Circle:")
print(f"Center: {solution.center}, Radius: {solution.radius}")
