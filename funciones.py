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