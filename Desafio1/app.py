# Importa as bibliotecas necessárias do Flask
from flask import Flask, render_template, request, redirect, url_for
from flask import send_file
from docx import Document
import pandas as pd
from reportlab.pdfgen import canvas

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
                mensagem += f"{qtd_notas_moedas[i]} nota(s) de {notas_moedas[i]} real(is)\n"
            else:
                mensagem += f"{qtd_notas_moedas[i]} moeda(s) de {notas_moedas[i]:.2f} centavo(os)\n"

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

@app.route('/exportar_excel')
def exportar_excel():
    if not pessoas:
        return "Nenhuma pessoa para exportar."

    # Criando um DataFrame do pandas com os dados
    df = pd.DataFrame(pessoas, columns=['Nome', 'Valor', 'Quantidade de Passagens', 'Quantidade de Moedas'])

    # Exportando para um arquivo Excel (xlsx)
    excel_filename = 'pessoas_data.xlsx'
    df.to_excel(excel_filename, index=False)

    return f'Dados exportados para {excel_filename}.'

@app.route('/gerar_pdf')
def gerar_pdf():
    # Crie um objeto PDF
    response = canvas.Canvas("dados_pessoas.pdf")

    # Adicione os cabeçalhos do PDF
    response.drawString(100, 800, "Nome")
    response.drawString(200, 800, "Valor")
    response.drawString(300, 800, "Qtd Passagens")
    response.drawString(400, 800, "Qtd de Moedas")

    # Adicione os dados da lista de pessoas ao PDF
    y_position = 780
    for pessoa in pessoas:
        response.drawString(100, y_position, str(pessoa[0]))
        response.drawString(200, y_position, str(pessoa[1]))
        response.drawString(300, y_position, str(pessoa[2]))
        response.drawString(400, y_position, str(pessoa[3]))

        y_position -= 20

    # Salve o PDF e finalize o objeto
    response.save()

    return "PDF gerado com sucesso!"

@app.route('/exportar_word')
def exportar_word():
    # Criar um novo documento Word
    doc = Document()

    # Adicionar um título ao documento
    doc.add_heading('Relatório de Pessoas', 0)

    # Adicionar uma tabela com cabeçalhos
    table = doc.add_table(rows=1, cols=4)
    table.autofit = True

    header_cells = table.rows[0].cells
    header_cells[0].text = 'Nome'
    header_cells[1].text = 'Valor'
    header_cells[2].text = 'Qtd de Passagens'
    header_cells[3].text = 'Qtd de Moedas'

    # Adicionar os dados da lista de pessoas à tabela
    for pessoa in pessoas:
        row_cells = table.add_row().cells
        row_cells[0].text = pessoa[0]  # Nome
        row_cells[1].text = str(pessoa[1])  # Valor
        row_cells[2].text = str(pessoa[2])  # Quantidade de Passagens
        row_cells[3].text = '\n'.join(exibir_notas_moedas(pessoa[3]))  # Quantidade de Moedas

    # Salvar o documento em um arquivo temporário
    temp_filename = 'relatorio_pessoas.docx'
    doc.save(temp_filename)

    # Enviar o arquivo para o cliente
    return send_file(temp_filename, as_attachment=True, download_name='relatorio_pessoas.docx')

# Executa o aplicativo se este script for executado diretamente
if __name__ == '__main__':
    app.run(debug=True)