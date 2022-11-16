#todo en español
from flask import Flask, render_template, request, session, redirect, flash
import mysql.connector
import os
from funciones import lista_a_dict


app = Flask(__name__)
app.secret_key='234524assdg'
conexion=mysql.connector.connect(user='admin',password='contrasenaAdmin',host='localhost',database='finkies')
cursor=conexion.cursor()
query=f'SELECT * FROM productos;'
cursor_dict=conexion.cursor(dictionary=True)
cursor_dict.execute(query)
productos=cursor_dict.fetchall()
productos_dict=lista_a_dict(productos)
current_user=''

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='GET':
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

@app.route('/shop.html')
def tienda():
    return render_template('shop.html')

@app.route('/ver_ordenes.html',methods=['GET','POST'])
def ordenes():
    if request.method=='GET':
        idusuario=f'SELECT idusuarios FROM usuarios WHERE username="{current_user}";'
        return render_template('ver_ordenes.html')#usuario_actual=idusuario
        
    

@app.route('/agregar_producto.html', methods=['GET','POST'])
def agregar_producto():
    if request.method=='GET':
        return render_template('agregar_producto.html')
    if request.method=='POST':
        nombre_introducido=request.form['nombre_producto']
        precio_introducido=str(request.form['precio'])
        descripcion_introducido=request.form['descripcion']
        foto_introducida=request.files['foto']
        foto_ruta = foto_introducida.filename
        foto_introducida.save(os.path.join('static/img/',foto_ruta))
        existencia_introducido=str(request.form['existencia'])
        if request.form['activo']=='on':
            activo_introducido=True
        else:
            activo_introducido=False
        query=f'INSERT INTO productos (nombre,precio,descripcion,foto,existencia,activo) VALUES ("{nombre_introducido}",{precio_introducido},"{descripcion_introducido}","{foto_ruta}",{existencia_introducido},{activo_introducido})'
        cursor.execute(query)
        return render_template('agregar_producto.html', mensaje='Articulo agregado exitosamente')


@app.route('/cart.html')
def carrito():
    return render_template('cart.html')

@app.route('/checkout.html')
def pago():
    return render_template('checkout.html')

@app.route('/contact.html')
def contacto():
    return render_template('contact.html')

@app.route('/producto/<id>')
def producto(id):
    producto=productos_dict[id]
    return render_template('producto.html', producto=producto)

@app.route('/logout',methods=['GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        return redirect("/")

if __name__=='__main__':
    app.run(debug=True)
    conexion.close()




        
##select
# query='SELECT * FROM usuarios;'
#     cursor.execute(query)
#     resultados=cursor.fetchall()
#     for fila in resultados:
#         print(fila)