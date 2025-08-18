from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

# Criando/Instaciando a aplicação Flask
app = Flask(__name__)

app.config["SECRET_KEY"] = "uma_chave_de_segurança_muito_dificil"

class MeuFormulario(FlaskForm):
    nome = StringField("Nome completo", validators=[DataRequired(message="Campo obrigatório")])
    email = StringField("E-mail", validators=[
        DataRequired(message="Campo obrigatório"),
        Email(message="Por favor, insira um e-mail válido.")
    ])
    submit = SubmitField("Enviar")

# Definindo as rotas
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/formulario", methods=["post", "get"])
def formulario():
    form = MeuFormulario()

    if form.validate_on_submit():
        nome = form.nome.data
        email = form.email.data
        flash(f"Cadastro recebido para { nome } e { email }")
        return redirect(url_for("formulario"))
    
    return render_template("formulario.html", form=form)

# Definindo a execução app flask
if __name__ == "__main__":
    app.run(debug=True)