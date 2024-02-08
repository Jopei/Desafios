from flask import Flask, render_template
import pyrebase
import time
import snap7.client as client
import snap7.client as c
from snap7.util import *
from snap7.snap7types import *
import numbers
import time
import sys
import os
import snap7

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

TestePLC = c.Client()
TestePLC.connect("192.168.1.10",0,1)
# Função para buscar o dado booleano e armazená-lo em uma variável
@app.route('/')
def index():
    # Busca o dado booleano no Firebase
    dado_booleano = buscar_dado_booleano("ligado")
    
    # Envia para o PLC
    
    
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
    EscreveDados(TestePLC,0,S7WLBit,1,0,dado_booleano)
    return str(dado_booleano)

def enviar_segundo_para_firebase():
    while True:
        try:
            segundo = time.localtime().tm_sec
            db.child("segundotempo").set(segundo)
            time.sleep(1)  # Espera 1 segundo antes de atualizar novamente
        except Exception as e:
            print("Ocorreu um erro ao enviar o segundo para o Firebase:", e)

def enviar_para_plc(valor):
    try:
        # Conecte-se ao PLC
        plc = client.Client()
        plc.connect('192.168.1.10', 0, 1)  # Substitua 'endereco_ip_plc' pelo endereço IP do seu PLC

        # Envie o valor para a entrada Q0.0
        plc.write_bit('Q0.0', valor)

        # Desconecte-se do PLC
        plc.disconnect()
    except Exception as e:
        print("Ocorreu um erro ao enviar dados para o PLC:", e)

def ReadMemory(plc,byte,datatype,db,bit=0,tam_st=0):
    if datatype=='String':
        result = plc.read_area(areas['DB'],db,byte,tam_st+2)
        return get_string(result,0,tam_st+2)
    else:
        result = plc.read_area(areas['DB'],db,byte,datatype)
    if datatype==S7WLBit:
        return get_bool(result,0,bit)
    elif datatype==S7WLByte or datatype==S7WLWord:
        return get_int(result,0)
    elif datatype==S7WLReal:
        return get_real(result,0)
    elif datatype==S7WLDWord:
        return get_dword(result,0)
    else:
        return None

def EscreveDados(plc,byte,datatype,db,bit,valor):
    resultado = plc.read_area(areas['DB'],db,byte,datatype)
    if datatype==S7WLBit:
        set_bool(resultado,0,bit,valor)
    elif datatype==S7WLByte or datatype==S7WLWord:
        set_int(resultado,0,valor)
    elif datatype==S7WLReal:
        set_real(resultado,0,valor)
    elif datatype==S7WLDWord:
        set_dword(resultado,0,valor)
    plc.write_area(areas["DB"],db,byte,resultado)

if __name__ == '__main__':
    # Inicia uma thread separada para enviar o tempo para o Firebase continuamente
    import threading
    firebase_thread = threading.Thread(target=enviar_segundo_para_firebase)
    firebase_thread.daemon = True
    firebase_thread.start()

    # Inicia o servidor Flask
    app.run(debug=True)