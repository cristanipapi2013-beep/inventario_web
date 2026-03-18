from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CONFIGURACIÓN BASE DE DATOS
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///productos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# MODELO
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)


# RUTA PRINCIPAL (LISTAR + BUSCAR)
@app.route("/")
def index():
    query = request.args.get("q")

    if query:
        productos = Producto.query.filter(Producto.nombre.contains(query)).all()
    else:
        productos = Producto.query.all()

    return render_template("index.html", productos=productos)


# AGREGAR PRODUCTO
@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"]
    precio = request.form["precio"]

    nuevo = Producto(nombre=nombre, precio=precio)
    db.session.add(nuevo)
    db.session.commit()

    return redirect("/")


# ELIMINAR PRODUCTO
@app.route("/eliminar/<int:id>")
def eliminar(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect("/")


# EDITAR PRODUCTO
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    producto = Producto.query.get(id)

    if request.method == "POST":
        producto.nombre = request.form["nombre"]
        producto.precio = request.form["precio"]

        db.session.commit()
        return redirect("/")

    return render_template("editar.html", producto=producto)


# EJECUTAR APP
if __name__ == "__main__":
    app.run(debug=True)
