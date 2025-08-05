# app.py
from flask import Flask, redirect, render_template, request, url_for
# Inicializa a aplicação Flask
app = Flask(__name__)

# No início do seu app.py
tarefas = [
    {'id': 1, 'descricao': 'Estudar os conceitos de rotas no Flask', 'concluida': True},
    {'id': 2, 'descricao': 'Criar o formulário de adição de tarefas', 'concluida': False}
]
proximo_id = 3 # Uma variável para controlar o próximo ID a ser usado

@app.route('/')
def index():
    return render_template('index.html', tarefas=tarefas)

@app.route('/adicionar', methods=['POST'])
def adicionar_tarefa():
    global proximo_id  # Usamos o contador global

    descricao = request.form['descricao'].strip()
    if descricao:  # Evita tarefas vazias
        nova_tarefa = {
            'id': proximo_id,
            'descricao': descricao,
            'concluida': False
        }
        tarefas.append(nova_tarefa)
        proximo_id += 1

    return redirect(url_for('index'))

@app.route('/concluir/<int:id_da_tarefa>', methods=['POST'])
def concluir_tarefa(id_da_tarefa):
    for tarefa in tarefas:
        if tarefa['id'] == id_da_tarefa:
            tarefa['concluida'] = True
            break
    return redirect(url_for('index'))

# --- Exercício 1: Exibindo uma Mensagem de Boas-Vindas ---
@app.route('/bemvindo')
def exercicio1():
    """
    Esta função responde à URL /bemvindo.
    Ela passa uma variável 'nome_usuario' para o template 'exercicio1.html'.
    """
    nome_usuario = "Maria"
    return render_template('exercicio1.html', nome_usuario=nome_usuario)

# --- Exercício 2: Listando Itens ---
@app.route('/cursos')
def exercicio2():
    """
    Esta função responde à URL /cursos.
    Ela passa uma lista de cursos para o template 'exercicio2.html'.
    """
    lista_de_cursos = [
    "Desenvolvimento Web com Flask",
    "Python para Análise de Dados",
    "Introdução a Machine Learning",
    "Banco de Dados SQL"
    ]
    return render_template('exercicio2.html', cursos=lista_de_cursos)

# --- Exercício 3: Usando Condicionais ---
@app.route('/perfil/<nome>')
@app.route('/perfil')
def exercicio3(nome=None):
    """
    Esta função responde a /perfil e /perfil/<nome>.
    Ela simula um status de login e passa para o template 'exercicio3.html'.
    """
    logado = nome is not None
    return render_template('exercicio3.html', usuario_logado=logado,
    nome_usuario=nome)

# --- Exercício 4: Herança de Templates ---
@app.route('/sobre')
def exercicio4():
    """
    Renderiza a página 'Sobre', que herda o layout base.
    """
    return render_template('sobre.html')

# --- Bloco para rodar a aplicação ---
if __name__ == '__main__':
    # O modo debug reinicia o servidor automaticamente a cada alteração no código.
    app.run(host='0.0.0.0', port=5000, debug=True)