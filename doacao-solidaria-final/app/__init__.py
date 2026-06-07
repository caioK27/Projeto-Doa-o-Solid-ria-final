"""
Factory da aplicação Flask.
Inicializa extensões, blueprints e popula dados iniciais.

CORREÇÕES APLICADAS:
  - Bug #1: test_config recebido ANTES do seed (fixtures de teste funcionam)
  - Bug #9: SECRET_KEY lida de variável de ambiente com fallback de desenvolvimento
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(test_config=None):
    """
    Cria e configura a aplicação Flask.

    Args:
        test_config (dict, opcional): Configurações que sobrescrevem os
            padrões antes de qualquer inicialização. Use em testes para
            injetar 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'.
    """
    app = Flask(__name__)

    # ── Configurações padrão ─────────────────────────────────────────────────
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY', 'dev-key-insegura-trocar-em-producao'
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doacoes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ── FIX #1: test_config aplicado ANTES do seed e do db.create_all ────────
    if test_config:
        app.config.update(test_config)

    # ── Extensões ────────────────────────────────────────────────────────────
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Faça login para acessar esta página.'
    login_manager.login_message_category = 'info'

    # ── Blueprints ───────────────────────────────────────────────────────────
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.doacoes import doacoes_bp
    from app.routes.beneficiarios import beneficiarios_bp
    from app.routes.relatorios import relatorios_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,          url_prefix='/auth')
    app.register_blueprint(doacoes_bp,       url_prefix='/doacoes')
    app.register_blueprint(beneficiarios_bp, url_prefix='/beneficiarios')
    app.register_blueprint(relatorios_bp,    url_prefix='/relatorios')

    # ── Banco de dados + Dados iniciais ──────────────────────────────────────
    with app.app_context():
        db.create_all()
        _seed_dados_iniciais()

    return app


def _seed_dados_iniciais():
    """Popula o banco com dados de demonstração na primeira execução."""
    from app.models.usuario import Usuario
    from app.models.doacao import Doacao
    from app.models.beneficiario import Beneficiario
    from datetime import datetime, timedelta
    import random

    if Usuario.query.first():
        return  # Já foi populado anteriormente

    # Usuários
    admin = Usuario(nome='Administrador', email='admin@solidaria.org', perfil='admin')
    admin.set_password('admin123')

    voluntario = Usuario(nome='Maria Silva', email='maria@solidaria.org', perfil='voluntario')
    voluntario.set_password('senha123')

    db.session.add_all([admin, voluntario])
    db.session.commit()  # commit aqui garante admin.id disponível abaixo

    # Beneficiários
    dados_beneficiarios = [
        ('Família Souza',    'Zona Norte',      5, 'Alimentos e Roupas'),
        ('Família Oliveira', 'Zona Sul',        3, 'Alimentos'),
        ('Dona Ana Costa',   'Centro',          1, 'Medicamentos'),
        ('Família Pereira',  'Zona Leste',      7, 'Alimentos e Roupas'),
        ('Família Santos',   'Zona Oeste',      4, 'Alimentos'),
        ('Sr. João Lima',    'Periferia Norte', 2, 'Alimentos e Medicamentos'),
    ]
    beneficiarios = []
    for nome, regiao, membros, necessidade in dados_beneficiarios:
        b = Beneficiario(nome=nome, regiao=regiao, membros=membros,
                         necessidade=necessidade, ativo=True)
        db.session.add(b)
        beneficiarios.append(b)
    db.session.commit()  # commit aqui garante b.id disponível abaixo

    # Doações de exemplo
    categorias = ['Alimentos', 'Roupas', 'Medicamentos', 'Higiene', 'Brinquedos']
    doadores = [
        'Ana Paula Ferreira', 'Carlos Mendes', 'Empresa XYZ Ltda.',
        'Igreja Nossa Sra. Aparecida', 'Escola Estadual Dom Pedro',
        'Condomínio Verde Vida',
    ]
    for i in range(20):
        data = datetime.now() - timedelta(days=random.randint(0, 90))
        d = Doacao(
            doador=random.choice(doadores),
            categoria=random.choice(categorias),
            quantidade=random.randint(1, 50),
            descricao=f'Doação de exemplo #{i + 1}',
            data_doacao=data,
            beneficiario_id=random.choice(beneficiarios).id,
            usuario_id=admin.id,
            status='entregue' if random.random() > 0.3 else 'pendente',
        )
        db.session.add(d)
    db.session.commit()
