#todo en español
from flask import Flask, render_template, request, session, redirect, flash
import mysql.connector
import os
from funciones import lista_a_dict, actualizar_diccionario

class orden:
    idpedido: int
    idproductos: list
    cantidad: list
    nombre: list
    precio:list
    imagen: list
    def __init__(self, idpedido:int, idproductos:list,cantidad:list,nombre:list,precio:list,imagen:list):
        self.idpedido=idpedido
        self.idproductos=idproductos
        self.cantidad=cantidad
        self.nombre=nombre
        self.precio=precio
        self.imagen=imagen

app = Flask(__name__)
app.secret_key='234524assdg'
conexion=mysql.connector.connect(user='admin',password='contrasenaAdmin',host='localhost',database='finkies')
cursor=conexion.cursor()
cursor_dict=conexion.cursor(dictionary=True)
select_categorias='SELECT * FROM categoria_producto'
idusuario='SELECT idusuario FROM usuarios LIMIT 1'
#diccionario todos los productos generales
productos_dict=actualizar_diccionario(cursor_dict,'producto_general','id_producto_general')
current_user=''
cursor_dict.execute(select_categorias)
categorias=cursor_dict.fetchall()
#diccionario todos los productos especificos
productos_especificos_dict=actualizar_diccionario(cursor_dict, 'producto_especifico', 'id_producto_especifico')
#diccionario de todas las fotos
fotos = actualizar_diccionario(cursor_dict, 'imagenes_especificas', 'id_imagen_especifica')
#diccionario de todos las categorias
categorias=lista_a_dict(categorias,'id_categoria')
query = 'SELECT * FROM talla;'
cursor_dict.execute(query)
tallas = cursor_dict.fetchall()
#diccionario de todas las tallas
tallas = lista_a_dict(tallas,'id_talla')
query = 'SELECT * FROM color;'
cursor_dict.execute(query)
colores = cursor_dict.fetchall()
#diccionario de todos los colores
colores = lista_a_dict(colores,'id_color')
query='SELECT idpedidos FROM pedidos WHERE idusuario='+'1 GROUP BY idpedidos'
cursor_dict.execute(query)
ordenes=cursor_dict.fetchall()
lista_ordenes=[]
for ordenal in ordenes:
    query='SELECT idproductos FROM pedidos WHERE idusuario='+'1 AND idpedidos= '+ str(ordenal['idpedidos'])
    cursor_dict.execute(query)
    ordenes_idproductos=cursor_dict.fetchall().copy()
    lista_idproductos=[]
    for idproducto in ordenes_idproductos:
        lista_idproductos.append(idproducto['idproductos'])
    query='SELECT cantidad FROM pedidos WHERE idusuario='+'1 AND idpedidos= '+ str(ordenal['idpedidos'])
    cursor_dict.execute(query)
    ordenes_cantidad=cursor_dict.fetchall().copy()
    lista_cantidad=[]
    for cantidad in ordenes_cantidad:
        lista_cantidad.append(cantidad['cantidad'])
    lista_cantidad=[int(x) for x in lista_cantidad]
    query='SELECT nombre from pedidos INNER JOIN  producto_especifico as pg on pg.id_producto_especifico=idproductos WHERE idusuario='+'1 AND idpedidos= '+ str(ordenal['idpedidos'])
    cursor_dict.execute(query)
    ordenes_nombre_producto=cursor_dict.fetchall().copy()
    lista_nombre=[]
    for nombre in ordenes_nombre_producto:
        lista_nombre.append(nombre['nombre'])
    query='SELECT pg.precio from pedidos INNER JOIN  producto_especifico as pg on pg.id_producto_especifico=idproductos WHERE idusuario='+'1 AND idpedidos= '+ str(ordenal['idpedidos'])
    cursor_dict.execute(query)
    ordenes_nombre_producto=cursor_dict.fetchall().copy()
    lista_precio=[]
    for nombre in ordenes_nombre_producto:
        lista_precio.append(nombre['precio'])
    lista_precio=[float(x) for x in lista_precio]
    query='SELECT imagen from pedidos INNER JOIN  producto_especifico as pg on pg.id_producto_especifico=idproductos INNER JOIN imagenes_especificas AS ie on pg.id_producto_especifico=ie.id_producto_especifico WHERE idusuario='+'1 AND idpedidos= '+ str(ordenal['idpedidos'])
    query=query+ ' group by pg.id_producto_especifico;'
    cursor_dict.execute(query)
    ordenes_imagen_producto=cursor_dict.fetchall().copy()
    lista_imagenes=[]
    for imagenes in ordenes_imagen_producto:
        lista_imagenes.append(imagenes['imagen'])
    lista_ordenes.append(orden(ordenal['idpedidos'],lista_idproductos,lista_cantidad,lista_nombre,lista_precio,lista_imagenes))
  #  diccionario_ordenes=lista_a_dict(lista_ordenes,ordenal['idpedidos'])

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='GET':
        print(categorias)
        return render_template('index.html')
    if request.method=='POST':
        if 'login' in request.form:
            correo_introducido=request.form['email']
            contrasena_introducida=request.form['password']
            query=f'SELECT username,correo,contrasena FROM usuarios WHERE correo="{correo_introducido}" AND contrasena="{contrasena_introducida}";'
            cursor.execute(query)
            resultados=cursor.fetchall()
            if len(resultados)>0:
                session['correo']=correo_introducido
                session['usuario']=resultados[0][0]
                current_user=session['usuario']
                print(session['usuario'])
                session['logged_in']=True
                session['datos_erroneos']=False
            else:
                session['datos_erroneos']=True
            return render_template('index.html')
        else:
            if 'registro' in request.form:

                session['datos_erroneos'] = False
                nombre_usuario = request.form['username']
                correo_electronico = request.form['email']
                nombres = request.form['nombre']
                apellido1 = request.form['apellido1']
                apellido2 = request.form['apellido2']
                contrasena = request.form['password']
                contrasena_confirmacion = request.form['password_confirmation']
                session['contrasenas_diferentes'] = False
                if contrasena == contrasena_confirmacion:
                    query=f'SELECT username,correo,contrasena FROM usuarios WHERE correo="{correo_electronico}" AND contrasena="{contrasena}";'
                    cursor.execute(query)
                    resultados=cursor.fetchall()
                    if len(resultados)==0:
                        query_insertar = f'INSERT INTO usuarios (username,nombre,apellido1,apellido2,correo,contrasena) VALUES ("{nombre_usuario}","{nombres}","{apellido1}","{apellido2}","{correo_electronico}","{contrasena}")'
                        cursor.execute(query_insertar)
                        session['logged_in'] = True
                    return render_template('index.html')
                else:
                    session['contrasenas_diferentes'] = True
            else:
                return render_template('index.html')

