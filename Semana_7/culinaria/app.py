# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# -----------------------------------------------------------------------------
# CONFIGURAÇÃO DA APLICAÇÃO E BANCO DE DADOS
# -----------------------------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta-receitas'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------------------------------------------------------------
# MODELOS (DENTRO DO APP.PY)
# -----------------------------------------------------------------------------
# Tabela de associação M:M (Receita ↔ Ingrediente)
receita_ingredientes = db.Table('receita_ingredientes',
    db.Column('receita_id', db.Integer, db.ForeignKey('receita.id'), primary_key=True),
    db.Column('ingrediente_id', db.Integer, db.ForeignKey('ingrediente.id'), primary_key=True)
)

class Chef(db.Model):
    __tablename__ = 'chef'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    
    # Relacionamento 1:1 com PerfilChef
    perfil = db.relationship('PerfilChef', uselist=False, back_populates='chef', cascade='all, delete-orphan')
    # Relacionamento 1:M com Receita
    receitas = db.relationship('Receita', back_populates='chef', cascade='all, delete-orphan')

class PerfilChef(db.Model):
    __tablename__ = 'perfil_chef'
    id = db.Column(db.Integer, primary_key=True)
    especialidade = db.Column(db.String(100), nullable=False)
    anos_experiencia = db.Column(db.Integer, nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef.id'), unique=True, nullable=False)
    
    chef = db.relationship('Chef', back_populates='perfil')

class Receita(db.Model):
    __tablename__ = 'receita'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    instrucoes = db.Column(db.Text, nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef.id'), nullable=False)
    
    chef = db.relationship('Chef', back_populates='receitas')
    ingredientes = db.relationship('Ingrediente', secondary=receita_ingredientes, back_populates='receitas')

class Ingrediente(db.Model):
    __tablename__ = 'ingrediente'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    
    receitas = db.relationship('Receita', secondary=receita_ingredientes, back_populates='ingredientes')

# -----------------------------------------------------------------------------
# ROTAS DA APLICAÇÃO
# -----------------------------------------------------------------------------
@app.route('/')
def index():
    receitas = Receita.query.all()
    return render_template('index.html', receitas=receitas)

@app.route('/receita/nova', methods=['GET', 'POST'])
def nova_receita():
    if request.method == 'POST':
        titulo = request.form['titulo']
        instrucoes = request.form['instrucoes']
        chef_id = request.form['chef_id']
        ingredientes_str = request.form['ingredientes']
        
        chef = Chef.query.get(chef_id)
        if not chef:
            flash("Chef não encontrado!", "danger")
            return redirect(url_for('nova_receita'))
        
        nova_receita = Receita(titulo=titulo, instrucoes=instrucoes, chef=chef)
        
        # Processa ingredientes (cria novos se não existirem)
        for nome in [n.strip() for n in ingredientes_str.split(',') if n.strip()]:
            ingrediente = Ingrediente.query.filter_by(nome=nome).first()
            if not ingrediente:
                ingrediente = Ingrediente(nome=nome)
                db.session.add(ingrediente)
            nova_receita.ingredientes.append(ingrediente)
        
        db.session.add(nova_receita)
        db.session.commit()
        flash("Receita criada com sucesso!", "success")
        return redirect(url_for('index'))
    
    chefs = Chef.query.all()
    return render_template('criar_receita.html', chefs=chefs)

@app.route('/chef/<int:chef_id>')
def detalhes_chef(chef_id):
    chef = Chef.query.get_or_404(chef_id)
    return render_template('detalhes_chef.html', chef=chef)

# Bônus: Busca por ingrediente
@app.route('/ingrediente/<string:nome_ingrediente>')
def buscar_ingrediente(nome_ingrediente):
    ingrediente = Ingrediente.query.filter_by(nome=nome_ingrediente).first_or_404()
    return render_template('index.html', receitas=ingrediente.receitas, titulo_busca=nome_ingrediente)

# -----------------------------------------------------------------------------
# INICIALIZAÇÃO (CRIA TABELAS E DADOS INICIAIS)
# -----------------------------------------------------------------------------
@app.before_first_request
def setup():
    db.create_all()
    # Dados iniciais para testes
    if not Chef.query.first():
        chef1 = Chef(nome="Gordon Ramsay")
        chef2 = Chef(nome="Érick Jacquin")
        chef3 = Chef(nome="Bela Gil")
        perfil1 = PerfilChef(especialidade="Culinária Francesa", anos_experiencia=20, chef=chef1)
        perfil2 = PerfilChef(especialidade="Culinária Franco-Brasileira", anos_experiencia=44, chef=chef2)
        perfil3 = PerfilChef(especialidade="Culinária Vegana", anos_experiencia=19, chef=chef3)
        db.session.add_all([chef1, perfil1])
        db.session.add_all([chef2, perfil2])
        db.session.add_all([chef3, perfil3])
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=5002)