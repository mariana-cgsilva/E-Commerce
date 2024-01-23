from flask import Flask, request, jsonify  #importando a Classe Flask da biblioteca flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  #permitir que sistemas de forma acessem o meu sistema swagger

app = Flask(__name__)   #Criar instância do aplicativo flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)
CORS(app)

#Modelagem
#Produto (id, name, price, description)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, )
    description = db.Column(db.Text, nullable=True)

@app.route('/api/products/add', methods=["POST"])
def add_product():
    data = request.json
    if 'name' in data and 'price' in data: 
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify ({"message": "Product added successfully"})
    return jsonify({"message": "Invalid product data"}), 400

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    #Recuperar o produto da base de dados
    #Verificar se produto existe 
    #Se esiste, apagar da base de dados
    #Se não existe, retornar 404 not found
    product = Product.query.get(product_id)
    if product: 
        db.session.delete(product)
        db.session.commit()
        return jsonify ({"message": "Product deleted successfully"})
    return jsonify({"message": "Product not found"}), 404       

@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product: 
        return jsonify ({
           "id": product.id, 
           "name": product.name,
           "price": product.price,
           "description": product.description
           }), 200
    return jsonify({"message": "Product not found"}), 404 

@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product: 
        return jsonify({"message": "Product not found"}), 404
    
    data = request.json
    if 'name' in data: 
        product.name = data['name']

    if 'description' in data: 
        product.description= data['description']

    if 'price' in data: 
        product.price = data['price']

    if 'id' in data: 
        product.id = data['id']

    db.session.commit()
    return jsonify({"message": "Product updated successfully"}), 200

@app.route('/api/products', methods=["GET"])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products: 
        product_data = {
           "id": product.id, 
           "name": product.name,
           "price": product.price,
           "description": product.description
        }
        product_list.append(product_data)
    return jsonify(product_list)


#Rotas pelas quais os usuário comunicarão com a API (endereço = endpoint)
#Definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == "__main__":
    app.run(debug=True)

