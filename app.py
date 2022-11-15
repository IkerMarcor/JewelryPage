#todo en español
from flask import Flask, render_template, request, session, redirect, flash
import mysql.connector
import os


app = Flask(__name__)
app.secret_key='234524assdg'
conexion=mysql.connector.connect(user='admin',password='contrasenaAdmin',host='localhost',database='finkies')
cursor=conexion.cursor()

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('index.html')
    if request.method=='POST':
        correo_introducido=request.form['email']
        contrasena_introducida=request.form['password']
        query=f'SELECT username,correo,contrasena FROM usuarios WHERE correo="{correo_introducido}" AND contrasena="{contrasena_introducida}";'
        cursor.execute(query)
        resultados=cursor.fetchall()
        if len(resultados)>0:
            session['correo']=correo_introducido
            session['usuario']=resultados[0][0]
            print(session['usuario'])
            session['logged_in']=True
            session['datos_erroneos']=False
        else:
            session['datos_erroneos']=True
        return render_template('index.html')

@app.route('/shop.html')
def tienda():
    return render_template('shop.html')

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
        #print(nombre_introducido,precio_introducido,descripcion_introducido,foto,existencia_introducido,activo_introducido)
        #nombre,precio,descripcion,foto,existencia,activo
        query=f'INSERT INTO productos (nombre,precio,descripcion,foto,existencia,activo) VALUES ("{nombre_introducido}",{precio_introducido},"{descripcion_introducido}","{foto_ruta}",{existencia_introducido},{activo_introducido})'
        cursor.execute(query)
        return render_template('agregar_producto.html')


@app.route('/cart.html')
def carrito():
    return render_template('cart.html')

@app.route('/checkout.html')
def pago():
    return render_template('checkout.html')

@app.route('/contact.html')
def contacto():
    return render_template('contact.html')

@app.route('/producto.html')
def producto():
    return render_template('producto.html')

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