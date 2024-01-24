from flask import Flask, request, jsonify  #importando a Classe Flask da biblioteca flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  #permitir que sistemas de forma acessem o meu sistema swagger
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)   #Criar instância do aplicativo flask
app.config['SECRET_KEY'] = "minha_chave_123"     #key to enable login
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

#Modelagem 
    #User(id, username, password)
class User(db.Model, UserMixin):                #UserMixin   -> Click "Go to definition" to see class and methods that are already defined
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=True)
    cart = db.relationship('CartItem', backref='user', lazy=True)

#Produto (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, )
    description = db.Column(db.Text, nullable=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

#Autenticação
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(username=data.get("username")).first()
    
    if user and data.get("password") == user.password:
            login_user(user)
            return jsonify({"message": "Logged in successfully"})
    return jsonify({"message": "Unauthorized. Invalid credentials"}), 401

@app.route('/logout', methods=["POST"])
@login_required          #É requisito o usuário estar logado
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})

@app.route('/api/products/add', methods=["POST"])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data: 
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify ({"message": "Product added successfully"})
    return jsonify({"message": "Invalid product data"}), 400

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
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
@login_required
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

#Checkout
@app.route('/api/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    #Usuario
    user = User.query.get(int(current_user.id))
    #Produto
    product = Product.query.get(product_id)

    if user and product: 
        cart_item = CartItem(user_id=user.id, product_id= product.id)
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item added to the cart successfully'}), 200
    return jsonify({'message': 'Failed to add item to the cart'}), 400

@app.route('/api/cart/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_cart(product_id):
    #To remove, filter cart with user and product; is going to delete the first item that was found
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item removed from the cart successfully'}), 200
    return jsonify({'message': 'Failed to remove item from the cart'}), 400  

#Rotas pelas quais os usuário comunicarão com a API (endereço = endpoint)
#Definir uma rota raiz (página inicial) e a função que será executada ao requisitar


if __name__ == "__main__":
    app.run(debug=True)

