#todo en español
from flask import Flask, render_template, request, session, redirect, flash, jsonify
import mysql.connector
import os
from funciones import lista_a_dict, actualizar_diccionario,actualizar_diccionario_productoXcategoria, orden, organizar_lista,sumar_cantidad,listar_ordenes,recuperar_contrasena,enviar_correo_confirmar_pago


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
  #  diccionario_ordenes=lista_a_dict(lista_ordenes,ordenal['idpedidos'])
carrito_dicc = {}

@app.route('/reporte_de_visitas', methods=['GET','POST'])
def reporte_de_visitas():
    query_visitas="SELECT p.id_producto_especifico, p.nombre, n.anio, sum(n.numero_visitas) as 'numero_visitas' FROM historial_visitas n INNER JOIN producto_especifico p WHERE n.id_producto_especifico = p.id_producto_especifico GROUP BY n.anio,p.id_producto_especifico;"
    cursor_dict.execute(query_visitas)
    lista_dict=cursor_dict.fetchall()
    print(lista_dict)
    diccionario = lista_a_dict(lista_dict,'id_producto_especifico')
    diccionario_con_llaves=diccionario['1']
    return render_template('reporte_de_visitas.html',visitas=diccionario,llaves=diccionario_con_llaves)

@app.route('/login_empleados',methods=['GET','POST'])
def login_empleados():
    if request.method == 'GET':
        return render_template('login_empleados.html')
    if request.method=='POST':
        usuario_introducido=request.form['username']
        contrasena_introducida=request.form['password']
        query=f'SELECT username,correo,contrasena,id_empleado FROM empleados WHERE username="{usuario_introducido}" AND contrasena="{contrasena_introducida}";'
        cursor.execute(query)
        resultados=cursor.fetchall()
        if len(resultados)>0:
            session['correo']=usuario_introducido
            session['usuario']=resultados[0][0]
            session['id']=resultados[0][3]
            current_user=session['usuario']
            session['logged_in']=True
            session['empleado']=True
            session['datos_erroneos']=False
            return redirect('/')
        else:
            session['datos_erroneos']=True
            return redirect('/login_empleados')

@app.route('/recuperar',methods=['GET','POST'])
def recuperar():
    if request.method == 'POST':
        datos = request.get_json()
        correo=datos[0]['correo']
        resultados={'procesado':'true'}
        query=f'SELECT contrasena FROM usuarios WHERE correo="{correo}"'
        cursor.execute(query)
        contrasenas=cursor.fetchall()
        for contrasena in contrasenas:
            recuperar_contrasena(correo, contrasena)
        return jsonify(resultados)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        datos = request.get_json()
        correo=datos[0]['correo']
        contrasena=datos[1]['password']
        query=f'SELECT username,correo,contrasena,idusuarios FROM usuarios WHERE correo="{correo}" AND contrasena="{contrasena}";'
        cursor.execute(query)
        resultados=cursor.fetchall()
        if len(resultados)>0:
            session['correo']=correo
            session['usuario']=resultados[0][0]
            session['id']=resultados[0][3]
            current_user=session['usuario']
            session['logged_in']=True
            session['datos_erroneos']=False
        else:
            session['datos_erroneos']=True
        resultados={'procesado':'true'}
        return jsonify(resultados)
    else:
         return None

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':    
        datos = request.get_json()
        session['datos_erroneos'] = False
        nombre_usuario = datos[0]['username'] 
        correo_electronico = datos[1]['email']
        nombres = datos[2]['nombre']
        apellido1 = datos[3]['apellido1']
        apellido2 = datos[4]['apellido2']
        contrasena = datos[5]['password']
        contrasena_confirmacion = datos[6]['password_confirmation']
        session['contrasenas_diferentes'] = False
        session['correo_repetido']=False
        if contrasena == contrasena_confirmacion:
            query=f'SELECT username,correo,contrasena FROM usuarios WHERE correo="{correo_electronico}";'
            cursor.execute(query)
            resultados=cursor.fetchall()
            if len(resultados)==0:
                query_insertar = f'INSERT INTO usuarios (username,nombre,apellido1,apellido2,correo,contrasena) VALUES ("{nombre_usuario}","{nombres}","{apellido1}","{apellido2}","{correo_electronico}","{contrasena}")'
                cursor.execute(query_insertar)
                session['logged_in'] = True
                session['correo']=correo_electronico
                session['usuario']=nombre_usuario
                session['id']=cursor.lastrowid
                current_user=session['usuario']
                resultados={'procesado':'true'}
                return jsonify(resultados)
            else:
                session['correo_repetido'] = True
                resultados={'procesado':'true'}
                return jsonify(resultados)
        else:
            session['contrasenas_diferentes'] = True
            resultados={'procesado':'true'}
            return jsonify(resultados)
    else:
         return None

