from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    nome_usuario = "João Cana Brava"
    return render_template("index.html", nome_usuario=nome_usuario)

@app.route("/perfil/<nome>")
def perfil(nome):
    logado = True
    nome_usuario = nome
    return render_template("perfil.html", logado=logado, nome_usuario=nome_usuario)

@app.route("/lista_produtos")
def list_produtos():
    produtos = ['Cadeira', 'Janela', 'Estetoscópio']
    return render_template("produtos.html", lista=produtos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)