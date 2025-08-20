import os
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

# --- Configuração da Aplicação Flask ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# --- Definição do formulário ---
class ContatoForm(FlaskForm):
    nome = StringField(
        'Nome',
        validators=[DataRequired(message="Campo obrigatório!")]
    )
    email = StringField(
        'E-mail',
        validators=[
            DataRequired(message="Campo obrigatório"), 
            Email(message="Formato de e-mail inválido!")
        ]
    )
    mensagem = TextAreaField("Mensagem...")
    enviar = SubmitField("Enviar")

# --- Definição objeto para simulação ---
class Usuario:
    def __init__(self, nome, email, mensagem=""):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem        

# --- Rotas da Aplicação ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/vazio", methods=["GET", "POST"])
def formulario_vazio():
    form = ContatoForm()

    # Resposta ao método POST
    if form.validate_on_submit():
        nome_usuario = form.nome.data
        email_usuario = form.email.data
        mensagem_usuario = form.mensagem.data
        return render_template("sucesso.html", 
                               nome_usuario=nome_usuario, 
                               email_usuario=email_usuario, 
                               mensagem_usuario=mensagem_usuario)
    # Resposta ao método GET
    return render_template(
        "formulario.html",
        form=form,
        title="1. Fomulário Vazio"
    )

@app.route("/via-argumentos", methods=["GET", "POST"])
def formulario_via_argumentos():
    form = ContatoForm()

    # Resposta ao método POST
    if form.validate_on_submit():
        nome_usuario = form.nome.data
        email_usuario = form.email.data
        mensagem_usuario = form.mensagem.data
        return render_template("sucesso.html", 
                               nome_usuario=nome_usuario, 
                               email_usuario=email_usuario, 
                               mensagem_usuario=mensagem_usuario)
    # Resposta ao método GET
    elif not form.is_submitted():
        dados_iniciais = {
            "nome": "Jones da Silva",
            "email": "jones.silva@gmail.com",
            "mensagem": "Esta é uma mensagem preenchida por argumentos."
        }
        form = ContatoForm(**dados_iniciais)

    return render_template(
        "formulario.html",
        form=form,
        title="2. Fomulário com Argumentos"
    )

# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True)