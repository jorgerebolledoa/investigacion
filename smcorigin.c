#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>
#include <stdio.h>
#include <float.h>
#define MAX_SIZE 100

typedef struct {
    double x;
    double y;
} Punto;

typedef struct {
    Punto centro;
    Punto original1;
    Punto original2;
    Punto original3; // Para círculos de 3 puntos
    double r;
} Circle;

typedef struct {
    Circle items[MAX_SIZE];
    int front;
    int rear;
} Queue;

// Lista de todos los puntos ingresados
typedef struct NodoPunto {
    Punto punto;
    struct NodoPunto* siguiente;
} NodoPunto;

NodoPunto* listaPuntos = NULL;

// Funciones auxiliares
void agregarPuntoALista(Punto p) {
    NodoPunto* nuevo = (NodoPunto*)malloc(sizeof(NodoPunto));
    nuevo->punto = p;
    nuevo->siguiente = listaPuntos;
    listaPuntos = nuevo;
}

void liberarListaPuntos() {
    NodoPunto* actual = listaPuntos;
    while (actual != NULL) {
        NodoPunto* temp = actual;
        actual = actual->siguiente;
        free(temp);
    }
    listaPuntos = NULL;
}

// Funciones de la cola (sin cambios)
void initializeQueue(Queue* q) {
    q->front = -1;
    q->rear = -1;
} 

// Verificar si la cola está vacía
bool isEmpty(Queue* q) {
    return (q->front == -1 || q->front > q->rear);
}

// Verificar si la cola está llena
bool isFull(Queue* q) {
    return (q->rear == MAX_SIZE - 1);
}

// Añadir un elemento a la cola
void enqueue(Queue* q, Circle value) {
    if (isFull(q)) {
        printf("Queue is full\n");
        return;
    }
    if (isEmpty(q)) {
        q->front = 0;
    }
    q->rear++;
    q->items[q->rear] = value;
}

// Eliminar un elemento de la cola
Circle dequeue(Queue* q) {
    Circle emptyCircle = {0.0, 0.0, 0.0};
    if (isEmpty(q)) {
        printf("Queue is empty\n");
        return emptyCircle;
    }
    Circle item = q->items[q->front];
    q->front++;
    
    if (q->front > q->rear) {
        initializeQueue(q);
    }
    return item;
}

// Obtener el elemento frontal de la cola
Circle peek(Queue* q) {
    Circle emptyCircle = {0.0, 0.0, 0.0};
    if (isEmpty(q)) {
        printf("Queue is empty\n");
        return emptyCircle;
    }
    return q->items[q->front];
}

// Imprimir la cola actual
void printQueue(Queue* q) {
    if (isEmpty(q)) {
        printf("Queue is empty\n");
        return;
    }

    printf("Current Queue: \n");
    for (int i = q->front; i <= q->rear; i++) {
        printf("Circle %d: center (%.2f, %.2f), radius %.2f\n",
               i - q->front + 1, q->items[i].centro.x, q->items[i].centro.y, q->items[i].r);
    }
}

double DistanciaDosPuntos(Punto p1, Punto p2) {
    return sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y));
}

Circle TwoPointCircle(Punto p1, Punto p2) {
    Circle result;
    result.centro.x = (p1.x + p2.x) / 2.0;
    result.centro.y = (p1.y + p2.y) / 2.0;
    result.r = DistanciaDosPuntos(p1, result.centro);
    result.original1 = p1;
    result.original2 = p2;
    result.original3.x = 0; result.original3.y = 0; // Inicializar
    return result;
}

