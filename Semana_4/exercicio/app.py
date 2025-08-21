import os
from datetime import date, datetime
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, DateField, ValidationError
from wtforms.validators import DataRequired

# --- Configuração da Aplicação Flask ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# --- Definição do formulário ---
class EventoForm(FlaskForm):
    def validate_data_before_today(self, field):
        if field.data < date.today():
            raise ValidationError("A data do evento não pode ser no passado")
        
    def validate_descricao(self, field):
        if self.tipo_evento.data == "Outro" and not field.data:
            raise ValidationError("Descrição é obrigatória quando o tipo do evento é outro!")
        
    nome_evento = StringField(
        'Nome do evento',
        validators=[DataRequired(message="Campo obrigatório")]
    )
    data_evento = DateField(
        'Data do evento',
        validators=[DataRequired(message="Campo obrigatório"), validate_data_before_today]
    )
    organizador = StringField(
        'Organizador',
        validators=[DataRequired(message="Campo obrigatório!")]
    )
    tipo_evento = SelectField(
        'Tipos do Evento',
        choices=[
            ("Palestra", "Palestra"),
            ("Workshop", "Workshop"),
            ("Meetup", "Meetup"),
            ("Outro", "Outro")
        ],
        validators=[DataRequired()]
    )
    descricao = StringField('Descrição')
        
    enviar = SubmitField("Enviar")
    


# --- Definição objeto para simulação ---
class Evento:
    def __init__(self, nome_evento, data_evento, organizador, tipo_evento, descricao):
        self.nome_evento = nome_evento
        self.data_evento = data_evento
        self.organizador = organizador
        self.tipo_evento = tipo_evento
        self.descricao = descricao


# --- Rotas da Aplicação ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/vazio", methods=["GET", "POST"])
def formulario_vazio():
    form = EventoForm()

    # Resposta ao método POST
    if form.validate_on_submit():
        nome_evento = form.nome_evento.data
        data_evento = form.data_evento.data
        organizador = form.organizador.data
        tipo_evento = form.tipo_evento.data
        descricao = form.descricao.data
        return render_template("sucesso.html", 
                               nome_evento=nome_evento, 
                               data_evento=data_evento, 
                               organizador=organizador,
                               tipo_evento=tipo_evento,
                               descricao=descricao)
    # Resposta ao método GET
    return render_template(
        "formulario.html",
        form=form,
        title="1. Fomulário Vazio"
    )

@app.route("/via-argumentos", methods=["GET", "POST"])
def formulario_via_argumentos():
    form = EventoForm()

    # Resposta ao método POST
    if form.validate_on_submit():
        nome_evento = form.nome_evento.data
        data_evento = form.data_evento.data
        organizador = form.organizador.data
        tipo_evento = form.tipo_evento.data
        descricao = form.descricao.data
        return render_template("sucesso.html", 
                               nome_evento=nome_evento, 
                               data_evento=data_evento, 
                               organizador=organizador,
                               tipo_evento=tipo_evento,
                               descricao=descricao)
    # Resposta ao método GET
    elif not form.is_submitted():
        dados_iniciais = {
            "nome_evento": "Jones da Silva",
            "data_evento": datetime.strptime('Mon Oct 15 2025', '%a %b %d %Y'),
            "organizador": "Esta é uma mensagem preenchida por argumentos.",
            "tipo_evento": "Palestra",
            "descricao": "123"
        }
        form = EventoForm(**dados_iniciais)

    return render_template(
        "formulario.html",
        form=form,
        title="2. Fomulário com Argumentos"
    )

@app.route("/via-objeto", methods=["GET", "POST"])
def formulario_via_objeto():
    form = EventoForm()

    # Resposta ao método POST
    if form.validate_on_submit():
        nome_evento = form.nome_evento.data
        data_evento = form.data_evento.data
        organizador = form.organizador.data
        tipo_evento = form.tipo_evento.data
        descricao = form.descricao.data
        return render_template("sucesso.html", 
                               nome_evento=nome_evento, 
                               data_evento=data_evento, 
                               organizador=organizador,
                               tipo_evento=tipo_evento,
                               descricao=descricao)
    # Resposta ao método GET
    elif not form.is_submitted():
        usuario_mock = Evento(
            nome_evento="Manoel Eventos", 
            data_evento=datetime.strptime('Mon Nov 15 2032', '%a %b %d %Y'), 
            organizador="Manoel Santos",
            tipo_evento="Workshop",
            descricao="descricao"
        )
        form = EventoForm(obj=usuario_mock)

    return render_template(
        "formulario.html",
        form=form,
        title="3. Fomulário preenchido por Objeto"
    )

# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True)