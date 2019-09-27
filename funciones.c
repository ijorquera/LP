#include "lista.c"
#include "funciones.h"

//Se aplica una operacion *f a cada nodo de la lista y se retorna
//Un puntero a la lista nueva. Problema: init debe ser con **lista
//Si no, el usuario debe hacer malloc y free de su lista, y eso es estupido
//En espera de respuesta de pantuflin
struct lista* map(struct lista *a, struct dato (*f)(struct dato)){
    struct lista *b=(struct lista*)malloc(sizeof(struct lista));
    struct lista *c;
    init(b);
    if(length(a)==0){
        return b;
    }
    struct dato disp;
    struct dato aux;
    int pos;
    for(pos=0; pos<length(a); pos++){
        disp=*at(a, pos);
        aux.tipo=disp.tipo;
        if(aux.tipo=='l'){
            aux.contenido=(void*)malloc(sizeof(struct lista));
            c = map((struct lista*)disp.contenido, (*f));
            *(struct lista*)aux.contenido = *c;
            clear(c);
            free(c);
            append(b, aux);
        }
        else{
            if(aux.tipo=='i'){
                aux.contenido=(void *)malloc(sizeof(int));
                *(int*)aux.contenido=*(int*)disp.contenido;
            }
            else{ // if(aux.tipo=='f')
                aux.contenido=(void *)malloc(sizeof(float));
                *(float*)aux.contenido=*(float*)disp.contenido;
            }
            append(b, (*f)(aux));
        }
    }
    return b;
}

//Suma total de elementos de lista. En caso de lista vacia, retorna 0.
float sum(struct lista *a){
    float suma=0;
    if (length(a)==0){
        return suma;
    }
    struct dato disp;
    int pos;
    for(pos=0; pos<length(a); pos++){
        //*at retorna puntero al elemento en posicion.
        disp = *at(a, pos);
        if(disp.tipo=='i'){
            //dereferencia el (int*)
            suma+=*(int*)disp.contenido;
        }
        else if(disp.tipo=='f'){
            //dereferencia el (float*)
            suma+=*(float*)disp.contenido;
        }
        else{ // disp.tip == 'l'
            //suma recursivamente
            suma+=sum((struct lista*)disp.contenido);
        }
    }
    return suma;
}

void print(struct lista *a){
    //para lista normal imprimira al funcionar algo como  [1, 2.5, 0]
    //para incrustadas algo como [1, 2, [9, 0.9], 9.99]
    struct dato *disp;
    printf("[");
    if (length(a)!=0){
        int pos;
        for (pos=0; pos<length(a); pos++){
            //dereferencia el struct en posicion pos
            disp=at(a, pos);
            if(disp->tipo=='i'){
                printf("%d", *(int*)disp->contenido);
            }
            else if(disp->tipo=='f'){
                printf("%f", *(float*)disp->contenido);
            }
            else{ // disp->tipo=='l'
                print((struct lista*)disp->contenido);
            }
            if(length(a)!=1 && pos!=length(a)-1){ // TODO probar sin primera condicion
                printf(", ");
            }
        }
    }
    printf("]");
    return;
}

float average(struct lista *a){
    float suma=0;
    if (length(a)==0){
        return suma;
    }
    int cantElem=length(a);
    struct dato disp;
    int pos;
    for (pos=0; pos<length(a); pos++){
        disp=*at(a, pos);
        if(disp.tipo!='l'){
            if(disp.tipo=='i'){
                suma+=*(int*)disp.contenido;
            }
            else{
                suma+=*(float*)disp.contenido;
            }
        }
        else{
            if(!length((struct lista*)disp.contenido)){
                //length es 0, no se considerara la lista vacia.
                cantElem--;
            }
            else{
                suma+=average((struct lista*)disp.contenido);
            }
        }
    }
    return suma/cantElem;
}


// Boorraaaaar.

struct dato triplicado(struct dato data){
    if(data.tipo=='i'){
        *(int *)data.contenido = *(int *)data.contenido * 3;
    }
    if(data.tipo=='f'){
        *(float *)data.contenido = *(float *)data.contenido * 3;
    }
    return data;
}

struct dato halved(struct dato data){
    if(data.tipo=='i'){
        *(int *)data.contenido=*(int *)data.contenido/2;
    }
    if(data.tipo=='f'){
        *(float *)data.contenido=*(float *)data.contenido/2;
    }
    return data;
}