// Crea un círculo a partir de 3 puntos (circunferencia circunscrita)
Circle ThreePointCircle(Punto a, Punto b, Punto c) {
    Circle result;
    
    // Calculamos el circuncentro
    double D = 2 * (a.x*(b.y - c.y) + b.x*(c.y - a.y) + c.x*(a.y - b.y));
    result.centro.x = ((a.x*a.x + a.y*a.y) * (b.y - c.y) + 
                     (b.x*b.x + b.y*b.y) * (c.y - a.y) + 
                     (c.x*c.x + c.y*c.y) * (a.y - b.y));
    result.centro.x /= D;
    
    result.centro.y = ((a.x*a.x + a.y*a.y) * (c.x - b.x) + 
                     (b.x*b.x + b.y*b.y) * (a.x - c.x) + 
                     (c.x*c.x + c.y*c.y) * (b.x - a.x));
    result.centro.y /= D;
    
    result.r = DistanciaDosPuntos(result.centro, a);
    result.original1 = a;
    result.original2 = b;
    result.original3 = c;
    
    return result;
}

// Verifica si un punto está dentro de un círculo
bool puntoEnCirculo(Punto p, Circle c) {
    return DistanciaDosPuntos(p, c.centro) <= c.r + 1e-6; // Pequeño margen para errores
}

// Verifica si todos los puntos están dentro del círculo
bool todosPuntosDentro(Circle c) {
    NodoPunto* actual = listaPuntos;
    while (actual != NULL) {
        if (!puntoEnCirculo(actual->punto, c)) {
            return false;
        }
        actual = actual->siguiente;
    }
    return true;
}

// Encuentra los puntos que no están en el círculo
NodoPunto* obtenerPuntosFuera(Circle c) {
    NodoPunto* fuera = NULL;
    NodoPunto* actual = listaPuntos;
    
    while (actual != NULL) {
        if (!puntoEnCirculo(actual->punto, c)) {
            NodoPunto* nuevo = (NodoPunto*)malloc(sizeof(NodoPunto));
            nuevo->punto = actual->punto;
            nuevo->siguiente = fuera;
            fuera = nuevo;
        }
        actual = actual->siguiente;
    }
    
    return fuera;
}

// Procesa dos círculos según la nueva lógica
Circle procesarCirculos(Circle c1, Circle c2) {
    double d1 = DistanciaDosPuntos(c1.original1, c2.original1);
    double d2 = DistanciaDosPuntos(c1.original1, c2.original2);
    double d3 = DistanciaDosPuntos(c1.original2, c2.original1);
    double d4 = DistanciaDosPuntos(c1.original2, c2.original2);
    double d5 = DistanciaDosPuntos(c1.original1, c1.original2);
    double d6 = DistanciaDosPuntos(c2.original1, c2.original2);
    double ds = fmax(fmax(d1, d2), fmax(d3, d4));
    ds = fmax(ds, fmax(d5, d6));
    Circle mejorCirculo;
    Punto pmedio;
    
    // Crear círculo inicial con los dos puntos más distantes
    if (ds == d1) {
        pmedio.x = (c1.original1.x + c2.original1.x) / 2.0;
        pmedio.y = (c1.original1.y + c2.original1.y) / 2.0;
        mejorCirculo = TwoPointCircle(c1.original1, c2.original1);
    }
    else if (ds == d2) {
        pmedio.x = (c1.original1.x + c2.original2.x) / 2.0;
        pmedio.y = (c1.original1.y + c2.original2.y) / 2.0;
        mejorCirculo = TwoPointCircle(c1.original1, c2.original2);
    }
    else if (ds == d3) {
        pmedio.x = (c1.original2.x + c2.original1.x) / 2.0;
        pmedio.y = (c1.original2.y + c2.original1.y) / 2.0;
        mejorCirculo = TwoPointCircle(c1.original2, c2.original1);
    }
    else if(ds == d4) {
        pmedio.x = (c1.original2.x + c2.original2.x) / 2.0;
        pmedio.y = (c1.original2.y + c2.original2.y) / 2.0;
        mejorCirculo = TwoPointCircle(c1.original2, c2.original2);
    }
    else if (ds == d5) {
        pmedio.x = (c1.original1.x + c1.original2.x) / 2.0;
        pmedio.y = (c1.original1.y + c1.original2.y) / 2.0;
        mejorCirculo = TwoPointCircle(c1.original1, c1.original2);
    }
    else {
        pmedio.x = (c2.original1.x + c2.original2.x) / 2.0;
        pmedio.y = (c2.original1.y + c2.original2.y) / 2.0;
        mejorCirculo = TwoPointCircle(c2.original1, c2.original2);
    }
    
    // Verificar si todos los puntos están incluidos
    if (todosPuntosDentro(mejorCirculo)) {
        return mejorCirculo;
    }
    
    // Si no, buscar el mejor círculo de 3 puntos
    NodoPunto* puntosFuera = obtenerPuntosFuera(mejorCirculo);
    Circle mejorCirculo3Puntos;
    double mejorRadio = DBL_MAX;
    bool encontrado = false;
    
    // Probar con cada punto fuera como tercer punto
    NodoPunto* actual = puntosFuera;
    while (actual != NULL) {
        Circle circulo3Puntos;
        
        if (ds == d1) {
            circulo3Puntos = ThreePointCircle(c1.original1, c2.original1, actual->punto);
        }
        else if (ds == d2) {
            circulo3Puntos = ThreePointCircle(c1.original1, c2.original2, actual->punto);
        }
        else if (ds == d3) {
            circulo3Puntos = ThreePointCircle(c1.original2, c2.original1, actual->punto);
        }
        else {
            circulo3Puntos = ThreePointCircle(c1.original2, c2.original2, actual->punto);
        }
        
        if (todosPuntosDentro(circulo3Puntos) && circulo3Puntos.r < mejorRadio) {
            mejorCirculo3Puntos = circulo3Puntos;
            mejorRadio = circulo3Puntos.r;
            encontrado = true;
        }
        
        actual = actual->siguiente;
    }
    
    // Liberar memoria de la lista de puntos fuera
    while (puntosFuera != NULL) {
        NodoPunto* temp = puntosFuera;
        puntosFuera = puntosFuera->siguiente;
        free(temp);
    }
    
    if (encontrado) {
        return mejorCirculo3Puntos;
    }
    
    // Si no se encontró un círculo de 3 puntos válido, devolver el original
    return mejorCirculo;
}

