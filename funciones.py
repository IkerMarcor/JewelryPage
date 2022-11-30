
class orden:
    idpedido: int
    idproductos: list
    idgeneral: list
    cantidad: list
    nombre: list
    precio:list
    imagen: list
    direccion: str
    def __init__(self, idpedido:int, idproductos:list,idgeneral:list,cantidad:list,nombre:list,precio:list,imagen:list, direccion:str):
        self.idpedido=idpedido
        self.idproductos=idproductos
        self.idgeneral=idgeneral
        self.cantidad=cantidad
        self.nombre=nombre
        self.precio=precio
        self.imagen=imagen
        self.direccion=direccion


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

def listar_ordenes(cursor_dict,id_usuario)->list:
    lista_ordenes=[]
    query=f'SELECT idpedidos FROM pedidos WHERE idusuario={id_usuario} GROUP BY idpedidos'
    cursor_dict.execute(query)
    ordenes=cursor_dict.fetchall()
    for ordenal in ordenes:
        query=f'SELECT idproductos FROM pedidos WHERE idusuario={id_usuario} AND idpedidos= {str(ordenal["idpedidos"])}'
        cursor_dict.execute(query)
        ordenes_idproductos=cursor_dict.fetchall().copy()
        lista_idproductos=[]
        for idproducto in ordenes_idproductos:
            lista_idproductos.append(idproducto['idproductos'])
        query=f'SELECT id_producto_general from pedidos INNER JOIN  producto_especifico as pg on pg.id_producto_especifico=idproductos WHERE idpedidos= {str(ordenal["idpedidos"])}'
        cursor_dict.execute(query)
        ordenes_idgeneral=cursor_dict.fetchall().copy()
        lista_idgeneral=[]
        for idproducto in ordenes_idgeneral:
            lista_idgeneral.append(idproducto['id_producto_general'])
        query=f'SELECT cantidad FROM pedidos WHERE idusuario={id_usuario} AND idpedidos= {str(ordenal["idpedidos"])}'
        cursor_dict.execute(query)
        ordenes_cantidad=cursor_dict.fetchall().copy()
        lista_cantidad=[]
        for cantidad in ordenes_cantidad:
            lista_cantidad.append(cantidad['cantidad'])
        lista_cantidad=[int(x) for x in lista_cantidad]
        query=f'SELECT nombre from pedidos INNER JOIN  producto_especifico as pg on pg.id_producto_especifico=idproductos WHERE idusuario={id_usuario} AND idpedidos= {str(ordenal["idpedidos"])}'
        cursor_dict.execute(query)
        ordenes_nombre_producto=cursor_dict.fetchall().copy()
        lista_nombre=[]
        for nombre in ordenes_nombre_producto:
            lista_nombre.append(nombre['nombre'])
        query=f'SELECT pg.precio from pedidos INNER JOIN  producto_especifico as pg on pg.id_producto_especifico=idproductos WHERE idusuario={id_usuario} AND idpedidos= {str(ordenal["idpedidos"])}'
        cursor_dict.execute(query)
        ordenes_nombre_producto=cursor_dict.fetchall().copy()
        lista_precio=[]
        for nombre in ordenes_nombre_producto:
            lista_precio.append(nombre['precio'])
        lista_precio=[float(x) for x in lista_precio]
        query=f'SELECT imagen from pedidos INNER JOIN  producto_especifico as pg on pg.id_producto_especifico=idproductos INNER JOIN imagenes_especificas AS ie on pg.id_producto_especifico=ie.id_producto_especifico WHERE idusuario={id_usuario} AND idpedidos={str(ordenal["idpedidos"])}'
        query=query+ ' group by pg.id_producto_especifico;'
        cursor_dict.execute(query)
        ordenes_imagen_producto=cursor_dict.fetchall().copy()
        lista_imagenes=[]
        for imagenes in ordenes_imagen_producto:
            lista_imagenes.append(imagenes['imagen'])
        query=f'SELECT direccion FROM direccion AS d INNER JOIN VENTA AS v ON d.id_direccion=v.id_direccion INNER JOIN pedidos AS p ON p.idpedidos=v.id_pedido WHERE p.idusuario={id_usuario} AND idpedidos={str(ordenal["idpedidos"])}'
        cursor_dict.execute(query)
        ordenes_imagen_producto=cursor_dict.fetchall().copy()
        direcciones_falsas=[]
        direccion=str
        for direccione in direcciones_falsas:
            direccion=direccione['direccion']
        lista_ordenes.append(orden(ordenal['idpedidos'],lista_idproductos,lista_idgeneral,lista_cantidad,lista_nombre,lista_precio,lista_imagenes,direccion))
    return lista_ordenes