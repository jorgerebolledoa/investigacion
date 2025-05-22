#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>
#include <time.h>
#include <pthread.h>

unsigned char Bandera = 0;
#define MAX_SIZE 100

struct Node {
    double x;
    double y;
    struct Node *next;
};

struct Node *insertar(struct Node *p, unsigned int x, unsigned char y) {//Función de manipulación de lista en la cual se guardarán los nodos visitados.
    struct Node *q, *l;
    if (p == NULL) { // p is an empty list
        q = calloc(1, sizeof(struct Node));
        q->valor = x;
        q->marca = y;
        q->next = NULL;
        p = q;
    } else {
        q = calloc(1, sizeof(struct Node));
        q->valor = x;
        q->marca = y;
        q->next = NULL;
        l = p;
        while (l->next != NULL)
            l = l->next;
        l->next = q;
    }
    return p;
}
struct Node *DeleteFirst(struct Node *p) {
    struct Node *q;
    if (p != NULL) {
        q = p->next;
        free(p);
        return q;
    }
    return NULL;
}

void PrintList(struct Node *p) {
    while (p != NULL) {
        printf("[ %d, %d ]",p->valor, p->marca);
        p = p->next;
    }
    printf("\n\n\n");
}

struct ArgsDFS {
    unsigned int myid;
    unsigned int hebras;
    unsigned int q_revisar;
    struct Node *puntos_por_revisar;
    puntos pts[]; 
};



// Structure to represent a 2D point
typedef struct {
    double x, y;
} Point;

// Structure to represent a 2D circle
typedef struct {
    Point c;
    double r;
} Circle;

// Function to return the euclidean distance between two points
double dist(Point a, Point b) {
    return sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2));
}

// Function to check whether a point lies inside or on the boundaries of the circle
int isInside(Circle c, Point p) {
    return dist(c.c, p) <= c.r;
}

// Helper method to get a circle defined by 3 points
Point getCircleCenter(double bx, double by, double cx, double cy) {
    double b = bx * bx + by * by;
    double c = cx * cx + cy * cy;
    double d = bx * cy - by * cx;
    Point center = {
        (cy * b - by * c) / (2 * d),
        (bx * c - cx * b) / (2 * d)
    };
    return center;
}

// Function to return a unique circle that intersects three points
Circle circleFrom3(Point a, Point b, Point c) {
    Point i = getCircleCenter(b.x - a.x, b.y - a.y, c.x - a.x, c.y - a.y);
    i.x += a.x;
    i.y += a.y;
    Circle circle = {i, dist(i, a)};
    return circle;
}

// Function to return the smallest circle that intersects 2 points
Circle circleFrom2(Point a, Point b) {
    // Set the center to be the midpoint of a and b
    Point c = {(a.x + b.x) / 2.0, (a.y + b.y) / 2.0};
    // Set the radius to be half the distance AB
    Circle circle = {c, dist(a, b) / 2.0};
    return circle;
}

// Function to check whether a circle encloses the given points
int isValidCircle(Circle c, Point* p, int p_size) {
    // Iterating through all the points to check whether the points lie inside the circle or not
    for (int i = 0; i < p_size; i++) {
        if (!isInside(c, p[i])) {
            return 0;
        }
    }
    return 1;
}

// Function to return the minimum enclosing circle for N <= 3
Circle minCircleTrivial(Point* p, int p_size) {
    assert(p_size <= 3);
    if (p_size == 0) {
        Circle c = {{0, 0}, 0};
        return c;
    }
    else if (p_size == 1) {
        Circle c = {p[0], 0};
        return c;
    }
    else if (p_size == 2) {
        return circleFrom2(p[0], p[1]);
    }

    // To check if MEC can be determined by 2 points only
    for (int i = 0; i < 3; i++) {
        for (int j = i + 1; j < 3; j++) {
            Circle c = circleFrom2(p[i], p[j]);
            if (isValidCircle(c, p, p_size)) {
                return c;
            }
        }
    }
    return circleFrom3(p[0], p[1], p[2]);
}

