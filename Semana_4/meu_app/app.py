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


# Exemplo 1: Populando o formulário via argumentos diretos
@app.route('/formulario/preenchido-args', methods=['GET', 'POST'])
def formulario_com_argumentos():
    """
    Demonstra como popular o formulário passando os valores como argumentos
    na sua instanciação.
    """
    form = MeuFormulario(nome="Fulano de Tal", email="fulano@exemplo.com")
    
    if form.validate_on_submit():
        flash(f'Dados de "{form.nome.data}" atualizados com sucesso!', 'success')
        return redirect(url_for('formulario_com_argumentos'))
        
    return render_template('formulario.html', form=form)

# Exemplo 2: Populando o formulário com um objeto
@app.route('/formulario/preenchido-obj', methods=['GET', 'POST'])
def formulario_com_objeto():
    """
    Demonstra como popular o formulário a partir de um objeto,
    simulando dados vindos de um banco de dados.
    """
    class UsuarioMock:
        def __init__(self, nome, email):
            self.nome = nome
            self.email = email
            
    usuario_do_banco = UsuarioMock(nome="Ciclano da Silva", email="ciclano@banco.com")

    form = MeuFormulario(obj=usuario_do_banco)
    
    if form.validate_on_submit():
        flash(f'Dados de "{form.nome.data}" atualizados com sucesso!', 'success')
        return redirect(url_for('formulario_com_objeto'))
        
    return render_template('formulario.html', form=form)

# Definindo a execução app flask
if __name__ == "__main__":
    app.run(debug=True)