@app.route('/ingresar_direccion',methods=['GET','POST'])
def ingresar_direccion():
    if carrito_dicc:
        if request.method=='GET':
            return render_template('ingresar_direccion.html')
        if request.method=='POST':
            nombres=request.form['nombres']
            apellidos=request.form['apellidos']
            correo=request.form['correo']
            telefono=request.form['telefono']
            calle=request.form['calle']
            colonia=request.form['colonia']
            num_ext=request.form['num_ext']
            num_int=request.form['num_int']
            ciudad=request.form['ciudad']
            estado=request.form['estado']
            codigo_postal=request.form['codigo_postal']
            referencia=request.form['referencia']
            direccion={
                'nombres':nombres,
                'apellidos':apellidos,
                'correo':correo,
                'telefono':telefono,
                'calle':calle,
                'colonia':colonia,
                'num_ext':num_ext,
                'num_int':num_int,
                'ciudad':ciudad,
                'estado':estado,
                'codigo_postal':codigo_postal,
                'referencia':referencia
            }
            return render_template('checkout.html',carrito=carrito_dicc,direccion=direccion)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='GET':
        query=f'SELECT pe.id_producto_especifico,pe.id_producto_general, nombre, precio,imagen FROM historial_visitas AS hv INNER JOIN producto_especifico AS pe ON pe.id_producto_especifico=hv.id_producto_especifico INNER JOIN imagenes_especificas AS ie ON ie.id_producto_especifico=pe.id_producto_especifico WHERE anio=substring(CURDATE(),3,2) AND mes=substring(CURDATE(),6,2) GROUP BY pe.nombre ORDER BY hv.numero_visitas DESC LIMIT 8;'        
        cursor_dict.execute(query)
        populares=cursor_dict.fetchall()
        populares=lista_a_dict(populares,'id_producto_especifico')
        query=f'SELECT pe.id_producto_especifico,pe.id_producto_general, nombre, precio,imagen FROM producto_especifico AS pe INNER JOIN imagenes_especificas AS ie ON ie.id_producto_especifico=pe.id_producto_especifico ORDER BY pe.fecha_creacion DESC LIMIT 8;'        
        cursor_dict.execute(query)
        nuevos=cursor_dict.fetchall()
        nuevos=lista_a_dict(nuevos,'id_producto_especifico')
        return render_template('index.html',nuevos=nuevos,populares=populares,carrito=carrito_dicc)

@app.route('/shop',methods=['GET','POST'])
def tienda():
    productos_dict=actualizar_diccionario(cursor_dict, 'producto_general', 'id_producto_general')
    productos_especificos_amostrar=actualizar_diccionario(cursor_dict, 'producto_especifico', 'id_producto_general')
   
    return render_template('shop.html',productos=productos_dict,productos_especificos_amostrar=productos_especificos_amostrar,carrito=carrito_dicc)

@app.route('/shop/<categoria>', methods=['GET'])
def productos_categoria(categoria):
    #diccionario de productos generales por categoria dada
    query = f"SELECT p.id_producto_general,p.nombre_general, p.descripcion_general,p.imagen,p.activo,p.id_categoria,c.categoria FROM producto_general p INNER JOIN categoria_producto c WHERE c.id_categoria = p.id_categoria AND c.categoria = '{categoria}';"
    cursor_dict.execute(query)
    productos_categoria=cursor_dict.fetchall()
    productos_categoria=actualizar_diccionario_productoXcategoria(cursor_dict, 'id_producto_general', categoria)
    productos_especificos_amostrar=actualizar_diccionario(cursor_dict, 'producto_especifico', 'id_producto_general')
    return render_template('shop.html',productos=productos_categoria,productos_especificos_amostrar=productos_especificos_amostrar,carrito=carrito_dicc)