// Returns the MEC using Welzl's algorithm
// Takes a set of input points p and a set r points on the circle boundary.
// n represents the number of points in p that are not yet processed.
Circle welzlHelper(Point* p, Point* r, int p_size, int r_size, int n) {
    // Base case when all points processed or |r| = 3
    if (n == 0 || r_size == 3) {
        return minCircleTrivial(r, r_size);
    }

    // Pick a random point randomly
    int idx = rand() % n;
    Point pnt = p[idx];

    // Put the picked point at the end of p since it's more efficient than
    // deleting from the middle of the array
    Point temp = p[idx];
    p[idx] = p[n - 1];
    p[n - 1] = temp;

    // Get the MEC circle d from the set of points p - {p}
    Circle d = welzlHelper(p, r, p_size, r_size, n - 1);

    // If d contains pnt, return d
    if (isInside(d, pnt)) {
        return d;
    }

    // Otherwise, must be on the boundary of the MEC
    // Add point to r (need to create new array with size+1)
    Point* new_r = malloc((r_size + 1) * sizeof(Point));
    for (int i = 0; i < r_size; i++) {
        new_r[i] = r[i];
    }
    new_r[r_size] = pnt;

    Circle result = welzlHelper(p, new_r, p_size, r_size + 1, n - 1);
    free(new_r);
    return result;
}

Circle welzl(Point* p, int p_size) {
    // Shuffle the points
    for (int i = p_size - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        Point temp = p[i];
        p[i] = p[j];
        p[j] = temp;
    }
    
    Point* r = NULL;
    Circle result = welzlHelper(p, r, p_size, 0, p_size);
    return result;
}

void PrintStack(Stack s)
{
    // If stack is empty
    if (s.empty())
        return;

// Extract top of the stack
    int x = s.top();

    s.pop();

    cout << x << ' ';

    PrintStack(s);
    s.push(x);
}

void *Process(void *arg){ //Función que coordina los hilos
    struct ArgsDFS *args;
    args = (struct ArgsDFS *)arg;

    while(Bandera == 0){
        if(puntos!=NULL && i<args->q_revisar){
            insertar(args->puntos_por_revisar, args->puntos_totales->x)
            i = i + 1;
        }
    }
        } 
        if(Bandera == 0){ //Ejecutamos la busqueda desde el vertice nsimo
            Alcanzar_nodos(args);
        }
        cantidad_revisados = cantidad_revisados + 1;
        args->nsimo_vertice = args->nsimo_vertice + args->hebras;//Actualizar el vértice a revisar.
    }
}

int main(int argc) {
    srand(time(NULL)); // Seed the random number generator

    Point points[] = {{3, -4}, {5, 3}, {-2, 1}};
    int n = sizeof(points) / sizeof(points[0]);
    
    //echar todos los puntos a los h stacks(h = cantidad de hilos)
    thread = calloc(k, sizeof(pthread_t));
    args = calloc(k, sizeof(struct ArgsDFS *)); 
    pthread_attr_init(&attribute);
    for (i = 0; i < k; i = i + 1) {
        args[i] = calloc(1, sizeof(struct ArgsDFS));
        args[i]->myid = i;  
        args[i]->hebras = k;    //Entrega la cantidad de hebras a usar
        args[i]->q_revisar = n/k; //cada nodo sabe cuantos puntos revisará
        args[i]->puntos_por_revisar = NULL;
        args[i]->puntos_totales = points;
        pthread_create(&thread[i], &attribute, Process, (void *)args[i]);
    }
    for (i = 0; i < k; i = i + 1) {
        pthread_join(thread[i], &exit_status); 
    }

    Circle mec = welzl(points, n);
    printf("%f %f %f", mec.c.x, mec.c.y, mec.r);
    return 0;
}