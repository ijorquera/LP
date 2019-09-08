import re

"""
line_parser
——————–
Entradas:
Sin entradas. Se ocupa variables globales.
——————–
Salida:
(tuple) Output: tupla de 2 valores, primero corresponde a la llave de diccionario
de las expresiones regulares y el segundo a valor de rx.search
——————–
La función revisa si existe un match completo con el alguna expresión regular del
diccionario global SQL_REGEX.Si se encuentra un match, se retorna la llave de diccionario
y el valor de rx.search. En caso de que no se encuentra correspondencia entre el input
y alguna de las posibles expresiones regulares, se retorna una tupla (None,None).
"""
def line_parser():
    for key,rx in SQL_REGEX.items():
        match = rx.search(statement)
        if match:
            return key,match

"""
reviseReservedWords
——————–
Entradas:
(list) Una lista con strings que puede tener nombres de tablas, de columnas, etc.
——————–
Salida:
(int) Output: Se retorna un 0 o un 1 dependiendo del caso.
——————–
La función contiene un conjunto local reservedWords con las palabras reservadas.
Una vez recibida la lista compara los elementos de esta con los valores en el conjunto para ver
si la lista posee palabras reservadas como elementos. 
Si es asi, retorna un 0 (Caso de Error de Sintaxis). Si no, retorna 1.
"""
def reviseReservedWords(lista):
    reservedWords = {'INSERT','ASC','DESC','INTO','VALUES','SELECT','FROM','WHERE','ORDER BY','UPDATE','SET'}
    for string in lista:
        if string in reservedWords:
            return 0
    return 1

"""
checkColumns
——————–
Entradas:
(list) listaColumnasInput: lista con las columnas que ingreso el usuario en el query.
(list) listaColumnasArchivo: lista con las columnas que posee la tabla ingresada por el usuario en el query.
——————–
Salida:
(tuple) Output: Retorna una tupla con dos listas (listaPositiveMatch, listaNegativeMatch).
    (list) listaPositiveMatch: lista con las columnas ingresadas por el usuario que existen en la tabla.
    (list) listaNegativeMatch: lista con las columnas ingresadas por el usuario que no existen en la tabla.
——————–
La función guarda en una lista la intersección entre las columnas ingresadas por el usuario y las columnas existentes en la tabla.
Luego guarda en otra lista todas las columnas ingresadas que no pertenecen a la tabla.
"""
def checkColumns(listaColumnasInput, listaColumnasArchivo):
    listaPositiveMatch = [columna.strip() for columna in listaColumnasInput if columna in listaColumnasArchivo]
    listaNegativeMatch = [columna.strip() for columna in listaColumnasInput if columna not in listaColumnasArchivo]
    return (listaPositiveMatch, listaNegativeMatch)


