from flask import Flask     #importando a Classe Flask da biblioteca flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)   #Criar instância do aplicativo flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

#Modelagem
#Produto (id, name, price, description)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, )
    description = db.Column(db.Text, nullable=True)


#Rotas pelas quais os usuário comunicarão com a API (endereço = endpoint)
#Definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == "__main__":
    app.run(debug=True)