@app.route('/shop')
def tienda():
    productos_especificos_amostrar=actualizar_diccionario(cursor_dict, 'producto_especifico', 'id_producto_general')
    return render_template('shop.html',productos=productos_dict,productos_especificos_amostrar=productos_especificos_amostrar)

@app.route('/ver_ordenes',methods=['GET','POST'])
def ver_ordenes():
    if request.method=='GET':
        print('hola')
        print(ordenal['idpedidos'])
        return render_template('ver_ordenes.html',lista_ordenes=lista_ordenes)#usuario_actual=idusuario

@app.route('/ver_orden/<idpedido>',methods=['GET','POST'])
def ver_orden(idpedido):
    pedido=orden
    if request.method=='GET':
        for objeto in lista_ordenes:
            print(objeto.idpedido)
            print(idpedido)
            if int(idpedido)==objeto.idpedido:
                pedido=objeto
        print('hola')
        print(pedido) #oki El idpedido es una variable pero todo lo demás pues son listas
        
        idusuario=f'SELECT idusuarios FROM usuarios WHERE username="{current_user}";'
        return render_template('ver_orden.html',pedido=pedido)
    

@app.route('/agregar_producto', methods=['GET','POST'])
def agregar_producto():
    if request.method=='GET':
        return render_template('agregar_producto.html', categorias=categorias)
    if request.method=='POST':
        nombre_introducido=request.form['nombre_producto']
        descripcion_introducido=request.form['descripcion']
        foto_introducida=request.files['foto']
        foto_ruta = foto_introducida.filename
        foto_introducida.save(os.path.join('static/img/',foto_ruta))
        if request.form['activo']=='on':
            activo_introducido=True
        else:
            activo_introducido=False
        query_select = f'SELECT id_categoria FROM categoria_producto WHERE categoria = "{request.form["categoria"]}";'
        cursor_dict.execute(query_select)
        lista_id_categoria = cursor_dict.fetchall()
        id_categoria = lista_id_categoria[0]["id_categoria"]
        query=f'INSERT INTO producto_general (nombre_general,descripcion_general,imagen,id_categoria,activo) VALUES ("{nombre_introducido}","{descripcion_introducido}","{foto_ruta}","{id_categoria}",{activo_introducido})'
        cursor_dict.execute(query)
        conexion.commit()
        productos_dict=actualizar_diccionario(cursor_dict,'producto_general','id_producto_general')
        print(productos_dict)
        return render_template('agregar_producto.html', mensaje='exito',categorias=categorias)


