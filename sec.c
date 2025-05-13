/* MEC(P, R):
1. if P = ∅ or |R| = 3 then
2. return trivial(R)
3. p = choose a point of P uniformly at random
4. D = MEC(P − {p}, R)
5. if p ∈ D then
6. return D
7. else
8. return MEC(P − {p}, R ∪ p)
*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <stdbool.h>

#define MAX_POINTS 100

typedef struct {
    double x, y;
} Point;

typedef struct {
    Point center;
    double radius;
} Circle;

// Function to calculate the distance between two points
double distance(Point a, Point b) {
    return sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y));
}

// Function to check if a point is inside a circle
bool is_inside(Circle c, Point p) {
    return distance(c.center, p) <= c.radius;
}

// Function to create a trivial circle from up to 3 points
Circle trivial(Point R[], int r_size) {
    if (r_size == 0) {
        return (Circle){{0, 0}, 0};
    } else if (r_size == 1) {
        return (Circle){R[0], 0};
    } else if (r_size == 2) {
        Point center = {(R[0].x + R[1].x) / 2, (R[0].y + R[1].y) / 2};
        double radius = distance(R[0], R[1]) / 2;
        return (Circle){center, radius};
    } else {
        // Calculate the circle passing through 3 points
        double ax = R[0].x, ay = R[0].y;
        double bx = R[1].x, by = R[1].y;
        double cx = R[2].x, cy = R[2].y;

        double d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by));
        double ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d;
        double uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d;

        Point center = {ux, uy};
        double radius = distance(center, R[0]);
        return (Circle){center, radius};
    }
}

// Recursive function to find the minimum enclosing circle
Circle MEC(Point P[], int p_size, Point R[], int r_size) {
    if (p_size == 0 || r_size == 3) {
        return trivial(R, r_size);
    }

    // Choose a random point from P
    int idx = rand() % p_size;
    Point p = P[idx];

    // Remove the chosen point from P
    P[idx] = P[p_size - 1];
    Circle D = MEC(P, p_size - 1, R, r_size);

    // Check if the chosen point is inside the circle
    if (is_inside(D, p)) {
        return D;
    }

    // Add the point to R and recurse
    R[r_size] = p;
    return MEC(P, p_size - 1, R, r_size + 1);
}

int main() {
    srand(time(NULL));

    Point P[MAX_POINTS] = {{0, 0}, {1, 0}, {0, 1}, {1, 1}, {0.5, 0.5}, {3, 3}, {7, 17}};
    int p_size = 5;

    Point R[3];
    int r_size = 0;

    Circle result = MEC(P, p_size, R, r_size);

    printf("Center: (%.2f, %.2f)\n", result.center.x, result.center.y);
    printf("Radius: %.2f\n", result.radius);

    return 0;
}


