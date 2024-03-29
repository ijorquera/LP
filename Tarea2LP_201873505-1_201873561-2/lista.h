struct dato{
  void* contenido;
  char tipo;
};

struct nodo{
  struct dato info;
  struct nodo* next;
};

struct lista{
  struct nodo* actual;
  struct nodo* head;
  struct nodo* tail;
  int length;
};

void init(struct lista *a);
void clear(struct lista *a);
void insert(struct lista *a,int i,struct dato d);
void append(struct lista *a, struct dato d);
void remov(struct lista *a,int i);
int length(struct lista *a);
struct dato* at(struct lista *a,int i);

char getTipo(struct dato dato);
void* getContenido(struct dato dato);
struct dato makeDato(void* contenido, char tipo);