void interface(struct lista *l){
    int conf=999;
    int pos;
    int func=0;
    struct dato *display;
    struct dato data;
    struct lista *mapeada;
    while(conf!=0){
        printf("\nEl largo de la lista es %d\nLa lista actual es la siguiente:\n", length(l));
        print(l);
        printf("\nIngrese el número de la operacion que desea realizar:\n");
        printf("-----------------------------------------------------\n");
        printf("1: Insertar un elemento en una posición específica.\n");
        printf("2: Remover un elemento en una posición específica.\n3: Obtener el dato de una posición en específica de la lista.\n");
        printf("4: Imprimir por pantalla la lista modificada por map.\n5: Obtener la suma de todos los elementos de la lista.\n");
        printf("6: Imprimir por pantalla la lista.\n7: Obtener el promedio de todos los elementos de la lista.\n");
        printf("8: Vaciar la lista.\n9: ingresar a una lista.\n");
        printf("0: Fin del programa.\n");
        printf("-----------------------------------------------------\n");
        scanf("%d", &conf);
        if(conf==1){
            printf("Ingrese el tipo de dato que desea ingresar (i de int, f de float, l de lista): ");
            scanf(" %c", &data.tipo);
            if(data.tipo=='i'){
                data.contenido=(int*)malloc(sizeof(int));
                data.contenido=(int*)data.contenido;
                printf("Ingrese el int que desea agregar a la lista: ");
                scanf("%d", (int*)data.contenido);
            }
            else if(data.tipo=='f'){
                data.contenido=(float*)malloc(sizeof(float));
                printf("Ingrese el float que desea agregar a la lista: ");
                scanf("%f", (float*)data.contenido);
            }
            else if(data.tipo=='l'){
                data.contenido=(struct lista*)malloc(sizeof(struct lista));
                init((struct lista*)data.contenido);
            }
            else{
                printf("El tipo de dato no es valido.");
                free(data.contenido);
                continue;
            }
            printf("Ingrese la posicion en donde desea insertar el nuevo elemento: " );
            scanf("%d", &pos);
            insert(l, pos, data);
            // printf("El largo actual es: %d\n", length(l));
            // print(l);
            printf("\n");
        }
        else if(conf==2){
            printf("Ingrese la posicion en donde desea remover el elemento: ");
            scanf("%d", &pos);
            remov(l,pos);
        }
        else if(conf == 3){
            printf("Ingrese la posicion de elemento que desea obtener: ");
            scanf("%d", &pos);
            display = at(l,pos);
            if(display == NULL){
                printf("La lista esta vacia, no se puede acceder a un elemento.");
                continue;
            }
            if(display->tipo != 'l'){
                if(display->tipo == 'i'){
                    printf("El elemento en posicion %d es un entero y su valor es: %d",pos, *(int*)display->contenido);
                }
                else{
                    printf("El elemento en posicion %d es un flotante y su valor es: %f",pos,*(float*)display->contenido);
                }
            }
            else{
                printf("El elementi en posicion %d es una lista y sus elementos son: ",pos);
                print((struct lista*)display->contenido);
            }

        }
        else if (conf == 4){
            printf("Aqui va el map");
            mapeada = NULL;
            printf("\n1-) Función triplicado.\n2-) Función halved.\nIngrese el número de la función que desea utilizar: ");
            scanf("%d", &func);
            if(func == 1){
                mapeada = map(l, (*triplicado));
            }
            if(func == 2){
                mapeada = map(l, (*halved));
            }
            if(mapeada!=NULL){
                print(mapeada);
                clear(mapeada);
                free(mapeada);
            }
        }
        else if (conf == 5){
            printf("La suma de todos los elementos de la lista (incluyendo los elementos de listas internas) es: %f", sum(l));    
        }
        else if (conf == 6){
            printf("La lista contiene los siguientes elementos:\n");
            print(l);
        }
        else if (conf == 7){
            printf("El promedio de todos los elementos de la lista (incluyendo los elementos de listas internas) es: %f", average(l));
        }
        else if (conf == 8){
            clear(l);
            printf("La lista actual es:\n");
            print(l);
            printf("\n");
        }
        else if (conf == 9){
            printf("Ingrese la posicion de la lista a que quiere ingresar: ");
            scanf("%d", &pos);
            if(at(l, pos)->tipo == 'l'){
                interface(at(l, pos)->contenido);
            }
            else{
                printf("La posición elegida no contiene una lista.");
            }
        }

    }
}

int main(){
    struct lista *lista=(struct lista*)malloc(sizeof(struct lista));
    init(lista);
    interface(lista);
    clear(lista);
    free(lista);
    return 0;
}