@app.route('/cart')
def carrito():
    return render_template('cart.html')

@app.route('/checkout')
def pago():
    return render_template('checkout.html')

@app.route('/contact')
def contacto():
    return render_template('contact.html')

@app.route('/producto/<id_producto_general>')
def producto(id_producto_general):
    producto=productos_dict[id_producto_general]
    return render_template('producto.html', producto=producto)


@app.route('/producto/<id_producto_general>/<id_producto_especifico>')
def producto_especifico(id_producto_general,id_producto_especifico):
    return True

#@app.route('/agregarcarrito')
#def agregarcarrito(id):


@app.route('/logout',methods=['GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        return redirect("/")

@app.route('/productos_generales',methods=['GET'])
def productos_generales():
    productos_dict=actualizar_diccionario(cursor_dict,'producto_general','id_producto_general')
    return render_template('productos_generales.html',productos=productos_dict,categorias=categorias)

@app.route('/agregar_producto_especifico/<id_producto_general>', methods=['GET','POST'])
def agregar_producto_especifico(id_producto_general):
    productos_dict=actualizar_diccionario(cursor_dict,'producto_general','id_producto_general')
    if request.method == 'GET':
        print(productos_dict)
        producto = productos_dict[str(id_producto_general)]
        return render_template("agregar_subproducto.html",producto=producto, colores=colores, tallas=tallas)
    if request.method == 'POST':
        producto = productos_dict[str(id_producto_general)]
        nombre_producto = request.form['nombre_producto']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        detalles = request.form['detalles']
        cantidad = request.form['cantidad']
        if request.form['activo']=='on':
            activo_introducido=True
        else:
            activo_introducido=False
        #consigue el id de la talla ingresada en el form
        query_select = f'SELECT id_talla FROM talla WHERE talla = "{request.form["talla"]}";'
        cursor_dict.execute(query_select)
        lista_id_talla = cursor_dict.fetchall()
        id_talla = lista_id_talla[0]["id_talla"]
        #consigue el id del color ingresado en el form
        query_select = f'SELECT id_color FROM color WHERE color = "{request.form["color"]}";'
        cursor_dict.execute(query_select)
        lista_id_color = cursor_dict.fetchall()
        id_color = lista_id_color[0]['id_color']
        #insertar registro en base de datos
        query=f'INSERT INTO producto_especifico(id_producto_general,nombre,descripcion,precio,detalles,cantidad,activo,id_talla,id_color) VALUES ({id_producto_general},"{nombre_producto}","{descripcion}",{precio},"{detalles}",{cantidad},{activo_introducido},{id_talla},{id_color});'
        cursor_dict.execute(query)
        conexion.commit()
        fotos = request.files.getlist('foto')
        id_nuevo = cursor_dict.lastrowid
        #guardar fotos localmente y en la base de datos
        for foto in fotos:
            foto_ruta = foto.filename
            foto.save(os.path.join('static/img/',foto_ruta))
            query=f'INSERT INTO imagenes_especificas (id_producto_especifico,imagen) VALUES({id_nuevo},"{foto_ruta}")'
            cursor_dict.execute(query)
            conexion.commit()
        productos_especificos_dict=actualizar_diccionario(cursor_dict, 'producto_especifico', 'id_producto_especifico')
        return render_template("agregar_subproducto.html",producto=producto, colores=colores, tallas=tallas)


@app.route('/editar_producto/<id_producto_general>', methods=['GET','POST'])
def editar_producto_general(id_producto_general):

    return render_template("editar_producto_general.html")

if __name__=='__main__':
    app.run(debug=True)
    conexion.close()




        
##select
# query='SELECT * FROM usuarios;'
#     cursor.execute(query)
#     resultados=cursor.fetchall()
#     for fila in resultados:
#         print(fila)