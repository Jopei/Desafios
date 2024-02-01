from flask import Flask, render_template
import pyrebase
import time


app = Flask(__name__)
# Configure sua conexão com o Firebase
config = {
        "apiKey": "AIzaSyARE1K6vM4j_QZlDVFBhgC9vl7uaF0c7ho",
        "authDomain": "plc-connect-ed3dd.firebaseapp.com",
        "databaseURL": "https://plc-connect-ed3dd-default-rtdb.firebaseio.com",
        "projectId": "plc-connect-ed3dd",
        "storageBucket": "plc-connect-ed3dd.appspot.com",
        "messagingSenderId": "689102691305",
        "appId": "1:689102691305:web:7fdf7aa6e2bb2f700cc978",
        "measurementId": "G-WESV9N1VQZ"
}

firebase = pyrebase.initialize_app(config)

# Referência para o Firebase Realtime Database
db = firebase.database()

# Função para buscar o dado booleano e armazená-lo em uma variável
# Rota para a página inicial
@app.route('/')
def index():
    # Busca o dado booleano no Firebase
    dado_booleano = buscar_dado_booleano("ligado")
    return render_template('index.html', dado_booleano=dado_booleano)

# Função para buscar o dado booleano
def buscar_dado_booleano(caminho):
    try:
        # Busca o dado booleano no caminho especificado
        dado = db.child(caminho).get().val()
        return dado
    except Exception as e:
        print("Ocorreu um erro ao buscar o dado:", e)
        return None

@app.route('/get_dado_booleano')
def get_dado_booleano():
    # Suponha que dado_booleano seja uma variável global
    # ou definida em um escopo acessível aqui
    dado_booleano = buscar_dado_booleano("ligado")# Exemplo: substitua pelo seu valor real
    return str(dado_booleano)

if __name__ == '__main__':
    app.run(debug=True)