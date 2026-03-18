from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)
ARCHIVO = "data.txt"

def cargar_datos():
    try:
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    except:
        return []

def guardar_datos(productos):
    with open(ARCHIVO, "w") as f:
        json.dump(productos, f, indent=4)

@app.route("/")
def index():
    productos = cargar_datos()
    return render_template("index.html", productos=productos)

@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"]
    precio = request.form["precio"]

    productos = cargar_datos()
    productos.append({"nombre": nombre, "precio": precio})
    guardar_datos(productos)

    return redirect("/")

@app.route("/eliminar/<nombre>")
def eliminar(nombre):
    productos = cargar_datos()
    productos = [p for p in productos if p["nombre"] != nombre]
    guardar_datos(productos)

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

    
@app.route("/editar/<nombre>", methods=["GET", "POST"])
def editar(nombre):
    productos = cargar_datos()

    if request.method == "POST":
        nuevo_nombre = request.form["nombre"]
        nuevo_precio = request.form["precio"]

        for p in productos:
            if p["nombre"] == nombre:
                p["nombre"] = nuevo_nombre
                p["precio"] = nuevo_precio

        guardar_datos(productos)
        return redirect("/")

    # GET
    producto = next((p for p in productos if p["nombre"] == nombre), None)
    return render_template("editar.html", producto=producto)
