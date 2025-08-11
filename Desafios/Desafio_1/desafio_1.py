from flask import Flask, request

app = Flask(__name__)

@app.route("/") # Rota principal
def ola_mundo():
    return "<h1>Olá mundo</h1>" \
    "<a href='/sobre'>Sobre</a>" \
    "</br>" \
    "<a href='/perfil/socorro'>Perfil</a>" \
    "</br>" \
    "<a href='/produto/26'>Produto</a>" \
    "</br>" \
    "<a href='/hobby'>Hobby</a>" \
    "</br>" \
    "<a href='/filme'>Filme</a>" \
    "</br>" \
    "<a href='/musica'>Música</a>" \

@app.route("/sobre")
def sobre():
    return "<h3>Está é a página sobre</h3>"

@app.route("/hobby")
def hobby():
    return "<h3>Jogar jogos eletrônicos em um computador pessoal</h3>"

@app.route("/filme")
def filme():
    return "<h2>Ainda estou aqui</h2>"

@app.route("/musica")
def musica():
    return "<h1>Construção - Chico Buarque</h1>"

@app.route("/perfil/<usuario>")
def perfil(usuario):
    return f"<h2>Essa é a página de perfil de {usuario}</h2>"

@app.route("/produto/<int:id_produto>")
def consultar_produto(id_produto):
    return f"<h1>Exibindo dados do produto com ID: {id_produto}</h1>"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        return f"<h1>Usuário: {usuario}</h1>"
    else:
        return '''
            <form method="post">
                <input type="text" name="usuario">
                <input type="submit" value="Login">
            </form>
        '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)