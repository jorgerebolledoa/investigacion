#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>

unsigned int **matriz;
unsigned char Bandera = 0;

struct Node {
    unsigned int valor;
    unsigned char marca;
    struct Node *next;
};

struct ArgsDFS {
    unsigned int myid;
    unsigned int nsimo_vertice;
    unsigned int q_columnas;
    unsigned int hebras;
    unsigned char modo;
    struct Node *visitados; 
};
struct Node *DeleteFirst(struct Node *p) {
    struct Node *q;
    if (p != NULL) {
        q = p->next;
        free(p);
        return q;
    }
    return NULL;
}

struct Node *KillAll(struct Node *p) {
    while (p != NULL)
        p = DeleteFirst(p);
    return NULL;
}

void PrintList(struct Node *p) {
    while (p != NULL) {
        printf("[ %d, %d ]",p->valor, p->marca);
        p = p->next;
    }
    printf("\n\n\n");
}

unsigned int esta_en_la_lista(struct Node *p, int x) {//Función que chequea si un nodo ya ha sido visitado.
    if (p == NULL)
        return 0;
    else {
        while (p != NULL) {
            if (p->valor == x)
                return 1;
            p = p->next;
        }
        return 0;
    }
}

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

unsigned char todos_marcados(struct Node *visitados){
    while (visitados != NULL){
        if (visitados->marca == 0){
            return 0;
        }
        visitados = visitados->next;
    }
    return 1;
}

unsigned int completitud_visitas(struct Node *visitados, struct ArgsDFS *args){//Cuenta cuantos nodos logró visitar cada nodo mediante la lista visitados.
    unsigned int cuantos;
    cuantos = 0;
    if (visitados == NULL){
        return 0;
    } else {
        while (visitados != NULL){
            if (args->modo == 1){
                printf("Visitado: %d desde nodo %d\n", visitados->valor, args->nsimo_vertice);
            }
            cuantos = cuantos + 1;
            visitados = visitados->next;
        }
    }
    return cuantos;
}
void marcar(struct Node *visitados, unsigned int nsimo_vertice){//Las filas visitadas deben marcarse.
    while(visitados!=NULL){
        if(visitados->valor == nsimo_vertice){
            visitados->marca = 1;
        }
        visitados = visitados->next;
    }
}
unsigned int nsimo_elemento_no_marcado(struct Node *visitados){//retorna el primer nodo no marcado.
    while(visitados!=NULL){
        if(visitados->marca == 0){
            return visitados->valor;
        }
        visitados = visitados->next;
    }
    return 0;
}


void Alcanzar_nodos(struct ArgsDFS *args){ //Realiza la búsqueda desde un nodo inicial.
    int i2, tamanho_lista, fila;
    if(args->visitados==NULL){
        args->visitados = insertar(args->visitados, args->nsimo_vertice, 0); //Marca el nodo inicial
        fila = args->nsimo_vertice;
    }

    if (Bandera == 0) {
        while(todos_marcados(args->visitados)==0){//Se revisa la fila y se registran los caminos en visitados mientras hayan elementos en la lista sin marcar.
            for(i2 = 0; i2<args->q_columnas; i2 = i2 + 1){
                if(matriz[fila][i2]==1 && esta_en_la_lista(args->visitados, i2)==0 && i2!=fila){
                    insertar(args->visitados, i2, 0);
                }
            }
            marcar(args->visitados, fila);//se marca la fila para no volver a visitarla.
            fila = nsimo_elemento_no_marcado(args->visitados);//se selecciona la siguiente fila a visitar.
        }
    printf("Revision de nodos visitados desde el vertice %d\n",args->nsimo_vertice);
    //PrintList(args->visitados);
    tamanho_lista = completitud_visitas(args->visitados, args);//se revisa cuantos nodos logró visitar desde el nodo en cuestión, para así levantar la bandera.
    if(tamanho_lista!=args->q_columnas){
        Bandera = 1;
    }
    }
}

void *Process(void *arg){ //Función que coordina los hilos
    struct ArgsDFS *args;
    args = (struct ArgsDFS *)arg;
    unsigned int cantidad_revisados;
    cantidad_revisados = 0;
    while(cantidad_revisados<args->q_columnas && args->nsimo_vertice<args->q_columnas && Bandera == 0){//Mientras no se hayan revisado todos los nodos. Además, considera no traspasar el límite de vértices.
        if (args->modo == 1){ //Nodo se presenta.
            printf("\n\n**************************************\n\n");
            printf("From thread number %d - vertex %d is being checked\n\n",args->myid,args->nsimo_vertice);
        } 
        if(Bandera == 0){ //Ejecutamos la busqueda desde el vertice nsimo
            Alcanzar_nodos(args);
        }
        cantidad_revisados = cantidad_revisados + 1;
        args->nsimo_vertice = args->nsimo_vertice + args->hebras;//Actualizar el vértice a revisar.
        args->visitados = KillAll(args->visitados);//Limpiar la lista que lleva consigo los hilos para que no se mezclen los nodos visitados.
    }
}

void ReadData(int dim){//lectura de input.
    int i, j;

    matriz = calloc(dim, sizeof(unsigned int *));
    for (i = 0; i < dim; i = i + 1){
        matriz[i] = calloc(dim ,sizeof(unsigned int));
    }

    for (i = 0; i <dim; i = i + 1){
       for (j = 0; j <dim; j = j + 1){
            scanf("%d",&matriz[i][j]);
            if(j == dim-1){
            }
       }
    }   
}

int main(int argc, char **argv) {
    unsigned int i, dim, k;
    unsigned char modo;
    
    pthread_t *thread;
    pthread_attr_t attribute;
    struct ArgsDFS **args;
    void *exit_status; 

    //Inicialización de variables entregadas por consola
    if (strcmp(argv[3],"-S") == 0)
	    modo = 0;
    if (strcmp(argv[3],"-V") == 0)
        modo = 1;
    k = atoi(argv[1]);

    scanf("%d", &dim);
    ReadData(dim);//leer y guardar datos

    //--------------------------------------------Inicio de la paralelización--------------------------------------------//
    if(k>dim){//Asegurar de no ocupar más hilos que vértices.
        k = dim;
    }
    thread = calloc(k, sizeof(pthread_t));
    args = calloc(k, sizeof(struct ArgsDFS *)); 
    pthread_attr_init(&attribute);
    for (i = 0; i < k; i = i + 1) {
        args[i] = calloc(1, sizeof(struct ArgsDFS));
        args[i]->myid = i;  
        args[i]->nsimo_vertice = i; //Asigna un vertice inicial.
        args[i]->modo = modo;      //Entrega el modo de impresión
        args[i]->hebras = k;          //Entrega la cantidad de hebras a usar
        args[i]->q_columnas = dim;     //Entrega la dimension de la matriz 
        args[i]->visitados = NULL;   //Inicializa la lista de visitados la cual registra los nodos visitados.
        pthread_create(&thread[i], &attribute, Process, (void *)args[i]);
    }
    for (i = 0; i < k; i = i + 1) {
        pthread_join(thread[i], &exit_status); 
    }
    if(Bandera == 0){
        printf("El grafo es fuertemente conectado\n");
    }
    if(Bandera == 1){
        printf("Finalmente, el grafo no es fuertemente conectado\n");
    }
    for (i = 0; i < dim; i = i + 1) {
        free(matriz[i]);
    }
    free(matriz);
    free(args);
    free(thread);
    
    return 0;
}