"""
insert
——————–
Entradas:
(list) valid: lista con los grupos capturados por el match 
——————–
Salida: 
(void) No retorna
——————–
La función verifica que los valores ingresados cumplan las condiciones para poder así, finalmente, 
insertarlos en la tabla señalada por el usuario en el query.
"""
def insert(valid):
    # Descomprime los grupos ingresados, eliminano caracteres molestos al inicio y al final de cada valor.
    Tabla = valid[0].strip()

    # Ninguna Tabla o Columna capturada puede coincidir con palabras reservadas
    if (reviseReservedWords([Tabla]) == 0):
        print(); print('Error de Sintaxis !'); print()
        return 
    # Abre el archivo de la Tabla correspondiente en modo r+ (lectura + append).
    try:
        file = open(Tabla + ".csv", "r+", encoding='utf-8')
        Columnas = [name.strip() for name in re.split(r',', valid[1])]
        Values = [name.strip() for name in re.split(r',', valid[2])]

        # Si la cantidad de columnas es distinta a la cantidad de valores 
        # o si alguno de estos incluye palabras reservadas será error de sintaxis.
        if ((len(Columnas) != len(Values)) or (reviseReservedWords(Columnas) == 0)):
            print(); print("Error de Sintaxis !"); print()
            file.close()
            return
        
        # Lee la primera línea del archivo, elimina el salto de línea al final y separa el string
        # según las comas para obtener una lista con las Columnas del archivo.
        columnasFile = file.readline().strip().split(",")

        # Se reasigna la lista de columnas para que guarde solo las columnas ingresadas que existen en el archivo.
        # Adicionalmente se hace una variable que almacene las columnas ingresadas que no existen en el archivo.
        Columnas, colNotFound = checkColumns(Columnas, columnasFile)

        # Si se ingresan columnas que no existen en la tabla será error de sintaxis.
        if (len(colNotFound) != 0):
            print(); print("Error de Sintaxis !, las columnas "+ ", ".join(colNotFound) + " no pertenecen a la tabla."); print()
            return
        
        # Diccionario donde valor = columnas de la tabla y llave = indice de la columna en la tabla
        indices = { Columna : columnasFile.index(Columna) for Columna in columnasFile}
        
        # Lista con la nueva fila que se insertará en la tabla.
        output = ["" for columna in columnasFile] # Se rellena con strings vacíos para darle el largo que debe tener una fila en la tabla ingresada.
        # Se rellena Output con los valores en el indice correspondiente
        for i in range(len(Columnas)):
            output[indices[Columnas[i]]] = Values[i].strip("'")
        
        # Agrega el output al archivo csv separando cada valor con una coma.
        file.write(",".join(output)+"\n")
        print(); print("Se ha insertado 1 fila."); print()
        file.close()

    except FileNotFoundError:
        print(); print('Tabla indicada no existe. Intente de nuevo.'); print()
        return

