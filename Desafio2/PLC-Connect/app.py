from flask import Flask, render_template
import pyrebase
import time
import snap7.client as client

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
    enviar_dado_para_plc(dado_booleano)
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

def enviar_dado_para_plc(dado_booleano):
    try:
        # Conecta-se ao PLC Siemens
        plc = client.Client()
    #Area do plc    plc.connect('192.168.0.1', 0, 2)  # Substitua pelo IP do seu PLC

        # Escreve o dado booleano em um byte específico do DB
        byte = 10  # Substitua pelo byte onde você deseja escrever o dado booleano
        db_number = 1  # Substitua pelo número do DB
        plc.write_area(client.S7AreaDB, db_number, byte, [dado_booleano])

        plc.disconnect()
    except Exception as e:
        print("Ocorreu um erro ao enviar o dado para o PLC:", e)

def enviar_segundo_para_firebase():
    while True:
        try:
            segundo = time.localtime().tm_sec
            db.child("segundotempo").set(segundo)
            time.sleep(1)  # Espera 1 segundo antes de atualizar novamente
        except Exception as e:
            print("Ocorreu um erro ao enviar o segundo para o Firebase:", e)


if __name__ == '__main__':
    # Inicia uma thread separada para enviar o tempo para o Firebase continuamente
    import threading
    firebase_thread = threading.Thread(target=enviar_segundo_para_firebase)
    firebase_thread.daemon = True
    firebase_thread.start()

    # Inicia o servidor Flask
    app.run(debug=True)