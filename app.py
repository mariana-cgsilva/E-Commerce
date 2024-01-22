from flask import Flask     #importando a Classe Flask da biblioteca flask

app = Flask(__name__)   #Criar instância do aplicativo flask

#Rotas pelas quais os usuário comunicarão com a API (endereço = endpoint)
#Definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == "__main__":
    app.run(debug=True)

