#include <stdlib.h>
#include <string.h>
#include "time.h"
#include <stdbool.h>
#include <stdio.h>
#define MAX_SIZE 100

typedef struct {
    double cx; //coord x del centro
    double cy; //coord y del centro
    double r;  //radio
} Circle;

typedef struct {
    Circle items[MAX_SIZE];  // Cambiado a array de Circle
    int front;
    int rear;               // Cambiado a int para índice
} Queue;

// Function to initialize the queue
void initializeQueue(Queue* q) {
    q->front = -1;
    q->rear = -1;
} 

// Function to check if the queue is empty
bool isEmpty(Queue* q) {
    return (q->front == -1 || q->front > q->rear);
}

// Function to check if the queue is full
bool isFull(Queue* q) {
    return (q->rear == MAX_SIZE - 1);
}

// Function to add an element to the queue (Enqueue operation)
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

// Function to remove an element from the queue (Dequeue operation)
Circle dequeue(Queue* q) {
    Circle emptyCircle = {0.0, 0.0, 0.0};
    if (isEmpty(q)) {
        printf("Queue is empty\n");
        return emptyCircle;
    }
    Circle item = q->items[q->front];
    q->front++;
    
    // Reset queue when empty
    if (q->front > q->rear) {
        initializeQueue(q);
    }
    return item;
}

// Function to get the element at the front of the queue (Peek operation)
Circle peek(Queue* q) {
    Circle emptyCircle = {0.0, 0.0, 0.0};
    if (isEmpty(q)) {
        printf("Queue is empty\n");
        return emptyCircle;
    }
    return q->items[q->front];
}

// Function to print the current queue
void printQueue(Queue* q) {
    if (isEmpty(q)) {
        printf("Queue is empty\n");
        return;
    }

    printf("Current Queue: \n");
    for (int i = q->front; i <= q->rear; i++) {
        printf("Circle %d: center (%.2f, %.2f), radius %.2f\n",
               i - q->front + 1, q->items[i].cx, q->items[i].cy, q->items[i].r);
    }
}

void ReadData(Queue *q, int n) {
    Circle ci;
    for(int i = 0; i < n; i++) {
        scanf("%lf", &ci.cx);
        
        scanf("%lf", &ci.cy);
        
        ci.r = 0.0; // Assuming radius is not provided, set to 0.0

        enqueue(q, ci);
    }
    printQueue(q);
}
int main(int argc, char* argv[]) {
    Queue q;
    initializeQueue(&q);
    Circle ci;
    int n;

    n = atoi(argv[1]);
    ReadData(&q, n);
    /*// Enqueue first circle
    ci.cx = 1.0;
    ci.cy = 2.0;
    ci.r = 3.0;
    enqueue(&q, ci);
    
    // Enqueue second circle
    ci.cx = 4.0;
    ci.cy = 5.0;
    ci.r = 6.0;
    enqueue(&q, ci);
    
    printQueue(&q);

    // Peek front element
    Circle front = peek(&q);
    printf("Front element: center (%.2f, %.2f), radius %.2f\n", front.cx, front.cy, front.r);

    // Dequeue an element
    Circle dequeued = dequeue(&q);
    printf("Dequeued: center (%.2f, %.2f), radius %.2f\n", dequeued.cx, dequeued.cy, dequeued.r);
    printQueue(&q);

    // Peek front element after dequeue
    front = peek(&q);
    printf("Front element after dequeue: center (%.2f, %.2f), radius %.2f\n", front.cx, front.cy, front.r);
    */
    return 0;
}