"""
update
——————–
Entradas:
(list) valid: lista con los grupos capturados por el match 
——————–
Salida: 
(void) No retorna
——————–
La función verifica que los valores ingresados cumplan las condiciones para poder así, finalmente, 
actualizar la tabla señalada por el usuario en el query con los valores ingresados.
"""
def update(valid):
    # Descomprime el nombre de la tabla ingresada.
    Tabla = valid[0].strip()
    
    # Ninguna Fila o Columna capturada puede coincidir con palabras reservadas
    if (reviseReservedWords([Tabla]) == 0):
        print(); print('Error de Sintaxis 136!'); print()
        return 

    try:# Abre el archivo de la Tabla correspondiente en modo r (lectura).
        fileTable = open(Tabla + ".csv", "r", encoding='utf-8')
        
        # Descomprime los cambios ingresados en SET, separándolos en una lista por comas (",") y después en otra por igual ("=").
        Set = [name.strip().split("=") for name in re.split(r',', valid[1])] 
        
        # Guarda las lineas del archivo en una lista de lista, donde cada lista interna es una fila.
        lineas = fileTable.readlines()
        cont = 0
        while(cont < len(lineas)):
            lineas[cont] = lineas[cont].strip().split(",") # Separa las filas usando la coma (",") para generar las columnas
            cont += 1
        fileTable.close()
            
        columnasFile = lineas[0] # Guarda las columnas que tiene la tabla.
        ColumnasSet = [Set[i][0].strip() for i in range(len(Set))] # Guarda las columnas que ingresó el usuario en SET.
        # Asigna una lista con las columnas que ingresó el usuario en SET que existen en la tabla
        # y una lista con las columnas que ingresó el usuario que no existen en la tabla.
        ColumnasSet , colNotFound = checkColumns(ColumnasSet ,columnasFile)
        
        # Si se ingresan columnas que no existen en la tabla o si las columnas en set incluyen 
        # palabras reservadas se imprimirá error de sintaxis y saldrá de la función
        if ((len(colNotFound) != 0) or (reviseReservedWords(ColumnasSet) == 0)):
            print(); print("Error de Sintaxis ! 163"); print()
            return
        
        # Descomprime las condiciones ingresadas en WHERE, separándolas por OR y luego por AND, manteniendo así la precedencia del segundo.
        Where = [name.strip().split("AND") for name in re.split(r'OR', valid[2])]

        # Separa las listas internas de WHERE haciendo split con el signo igual ("=") y revisa que la columna se encuentre en la tabla.
        # De no estar la columna en la tabla se imprimirá "Error de Sintaxis !" por consola.
        # Where quedará como se muestra en la siguiente línea:
        # Where = [[[columna1, cosa1]], [[columna2, cosa2], [columna3, cosa3]]], siendo los elementos en Where[i] las listas de condiciones
        # separadas por un OR, los elementos en Where[i][j] las condiciones separadas por un AND y los elementos en Where[i][j][k] 
        # las columnas con el valor que se desea buscar.
        i = 0
        while(i < len(Where)):
            j = 0

            while (j < len(Where[i])):
                col, value = Where[i][j].split("=")
                col = col.strip() # col puede ser de la forma Columna o de la forma Tabla.Columna
                value = value.strip().strip("'")
                Where[i][j] = [col, value]
                j = j + 1
            ColumnasWhere = [condicion[0] for condicion in Where[i]]
            # Asigna una lista con las columnas que ingresó el usuario en WHERE que existen en la tabla
            # y una lista con las columnas que ingresó el usuario que no existen en la tabla.
            ColumnasWhere , colNotFound = checkColumns(ColumnasWhere ,columnasFile)
            if((reviseReservedWords(ColumnasWhere) == 0) or (len(colNotFound) != 0)):
                print('Error de Sintaxis! (columnas de where)')
                return
            i = i + 1

        # # Diccionario donde valor = columnas de la tabla y llave = indice de la columna en la tabla
        # indices = { Columna : columnasFile.index(Columna) for Columna in columnasFile}
        # print(indices)

        # Ya no quedan más casos de error, ahora hay que verificar si se cumple alguna condición para modificar los datos de la tabla.
        indicesOutput = set() # Almacena los indices de las filas a modificar.
        for condiciones in Where:
            matchCondiciones = set() # Conjunto para realizar intersección entre condiciones unidas por AND
            for i in range(len(condiciones)):
                j = 1
                filas = set()
                cont = 0
                while (j < len(lineas)):
                    if (condiciones[i][1] == lineas[j][columnasFile.index(condiciones[i][0])]): # Si valor en set = valor en tabla
                        filas.add(j) # Agrega el indice de la fila que cumple la condición ingresada
                    j = j + 1
                if (i == 0):
                    matchCondiciones = matchCondiciones.union(filas) # Si es la primera iteración se le asigna el mismo valor para que no se anule
                matchCondiciones = matchCondiciones.intersection(filas) # Intersección entre conjunto filas y matchCondiciones
            indicesOutput = indicesOutput.union(matchCondiciones) # Unión entre conjuntos separados por OR 
        if (len(indicesOutput) == 0):
            print ("No se pudo actualizar la información con la información entregada.")
            return

        # Modificación de las filas de la tabla:
        for indice in indicesOutput:
            for col, val in Set:
                lineas[indice][columnasFile.index(col.strip())] = val.strip().strip("'")
        
        # Actualización de la tabla en el archivo css
        file = open(Tabla + ".csv", "w", encoding='utf-8')
        for linea in lineas:
            file.write(",".join(linea)+"\n")
        file.close()
        print("Se ha actualizado " + str(len(indicesOutput)) + " fila")
        
        # UPDATE Notas SET Nota = -10 WHERE Nombre = 'ore ' OR Nombre = 'ore sama' OR Nombre = 'Clemente Aguilar'  AND Rol = '201773580-3' OR Rol = '201673557-4';

        return
    except FileNotFoundError:
        print(); print('Tabla indicada no existe. Intente de nuevo.'); print()
        return

