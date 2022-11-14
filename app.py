#todo en español
from flask import Flask, request, render_template
import mysql.connector


app = Flask(__name__)

@app.route('/')
def index():
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


if __name__=='__main__':
    conexion=mysql.connector.connect(user='admin',password='contrasenaAdmin',host='localhost',database='finkies')
    cursor=conexion.cursor()
    query='SELECT * FROM usuarios;'
    cursor.execute(query)
    resultados=cursor.fetchall()
    for fila in resultados:
        print(fila)
    app.run(debug=True)
    conexion.close()

##select
# query='SELECT * FROM usuarios;'
#     cursor.execute(query)
#     resultados=cursor.fetchall()
#     for fila in resultados:
#         print(fila)