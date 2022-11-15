#todo en español
from flask import Flask, render_template, request, session, redirect, flash
import mysql.connector


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

@app.route('/agregar_producto.html')
def agregar_producto():
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