#include <stdio.h>
#include "lista.h"


void init(struct lista *a){
  struct lista *a = (struct lista*)malloc(sizeof(struct lista));
  a->actual = NULL;
  a->head = NULL;
  a->length = 0;
  a->tail = NULL;
  return;
}

//no soporta listas incrustadas todavia.
void clear(struct lista *a){
  struct nodo *loop_aux_next;
  a->actual = a->head;
  while(a->head != NULL){
    loop_aux_next = a->head;
    a->head = a->head->next;
    free(loop_aux_next);
  }
  a->length = 0;
  a->actual = NULL;
  a->tail = NULL;
  return;
}

void insert(struct lista *a, int i, dato d){
  return;
}

void remove(struct lista *a, int i){
  return;
}

int length(struct lista *a){
  return a->length;
}

dato* at(struct lista *a, int i){
  return;
}
