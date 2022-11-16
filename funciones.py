def lista_a_dict(lista:list):
    diccionario_bonito = dict()
    for diccionario in lista:
        diccionario_bonito[str(diccionario['idproductos'])]=diccionario
    return diccionario_bonito