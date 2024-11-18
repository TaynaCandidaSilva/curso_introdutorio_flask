from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from repository.database import db
from flask_cors import CORS
from flask_login import UserMixin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"  # Configuracao do B.D

# Iniciando o Banco de Dados
db = SQLAlchemy(app)
CORS(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)


@app.route("/api/products/add", methods=["POST"])
def add_product():
    data = request.json
    if "name" in data and "price" in data:
        product = Product(
            name=data["name"],
            price=data["price"],
            description=data.get("description", ""),
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added successfully"})
    return jsonify({"message": "Invalid product data"}), 400


@app.route("/api/products/delete/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted sucessfully"})
    return jsonify({"message": "Product not found"}), 404


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "description": product.description,
            }
        )
    return jsonify({"message": "Product not found"}), 404


@app.route("/api/products/update/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    data = request.json
    if "name" in data:
        product.name = data["name"]

    if "price" in data:
        product.price = data["price"]

    if "description" in data:
        product.description = data["description"]

    db.session.commit()

    return jsonify({"message": "Product updated sucessfully"}), 200


@app.route("/api/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    products_list = []
    for product in products:
        products_data = {"id": product.id, "name": product.name, "price": product.price}
        products_list.append(products_data)
    return jsonify(products_list)


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