@app.route('/ver_ordenes',methods=['GET','POST'])
def ver_ordenes():
    if 'logged_in' in session:
        lista_ordenes=listar_ordenes(cursor_dict,session['id'])
        if request.method=='GET':
            total=[]
            for objeto in lista_ordenes:
                total.append(sumar_cantidad(objeto.precio, objeto.cantidad))
            return render_template('ver_ordenes.html',lista_ordenes=lista_ordenes,total=total,carrito=carrito_dicc)#usuario_actual=idusuario
    else:
        return redirect('/')
    
@app.route('/ver_orden/<idpedido>',methods=['GET','POST'])
def ver_orden(idpedido):
    if 'logged_in' in session:
        lista_ordenes=listar_ordenes(cursor_dict,session['id'])
        pedido=orden
        if request.method=='GET':
            for objeto in lista_ordenes:
                if int(idpedido)==objeto.idpedido:
                    pedido=objeto
            total=sumar_cantidad(pedido.precio,pedido.cantidad)
            return render_template('ver_orden.html',pedido=pedido,total=total,carrito=carrito_dicc)
    else:
        return redirect('/')
        

@app.route('/agregar_producto', methods=['GET','POST'])
def agregar_producto():
    if request.method=='GET':
        if 'empleado' in session:
            if session['empleado']==True:
                return render_template('agregar_producto.html', categorias=categorias)
            else:
                return redirect('/')
        else:
            return redirect('/')
    if request.method=='POST':
        nombre_introducido=request.form['nombre_producto']
        descripcion_introducido=request.form['descripcion']
        foto_introducida=request.files['foto']
        foto_ruta = foto_introducida.filename
        foto_introducida.save(os.path.join('static/img/',foto_ruta))
        if 'activo' in request.form:
            activo_introducido=1
        else:
            activo_introducido=0
        query_select = f'SELECT id_categoria FROM categoria_producto WHERE categoria = "{request.form["categoria"]}";'
        cursor_dict.execute(query_select)
        lista_id_categoria = cursor_dict.fetchall()
        id_categoria = lista_id_categoria[0]["id_categoria"]
        query=f'INSERT INTO producto_general (nombre_general,descripcion_general,imagen,id_categoria,activo) VALUES ("{nombre_introducido}","{descripcion_introducido}","{foto_ruta}","{id_categoria}",{activo_introducido})'
        cursor_dict.execute(query)
        conexion.commit()
        productos_dict=actualizar_diccionario(cursor_dict,'producto_general','id_producto_general')
        return render_template('agregar_producto.html', mensaje='exito',categorias=categorias)

@app.route('/editar_producto_general/<id_general>', methods=['GET','POST'])
def editar_producto_general(id_general):    
    productos_dict=actualizar_diccionario(cursor_dict, 'producto_general', 'id_producto_general')
    producto=productos_dict[id_general]
    if request.method=='GET':
        if 'empleado' in session:
            if session['empleado']==True:
                query_select = f'SELECT categoria FROM categoria_producto WHERE id_categoria = "{producto["id_categoria"]}";'
                cursor_dict.execute(query_select)
                lista_id_categoria = cursor_dict.fetchall()
                categoria_p = lista_id_categoria[0]["categoria"]
                return render_template('editar_producto_general.html', categorias=categorias,producto=producto,categoria_p=categoria_p)
            else:
                return redirect('/')
        else:
            return redirect('/')
    if request.method=='POST':
        nombre_introducido=request.form['nombre_producto']
        descripcion_introducido=request.form['descripcion']
        foto_introducida=request.files['foto']
        foto_ruta = foto_introducida.filename
        if foto_ruta!='':
            foto_introducida.save(os.path.join('static/img/',foto_ruta))
        if 'activo' in request.form:
            activo_introducido=1
        else:
            activo_introducido=0
        if foto_ruta=='':
            query=f'UPDATE producto_general SET nombre_general="{nombre_introducido}", descripcion_general="{descripcion_introducido}", activo="{activo_introducido}" WHERE id_producto_general={producto["id_producto_general"]}'
        else:
            query=f'UPDATE producto_general SET nombre_general="{nombre_introducido}", descripcion_general="{descripcion_introducido}", imagen="{foto_ruta}", activo="{activo_introducido}" WHERE id_producto_general={producto["id_producto_general"]}'
        cursor_dict.execute(query)
        conexion.commit()
        productos_dict=actualizar_diccionario(cursor_dict,'producto_general','id_producto_general')
        producto=productos_dict[id_general]
        return render_template('editar_producto_general.html', mensaje='exito',categorias=categorias,producto=producto)

