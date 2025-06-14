#include <stdlib.h>
#include <string.h>
#include "time.h"
#include <stdbool.h>
#include <math.h>
#include <stdio.h>
#define MAX_SIZE 100

typedef struct {
    double x; // coordenada x
    double y; // coordenada y
} Punto;

typedef struct {
    double m; // pendiente
    double b; // intersección en y
} Recta;

typedef struct {
    Punto centro ; // centro del círculo
    double r;  //radio
} Circle;

typedef struct {
    Circle items[MAX_SIZE];
    int front;
    int rear;
} Queue;

// Inicializar la cola
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
    Punto pcentro;
    double xcoord, ycoord;
    xcoord = (p1.x + p2.x) / 2.0;
    ycoord = (p1.y + p2.y) / 2.0;
    pcentro.x = xcoord;
    pcentro.y = ycoord;
    result.centro = pcentro;
    result.r = DistanciaDosPuntos(p1, result.centro);
    return result;
}

// Función para encontrar puntos de intersección entre recta y círculo
Punto encontrarPuntoInterseccionLejano(Recta recta, Circle circulo, Punto pmedio) {
    Punto puntos[2]; // Almacenará los dos puntos de intersección
    int numPuntos = 0;
    
    // Convertir la ecuación de la recta a forma general: Ax + By + C = 0
    double A = -recta.m;
    double B = 1.0;
    double C = -recta.b;
    
    double h = circulo.centro.x;
    double k = circulo.centro.y;
    double r = circulo.r;
    
    // Coeficientes de la ecuación cuadrática
    double a = A*A + B*B;
    double b = 2*(A*C + A*B*k - B*B*h);
    double c = B*B*h*h + C*C + 2*B*C*k + B*B*(k*k - r*r);
    
    double discriminante = b*b - 4*a*c;
    
    if (discriminante >= 0) {
        // Calcular los puntos de intersección
        double x1 = (-b + sqrt(discriminante)) / (2*a);
        double y1 = recta.m * x1 + recta.b;
        puntos[0].x = (int)round(x1);
        puntos[0].y = (int)round(y1);
        numPuntos++;
        
        if (discriminante > 0) {
            double x2 = (-b - sqrt(discriminante)) / (2*a);
            double y2 = recta.m * x2 + recta.b;
            puntos[1].x = (int)round(x2);
            puntos[1].y = (int)round(y2);
            numPuntos++;
        }
    }
    
    // Determinar qué punto está más lejos de pmedio
    if (numPuntos == 0) {
        // No hay intersección, devolver un punto inválido
        Punto invalido = {-1, -1};
        return invalido;
    } else if (numPuntos == 1) {
        return puntos[0];
    } else {
        // Calcular distancias al punto medio
        double dist1 = DistanciaDosPuntos(puntos[0], pmedio);
        double dist2 = DistanciaDosPuntos(puntos[1], pmedio);
        
        return (dist1 > dist2) ? puntos[0] : puntos[1];
    }
}

void ReadData(Queue *q, int n) {
    Punto p1, p2;
    Circle ci;
    for(int i = 0; i < n/2; i++) {
        scanf("%lf %lf %lf %lf", &p1.x, &p1.y, &p2.x, &p2.y);
        ci = TwoPointCircle(p1, p2);
        enqueue(q, ci);
    }
    printQueue(q);
}

int main(int argc, char* argv[]) {
    Queue q;
    Circle circle_solucion;
    Recta recta;
    Punto paux1, paux2, pmedio, centro_solucion;
    double radio_solucion;
    initializeQueue(&q);
    int n = atoi(argv[1]);
    ReadData(&q, n);
    int limite = n/4 + 1;
    
    //hasta aqui todo bien.
    
    for(int i = 0; i < limite; i++) {
        Circle c1 = dequeue(&q);
        Circle c2 = dequeue(&q);
        
        // Crear recta entre los centros de los círculos
        recta.m = (c2.centro.y - c1.centro.y) / (c2.centro.x - c1.centro.x);
        recta.b = c1.centro.y - recta.m * c1.centro.x;

        // Encontrar puntos de intersección paux1 y paux2  
        pmedio.x = (c1.centro.x + c2.centro.x) / 2.0; 
        pmedio.y = (c1.centro.y + c2.centro.y) / 2.0;      
        paux1 = encontrarPuntoInterseccionLejano(recta, c1, pmedio);
        paux2 = encontrarPuntoInterseccionLejano(recta, c2, pmedio);
        
        centro_solucion.x = (paux1.x + paux2.x) / 2.0;
        centro_solucion.y = (paux1.y + paux2.y) / 2.0;
        radio_solucion = DistanciaDosPuntos(paux1, centro_solucion);
        
        circle_solucion.centro = centro_solucion;
        circle_solucion.r = radio_solucion;
        enqueue(&q, circle_solucion);
    }
    printf("final queue:\n");
    printQueue(&q);
    return 0;
}