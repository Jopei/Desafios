# Importa as bibliotecas necessárias do Flask
from flask import Flask, render_template, request, redirect, url_for

# Inicia a aplicação Flask
app = Flask(__name__)

# Lista para armazenar informações das pessoas
pessoas = []

# Rota principal que renderiza a página inicial
@app.route('/')
def index():
    return render_template('index.html', pessoas=pessoas, total_notas_moedas=calcular_total_notas_moedas(pessoas), exibir_notas_moedas=exibir_notas_moedas)

# Rota para inserir informações de uma pessoa
@app.route('/inserir_pessoa', methods=['POST'])
def inserir_pessoa():
    try:
        # Obtém dados do formulário
        nome = request.form['nome']
        valor_passagem = float(request.form['valor_passagem'])
        passagens = int(request.form['passagens'])

        if valor_passagem <= 0 or passagens <= 0:
            raise ValueError("Valores inválidos. Certifique-se de inserir valores positivos.")

        # Calcula o total do valor e a quantidade de notas e moedas necessárias
        total_valor = passagens * valor_passagem
        qtd_notas_moedas = calcular_notas_moedas(total_valor)

        # Adiciona informações à lista de pessoas
        pessoas.append((nome, valor_passagem, passagens, qtd_notas_moedas))

        # Redireciona para a página de pessoas
        return redirect(url_for('listar_pessoas'))

    except ValueError as e:
        # Em caso de erro de validação, exibe uma mensagem de erro na página
        return render_template('index.html', pessoas=pessoas, mensagem_erro=str(e))

# Rota para a página de pessoas inseridas
@app.route('/pessoas')
def listar_pessoas():
    nomes_pessoas = [pessoa[0] for pessoa in pessoas]
    return render_template('pessoas.html', nomes_pessoas=nomes_pessoas)

# Rota para a página com o total de moedas
@app.route('/total_moedas/<int:pessoa_index>')
def detalhes_moedas(pessoa_index):
    pessoa = pessoas[pessoa_index]
    total_notas_moedas = pessoa[3]
    return render_template('total_moedas.html', pessoa=pessoa, total_notas_moedas=total_notas_moedas, exibir_notas_moedas=exibir_notas_moedas)

# Rota para a página com o total de moedas para todas as pessoas
@app.route('/total_moedas_global')
def total_moedas_global():
    total_notas_moedas = calcular_total_notas_moedas(pessoas)
    return render_template('total_moedas.html', total_notas_moedas=total_notas_moedas)

# Função para calcular a quantidade de notas e moedas necessárias
def calcular_notas_moedas(valor):
    notas_moedas = [50, 10, 5, 2, 1, 0.5, 0.25, 0.1, 0.05, 0.01]
    qtd_notas_moedas = [0] * len(notas_moedas)

    for i in range(len(notas_moedas)):
        qtd_notas_moedas[i] = int(valor // notas_moedas[i])
        valor %= notas_moedas[i]

    return qtd_notas_moedas

# Função para exibir as notas e moedas
def exibir_notas_moedas(qtd_notas_moedas):
    notas_moedas = [50, 10, 5, 2, 1, 0.5, 0.25, 0.1, 0.05, 0.01]
    mensagem = ""

    for i in range(len(notas_moedas)):
        if qtd_notas_moedas[i] > 0:
            if notas_moedas[i] >= 1:
                mensagem += f"{qtd_notas_moedas[i]} nota(s) de {notas_moedas[i]}\n"
            else:
                mensagem += f"{qtd_notas_moedas[i]} moeda(s) de {notas_moedas[i]:.2f}\n"

    return mensagem

# Função para calcular o total de notas e moedas utilizadas por todas as pessoas
def calcular_total_notas_moedas(pessoas):
    total_notas_moedas = [0] * 10

    for pessoa in pessoas:
        for i in range(10):
            total_notas_moedas[i] += pessoa[3][i]

    return total_notas_moedas

@app.route('/inserir')
def inserir():
    return render_template('inserir.html')

@app.route('/limpar')
def limpar():
    pessoas.clear()
    return render_template('index.html', pessoas=pessoas, total_notas_moedas=calcular_total_notas_moedas(pessoas), exibir_notas_moedas=exibir_notas_moedas)


# Executa o aplicativo se este script for executado diretamente
if __name__ == '__main__':
    app.run(debug=True)