def select(valid):

    Tablas = [] # [ tabla 1, tabla 2], Tablas puede tener largo 1 o 2, dependiendo si se incluye INNER JOIN
    Tablas.append(valid[1].strip()) # Tablas = [tabla 1], agrega la primera tabla a Tablas
       # Ingresos opcionales:
    if(valid[2] != None): # Pregunta si se incluye el comando INNER JOIN
        Tablas.append(valid[2].strip().strip("'")) # Tablas = [tabla 1, tabla 2], agrega tabla 2 a Tablas
    # Ninguna tabla capturada puede coincidir con palabras reservadas
    if (reviseReservedWords(Tablas) == 0):
        print(); print('Error de Sintaxis 257!'); print()
        return 
    
    try:
        archivos = dict()
        for tabla in Tablas:
            fileTable = open(tabla + ".csv", "r", encoding='utf-8') # Abre el archivo de la Tabla correspondiente en modo r (lectura).
            lineas = fileTable.readlines() # Guarda las lineas del archivo en una lista de lista, donde cada lista interna es una fila.
            cont = 0
            while(cont < len(lineas)):
                lineas[cont] = lineas[cont].strip().split(",") # Separa las filas usando la coma (",") para generar las columnas
                cont += 1
            archivos[tabla] = lineas # Agrega el archivo separado en filas y columnas al diccionario con llave = nombre tabla
            fileTable.close()
       
        colTablas = archivos[Tablas[0]][0] # Lista que guarda todas las columnas de las tablas ingresadas (sin repetir) para futuras comparaciones.
        if(len(Tablas) > 1):
            colTablas = colTablas + [columna for columna in archivos[Tablas[1]][0] if columna not in colTablas]

        Select = [name.strip() for name in re.split(r',', valid[0])] # Desempaqueta las columnas ingresadas en el query [[Columna1] , [columna2]]

        if (Select == "*"): # Si se ingresó * en select, este tomará todas las columnas de las tablas ingresadas.
            Select = colTablas.copy()

        # Check de WHERE
        if(valid[3] != None ): # Revisa si el usuario ingreso WHERE en su input para desempaquetar sus datos
            Where = [name.split("AND") for name in re.split(r'OR', valid[3])] # [[cond11 = value11 , cond12 = value12], [cond21 = val21]] [[And, And] OR [And]], OR = ","
        else:
            Where = [] # Se deja como lista vacia dado que no fue ingresado   
        
        # Check de ORDER BY
        if(valid[4] != None ): # Revisa si el usuario ingreso ORDER BY en su input para esempaquetar sus datos
            Order = valid[4].strip() # Columna que se quiere usar para ordenar los datos mostrados en pantalla
            By = valid[5].strip() # ASC | DESC
        else:
            Order = [] # Se deja como lista vacia dado que no fue ingresado
            By = "" # Se deja como string vacio dado que no fue ingresado
        
        columnasSelectOrder = Select + Order # Lista que almacenará todas las columnas ingresadas en SELECT y ORDER BY para ver si existen en las tablas
        if (reviseReservedWords(columnasSelectOrder) == 0):
            print('\nError de Sintaxis ! linea 303\n')
            return
        
        columnasSelectOrder, colNotFound = checkColumns(columnasSelectOrder, colTablas)
        if (len(colNotFound) != 0):
            print('\nError de Sintaxis ! linea 308\n')
            return
        
        Output = [] # Lista que almacena las OutputFila que cumplan las condiciones solicitadas
        
        if (len(Where) != 0): # Si se ingresa WHERE           
            # Separa las condiciones del WHERE haciendo split en el signo =
            for cont in range(len(Where)): # Condiciones separadas por OR
                        
                OutputMatch = [] # Almacena las filas que cumplen las condiciones señaladas
                blend = [] # Guarda la o las columnas que se deben unir para juntar tablas
                for cont2 in range(len(Where[cont])): # Condiciones separadas por AND
                    matchRow = [] # Lista que almacena la fila con los elementos solicitados
                    Where[cont][cont2] = Where[cont][cont2].split("=")
                    Where[cont][cont2][0] = Where[cont][cont2][0].strip().split(".") # Si es de la forma tabla.columna tendrá largo 2, else largo 1
                    Where[cont][cont2][1] = Where[cont][cont2][1].strip().split(".")
                    # Where[cont][cont2][0] -> lado izquierdo de la igualdad
                    # Where[cont][cont2][1] -> lado derecho de la igualdad
                    # Si el usuario ingresa INNER JOIN 
                    if(len(Tablas) == 2):
                        if(len(Where[cont][cont2][0]) == 1): # Si la parte izquierda de la igualdad de alguna condición no es de la forma tabla.columna -> error sintaxis
                            print("\nError de Sintaxis ! linea 323\n")
                            return
                        tabla1 = Where[cont][cont2][0][0]
                        col1 = Where[cont][cont2][0][1]
                        if (reviseReservedWords([tabla1]+[col1]) == 0 or tabla1 not in Tablas or col1 not in colTablas):
                            print('\nError de Sintaxis ! linea 328\n')
                            return
                        indice1 = archivos[tabla1][0].index(col1)
                        
                        if(len(Where[cont][cont2][1]) == 2): # Si la parte derecha de la igualdad es de la forma tabla.columna
                            tabla2 = Where[cont][cont2][1][0] # tabla ingresada en la parte derecha de la igualdad
                            col2 = Where[cont][cont2][1][1] # columna ingresada en la parte derecha de la igualdad
                            if(tabla1 != tabla2 and col1 == col2): # si tabla1.Columna = tabla2.Columna, columnas iguales
                                blend.append(col1) # agrega la columna a la lista blend TODO es posible que remueva esa lista completamente

                            if (reviseReservedWords([tabla2]+[col2]) == 0 or tabla2 not in Tablas or col2 not in colTablas):
                                print('\nError de Sintaxis ! linea 339\n')
                                return

                            indice2 = archivos[tabla2][0].index(col2) # Indice de la columna ingresada en la parte derecha en su respectiva tabla

                            for fila1 in range(1, len(archivos[tabla1])): # Empieza a buscar las filas que cumplan la condición ingresada
                                for fila2 in range(1, len(archivos[tabla2])):
                                    if (archivos[tabla1][fila1][indice1] == archivos[tabla2][fila2][indice2]):
                                        matchRow.append((archivos[tabla1][fila1], archivos[tabla2][fila2]))

                        else: # Si la parte derecha tiene largo = 1 y es de la forma value
                            # Código para tabla.columna = valor
                            val = Where[cont][cont2][1][0]
                            # Si val no es un número ni un 'string' ni un número negativo -> error
                            if(val.isnumeric() or (val[0] == "'" and val[-1] == "'" and len(val) > 2) or (val[0] == "-" and val.count("-") == 1 and val.strip("-").isnumeric())):
                                for fila in range(1, len(archivos[tabla1])): # Itera por cada fila de la tabla 1
                                    if(archivos[tabla1][fila][indice1] == val): # Encuentra una fila-columna que tiene el mismo valor que value
                                        item1 = archivos[tabla1][fila] # Guarda la fila completa en una variable
                                        for key in archivos.keys():
                                            if (key != tabla1): # Empieza a hacer matching con cada uno de los elementos de la otra tabla
                                                for fila2 in range(1, len(archivos[key])): # Al no tener restricción en la segunda tabla, toma todas sus filas
                                                    item2 = archivos[key][fila2]
                                                    matchRow.append((item1, item2))
                            else:
                                print('\nError de Sintaxis ! linea 363\n')
                                return

                    else: # Sin INNER JOIN
                        if(len(Where[cont][cont2][1]) > 1 or len(Where[cont][cont2][0]) > 1): # Si el lado izquierdo o el derecho incluye punto (.)
                            print("\nError de Sintaxis !\n") # Al no haber inner join debe ser de la forma Columna = valor, sin puntos
                            return
                    
                        col1 = Where[cont][cont2][0][0]
                        val = Where[cont][cont2][1][0]

                        if (reviseReservedWords([col1]) == 0 or col1 not in colTablas):
                            print('\nError de Sintaxis ! linea 332\n')
                            return
                        indice1 = archivos[tabla1][0].index(col1)
                        # Columna = Valor
                        if(val.isnumeric() or (val[0] == "'" and val[-1] == "'" and len(val) > 2) or (val[0] == "-" and val.count("-") == 1 and val.strip("-").isnumeric())):
                            for fila in range(1,len(archivos[Tablas[0]])): # Revisa todas las filas de la tabla ingresada
                                if(archivos[Tablas[0]][fila][indice1] == val): # Si la columna de la fila = valor ingresado, lo guarda en la lista
                                    matchRow.append(archivos[Tablas[0]][fila])

                        else: # Columna = Columna   
                            if (reviseReservedWords([val]) == 0 or val not in colTablas):
                                print('\nError de Sintaxis ! linea 332\n')
                                return
                            indice2 = archivos[tabla1][0].index(val)
                            for fila in range(1,len(archivos[Tablas[0]])): # Revisa todas las filas de la tabla ingresada
                                if(archivos[Tablas[0]][fila][indice1] == archivos[Tablas[0]][fila][indice2]): # Si valor de columna1 = valor columna 2, guarda la fila en la lista
                                    matchRow.append(archivos[Tablas[0]][fila])

                    if(cont2 == 0):
                        OutputMatch = matchRow.copy() # Si es la primera iteración, OutputMatch toma el mismo valor que matchRow
                    else: 
                        OutputMatch = [value for value in matchRow if value in OutputMatch] # Intersecta las condiciones separadas por un AND  
                # Une las condiciones separadas por un OR
                for filas in OutputMatch:
                    if filas not in Output:
                        Output.append(filas)
            
        else: # Si no se ingresa WHERE
            for fila in range(1, len(archivos[Tablas[0]]))
            while(fila < len(tabla)): # Si no hay WHERE, guarda todas las filas de la tabla ingresada
                Output.append(archivos[Tablas[0]][fila])

        if(len(Output) >0): # Si hay al menos una fila que cumpla las condiciones ingresadas
            # Código para ORDER BY 
            if(len(Order) > 0): # Si se ingresa ORDER BY
                if (reviseReservedWords([Order]) == 0 or Order not in colTablas):
                    print('\nError de Sintaxis ! linea 411\n')
                    return
                if(len(Tablas) == 1): # Sin INNER JOIN
                    # TODO Revisar de aqui para abajo
                    indice = Select_dict[Order][Tablas[0]]
                    if(indice != -1):
                        OutputMatch.sort(key=lambda x: x[indice])# Función Lambda,
                        # permite aplicar sort usando un indice en particular como pivote.
                        if (By.strip() == "DESC"): # Si pide desceniente basta con invertir la lista.
                            OutputMatch.reverse()
                    else:
                        print("La columna que ingresó después del comando ORDER BY no existe en la tabla.")
                else: # Considerando inner join
                    indice = -1
                    i = 0
                    while (i < len(Tablas)):
                        if (Order in archivos[Tablas[i]][0]):
                            indice = archivos[Tablas[i]][0].index(Order)
                            tabla = i
                        i = i + 1
                    if (indice == -1):
                        print("La columna que ingresó después del comando ORDER BY no existe en las tablas.")
                    else:
                        OutputMatch.sort(key=lambda x: x[tabla][indice])# Función Lambda,
                        # permite aplicar sort usando un indice en particular como pivote.
                        if (By.strip() == "DESC"): # Si pide desceniente basta con invertir la lista.
                            OutputMatch.reverse()
                    
                    


                        # Nueva forma de Where: [[[cond11,value11], [cond12, value12]], [[cond21, val21]]]

        else:
            print("La información solicitada no existe")


    except FileNotFoundError:
        print(" ERROR DE SINTAXIS EXCEPT Linea 368")
        return


