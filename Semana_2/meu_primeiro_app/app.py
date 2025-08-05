from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    nome_usuario = 'Visitante'
    return render_template('index.html', usuario=nome_usuario)

@app.route('/produtos')
def produtos():
    lista_produtos = [
        {'nome': 'Microooooondas', 'preco': 'R$1.500,00'},
        {'nome': 'Geladeideira', 'preco': '$2.500,00'},
        {'nome': 'Prateleira', 'preco': 'K$7.500,00'}
    ]
    return render_template('produtos.html', produtos=lista_produtos)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