@app.route('/cart',methods=['GET','POST'])
def carrito():
    if request.method=='GET':
        return render_template('cart.html',carrito=carrito_dicc)

@app.route('/actualizar_carritodict',methods=['GET','POST'])
def actualizar_carritodict():
    if request.method == "POST":
        datos_actualizados = request.get_json()
        id_producto=datos_actualizados[0]['id_producto']
        cantidad=datos_actualizados[1]['cantidad']
        tipo=datos_actualizados[2]['tipo']
        if tipo=='actualizar':
            carrito_dicc[id_producto]['cantidad']=cantidad
        else:
            carrito_dicc.pop(id_producto)
        resultados={'procesado':'true'}

        return jsonify(resultados)

@app.route('/checkout')
def pago():
    if(len(carrito_dicc)==0):
        return redirect('/cart')
    return render_template('checkout.html',carrito=carrito_dicc)

@app.route('/contact')
def contacto():
    return render_template('contact.html')


@app.route('/producto/<id_producto_general>/<id_producto_especifico>', methods=['GET','POST'])
def producto_especifico(id_producto_general,id_producto_especifico):
    productos_especificos_dict=actualizar_diccionario(cursor_dict, 'producto_especifico', 'id_producto_especifico')
    producto_especifico=productos_especificos_dict[id_producto_especifico]
    query = f"SELECT imagen FROM imagenes_especificas WHERE id_producto_especifico = {id_producto_especifico};"
    lista_fotos = organizar_lista(cursor_dict,query,'imagen')
    lista_tallas = actualizar_diccionario(cursor_dict,'talla','id_talla')
    lista_colores = actualizar_diccionario(cursor_dict,'color','id_color')
    if request.method=='GET':
        query=f'call cuenta_visitas({id_producto_especifico});'
        cursor_dict.execute(query)
        return render_template('producto.html',producto=producto_especifico, fotos=lista_fotos,tallas=lista_tallas, colores=lista_colores,carrito=carrito_dicc)
    if request.method=='POST':
        if id_producto_especifico not in carrito_dicc:
            carrito_dicc[id_producto_especifico]={
                'id_producto_especifico':id_producto_especifico,
                'precio':request.form['precio'],
                'cantidad':request.form['cantidad_form'],
                'nombre':request.form['nombre_form']
            }
        else:
            carrito_dicc[id_producto_especifico]['cantidad']=str(int(request.form['cantidad_form'])+int(carrito_dicc[id_producto_especifico]['cantidad']))
        return render_template('producto.html',producto=producto_especifico, fotos=lista_fotos,tallas=lista_tallas, colores=lista_colores,carrito=carrito_dicc)

#@app.route('/agregarcarrito')
#def agregarcarrito(id):