void ReadData(Queue *q, int n) {
    Punto p1, p2;
    Circle ci;
    for(int i = 0; i < n/2; i++) {
        scanf("%lf %lf %lf %lf", &p1.x, &p1.y, &p2.x, &p2.y);
        agregarPuntoALista(p1);
        agregarPuntoALista(p2);
        ci = TwoPointCircle(p1, p2);
        enqueue(q, ci);
    }
    printf("Queue after reading data:\n");
    printQueue(q);
}

int main(int argc, char* argv[]) {
    Queue q;
    initializeQueue(&q);
    int n = atoi(argv[1]);
    
    ReadData(&q, n);
    int limite = n/4 + 1;
    
    for(int i = 0; i < limite; i++) {
        Circle c1 = dequeue(&q);
        Circle c2 = dequeue(&q);
        
        Circle nuevoCirculo = procesarCirculos(c1, c2);
        enqueue(&q, nuevoCirculo);
        
        printf("Procesando par de círculos %d...\n", i+1);
        printf("Nuevo círculo: centro (%.2f, %.2f), radio %.2f\n", 
               nuevoCirculo.centro.x, nuevoCirculo.centro.y, nuevoCirculo.r);
        
        if (nuevoCirculo.original3.x != 0 || nuevoCirculo.original3.y != 0) {
            printf("Definido por 3 puntos\n");
        } else {
            printf("Definido por 2 puntos\n");
        }
    }
    
    printf("\nCírculo final:\n");
    Circle final = dequeue(&q);
    printf("Centro: (%.2f, %.2f)\n", final.centro.x, final.centro.y);
    printf("Radio: %.2f\n", final.r);
    printf("Puntos definitorios:\n");
    printf("1: (%.2f, %.2f)\n", final.original1.x, final.original1.y);
    printf("2: (%.2f, %.2f)\n", final.original2.x, final.original2.y);
    if (final.original3.x != 0 || final.original3.y != 0) {
        printf("3: (%.2f, %.2f)\n", final.original3.x, final.original3.y);
    }
    
    liberarListaPuntos();
    return 0;
}