# Main loop
while(True):
    #recepcion de input

    print ("Ingrese su query:")
    statement = input()
    #condicion de salida de loop infinito
    if(statement == 'EXIT'):
        print()
        print('Se recibió comando de salida.Terminando la ejecución.')
        print()
        break
    #un diccionario con posibles llaves de expresiones completas
    SQL_REGEX = {
    'UPDATE_Key' : re.compile(r'^UPDATE\s+([^\s;,]+)\s+SET\s+((?:[^\s\.\'=*,;]+\s*=(?:\s*\'\s*[^\']+\s*\'|\s*-?\d+(?:\.\d+)?)(?:\s*,\s*[^\s\.\'=*,;]+\s*=(?:\s*\'\s*[^\']+\s*\'|\s*-?\d+(?:\.\d+)?))*))\s+WHERE\s+((?:[^\s\.\'=*,;]+\s*=(?:\s*\'\s*[^\']+\s*\'|\s*-?\d+(?:\.\d+)?)(?:\s*(?:AND|OR)\s*[^\s\.\'=*,;]+\s*=(?:\s*\'\s*[^\']+\s*\'|\s*-?\d+(?:\.\d+)?))*));{1}$'),
    'SELECT_Key' : re.compile(r'^SELECT\s+((?:\s*[^\s,;=\']+)(?:(?:\s*,\s*[^\s,*=;\']+)*))\s+FROM\s+([^\s;,]+)(?:(?:\s+INNER\sJOIN\s+([^\s;]+))?(?:(?:\s+WHERE\s+((?:[^\s.\'=*,;]+(?:.[^\s.\'=*,;]+)?\s*=(?:(?:\s*\'\s*[^\']+\s*\'|\s*-?\d+(?:.\d+)|\s*[^\s.\'=*;,]+(?:.[^\s.\'=*,;]+)?))(?:(?:\s+(?:AND|OR)\s+[^\s.\'=,;*]+(?:.[^\s.\'=,*;]+)?\s*=(?:(?:\s*\'\s*[^\']+\s*\'|\s*-?\d+(?:.\d+)|\s*[^\s.\'=,;*]+(?:\.[^\s.\'=;,*]+)?)))*)?)))))?(?:\s+ORDER\sBY\s+([^*\s=\';,]+)\s+(ASC|DESC))?;{1}$'),
    'INSERT_Key':re.compile(r'^INSERT\sINTO\s+([^\s,]+)\s+\(\s*((?:\s*[^\s,=*\';]+)(?:(?:\s*,\s*[^\s,=*\';]+\s*)*))\)\s+VALUES\s+\(((?:\s*\'[^\']+\s*\'\s*|\s*-?\d+|(?:\.\d+))(?:(?:,\s*\'\s*[^\']+\s*\'\s*|\s*,\s*-?\d+|(?:\.\d+)\s*)*))\);{1}$'),
    }
    #tupla key-match
    result_tuple = line_parser()
    #isinstance verifica que la llave no es null para no generar error de
    #noneType error.
    if isinstance(result_tuple,type(None)):
        #si la llave o match son None,no había match. Es decir, fallo la sintaxis.
        print()
        print('Error de Sintaxis! 396')
        print()
        
    else:
        key = result_tuple[0]
        if key == 'UPDATE_Key':
            update(SQL_REGEX['UPDATE_Key'].match(statement).groups())
        elif key == 'SELECT_Key':
            select(SQL_REGEX['SELECT_Key'].match(statement).groups())
        elif key == 'INSERT_Key':
            insert(SQL_REGEX['INSERT_Key'].match(statement).groups())