@app.route('/logout',methods=['GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        return redirect("/")

@app.route('/productos_generales',methods=['GET'])
def productos_generales():
    if request.method=='GET':
        if 'empleado' in session:
            if session['empleado']==True:
                productos_dict=actualizar_diccionario(cursor_dict,'producto_general','id_producto_general')
                return render_template('productos_generales.html',productos=productos_dict,categorias=categorias)
            else:
                return redirect('/')
        else:
            return redirect('/')

@app.route('/productos_especificos/<id_producto_general>',methods=['GET'])
def productos_especificos(id_producto_general):
    if request.method=='GET':
        if 'empleado' in session:
            if session['empleado']==True:
                query=f'select* FROM producto_especifico AS pe INNER JOIN imagenes_especificas AS ie ON ie.id_producto_especifico=pe.id_producto_especifico WHERE id_producto_general={id_producto_general} GROUP BY nombre;'    
                cursor_dict.execute(query)
                resultados=cursor_dict.fetchall()    
                return render_template('productos_especificos.html',productos=resultados)
            else:
                return redirect('/')
        else:
            return redirect('/')
    

@app.route('/agregar_producto_especifico/<id_producto_general>', methods=['GET','POST'])
def agregar_producto_especifico(id_producto_general):
    productos_dict=actualizar_diccionario(cursor_dict,'producto_general','id_producto_general')
    categoria = productos_dict[id_producto_general]['id_categoria'] 
    if request.method=='GET':
        if 'empleado' in session:
            if session['empleado']==True:
                producto = productos_dict[str(id_producto_general)]
                return render_template("agregar_subproducto.html",producto=producto, colores=colores, tallas=tallas,id_categoria=categoria)
            else:
                return redirect('/')
        else:
            return redirect('/')       
    if request.method == 'POST':
        producto = productos_dict[str(id_producto_general)]
        nombre_producto = request.form['nombre_producto']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        detalles = request.form['detalles']
        cantidad = request.form['cantidad']
        if 'activo' in request.form:
            activo_introducido=1
        else:
            activo_introducido=0
        #consigue el id de la talla ingresada en el form
        if categoria == 2:
            query_select = f'SELECT id_talla FROM talla WHERE talla = "{request.form["talla"]}";'
            cursor_dict.execute(query_select)
            lista_id_talla = cursor_dict.fetchall()
            id_talla = lista_id_talla[0]["id_talla"]
        else:
            id_talla = 5
        #consigue el id del color ingresado en el form
        if categoria != 2: 
            query_select = f'SELECT id_color FROM color WHERE color = "{request.form["color"]}";'
            cursor_dict.execute(query_select)
            lista_id_color = cursor_dict.fetchall()
            id_color = lista_id_color[0]['id_color']
        else:
            id_color = 3
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
        query=f'UPDATE producto_general SET activo=1 WHERE id_producto_general={id_producto_general};'
        cursor_dict.execute(query)
        conexion.commit()
        productos_especificos_dict=actualizar_diccionario(cursor_dict, 'producto_especifico', 'id_producto_especifico')
        return render_template("agregar_subproducto.html",producto=producto, colores=colores, tallas=tallas, id_categoria = categoria)

@app.route('/editar_producto_especifico/<id_producto_general>/<id_producto_especifico>', methods=['GET','POST'])
def editar_producto_especifico(id_producto_general,id_producto_especifico):
    productos_especificos_dict=actualizar_diccionario(cursor_dict, 'producto_especifico', 'id_producto_especifico')
    producto_e=productos_especificos_dict[id_producto_especifico]
    productos_dict=actualizar_diccionario(cursor_dict,'producto_general','id_producto_general')
    categoria = productos_dict[id_producto_general]['id_categoria'] 
    if request.method=='GET':
        if 'empleado' in session:
            if session['empleado']==True:
                query=f'select* FROM producto_especifico AS pe INNER JOIN imagenes_especificas AS ie ON ie.id_producto_especifico=pe.id_producto_especifico WHERE id_producto_general={id_producto_general} GROUP BY nombre;'    
                cursor_dict.execute(query)
                resultados=cursor_dict.fetchall()    
                producto = productos_dict[str(id_producto_general)]
                return render_template("editar_producto_especifico.html",producto=producto,producto_e=producto_e,colores=colores, tallas=tallas,id_categoria=categoria)
            else:
                return redirect('/')
        else:
            return redirect('/')
    if request.method == 'POST':
        producto = productos_dict[str(id_producto_general)]
        nombre_producto = request.form['nombre_producto']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        detalles = request.form['detalles']
        cantidad = request.form['cantidad']
        if 'activo' in request.form:
            activo_introducido=1
        else:
            activo_introducido=0
        #insertar registro en base de datos
        query=f'UPDATE producto_especifico SET nombre="{nombre_producto}", descripcion="{descripcion}",precio="{precio}",detalles="{detalles}",cantidad="{cantidad}", activo="{activo_introducido}" WHERE id_producto_especifico={id_producto_especifico};'
        cursor_dict.execute(query)
        conexion.commit()
        fotos = request.files.getlist('foto')
        #guardar fotos localmente y en la base de datos
        for foto in fotos:
            foto_ruta = foto.filename
            if foto_ruta!='':
                foto.save(os.path.join('static/img/',foto_ruta))
                query=f'INSERT INTO imagenes_especificas (id_producto_especifico,imagen) VALUES({id_producto_especifico},"{foto_ruta}")'
                cursor_dict.execute(query)
                conexion.commit()
        productos_especificos_dict=actualizar_diccionario(cursor_dict, 'producto_especifico', 'id_producto_especifico')
        producto_e=productos_especificos_dict[id_producto_especifico]
        productos_especificos_dict=actualizar_diccionario(cursor_dict, 'producto_especifico', 'id_producto_especifico')
        return render_template("editar_producto_especifico.html",producto=producto,producto_e=producto_e, colores=colores, tallas=tallas, id_categoria = categoria)


@app.route('/verificar_pago', methods=['GET','POST'])
def verificar_pago():
    if request.method=='POST':
        datos = request.get_json()
        calle=datos['direccion']['calle']
        colonia=datos['direccion']['colonia']
        num_ext=datos['direccion']['numero exterior']
        num_int=datos['direccion']['numero interior']
        referencia=datos['direccion']['referencia']
        ciudad=datos['direccion']['ciudad']
        estado=datos['direccion']['estado']
        cp=datos['direccion']['codigo_postal']
        nombre=datos['direccion']['nombres']
        apellido=datos['direccion']['apellidos']
        telefono=datos['direccion']['telefono']
        correo=datos['direccion']['correo']
        carrito_dicc.clear()
        resultados={'procesado':'true'}
        query='SELECT MAX(idpedidos) FROM pedidos;'
        cursor_dict.execute(query)
        lista_ids=cursor_dict.fetchall()
        if len(lista_ids)!=0:
            id_pedido=int(lista_ids[0]['MAX(idpedidos)'])+1
        else:
            id_pedido=1
        if num_int=='':
            direccion=f'{calle} #{num_ext} {colonia}'
        else:
            direccion=f'{calle} #{num_ext}, #{num_int} {colonia}'
        if 'logged_in' in session:
            idusuario_direccion=session['id']
        else:
            idusuario_direccion=4
        query=f"INSERT INTO direccion(direccion,ciudad,estado,cp,nombre,apellido,correo,telefono,id_usuario,referencia) VALUES('{direccion}','{ciudad}','{estado}',{cp},'{nombre}','{apellido}','{correo}','{telefono}',{idusuario_direccion},'{referencia}');"
        cursor_dict.execute(query)
        conexion.commit()
        id_direccion_nuevo = cursor_dict.lastrowid
        carrito=datos['carrito']
        for id_producto,producto in carrito.items():
            cantidad=producto['cantidad']
            precio=producto['precio']   
            query=f"INSERT INTO pedidos(idpedidos,idproductos,cantidad,idusuario,precio) VALUES({id_pedido},{id_producto},{cantidad},{idusuario_direccion},{precio});"
            cursor_dict.execute(query)
            conexion.commit()
        costo=float(datos['amount']['value'])
        tnx_id=datos['id']
        estado_venta=datos['status']
        fecha=datos['create_time']
        fecha=fecha.replace('T',' ')
        fecha=fecha.replace('Z','')
        query=f"INSERT INTO venta(costo,tnx_id,estado,fecha,id_pedido,id_direccion) VALUES({costo},'{tnx_id}','{estado_venta}','{fecha}',{id_pedido},{id_direccion_nuevo});"
        cursor_dict.execute(query)
        conexion.commit()
        enviar_correo_confirmar_pago(correo,nombre,apellido,direccion,carrito)
        return jsonify(resultados)


if __name__=='__main__':
    app.run(debug=True)
    conexion.close()