
def lista_a_dict(lista:list,llave:str):
    diccionario_bonito = dict()
    for diccionario in lista:
        diccionario_bonito[str(diccionario[llave])]=diccionario
    return diccionario_bonito


def actualizar_diccionario(cursor_dict,tabla:str,llave:str):
    query=f'SELECT * FROM {tabla};'
    cursor_dict.execute(query)
    productos=cursor_dict.fetchall()
    productos_dict=lista_a_dict(productos,llave)
    return productos_dict

def organizar_lista(cursor_dict,query,llave):
    cursor_dict.execute(query)
    lista_desorganizada =  cursor_dict.fetchall()
    lista_organizada = []
    for elemento in lista_desorganizada:
        lista_organizada.append(elemento[llave])
    return lista_organizada
def sumar_cantidad(lista_precio:list,lista_cantidad:list)-> float:
    sumado=0.0
    i=0
    for x in lista_precio:
        sumado=sumado+(x*lista_cantidad[i])
        i=i+1
    return sumado
