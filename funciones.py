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

def limpiar_string(cuerda:str) -> str:
    remplazador='abcdefghijklmnñopqrstuvwxyz}{][ ,)(\'\"'
    for remplazado in remplazador:
        cuerda.replace(remplazado,'')
        print(cuerda)
    return cuerda
