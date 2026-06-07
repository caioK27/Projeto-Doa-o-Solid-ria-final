"""
Model de Doação.
Representa cada item doado: categoria, quantidade, doador e status de entrega.
"""

from datetime import datetime
from app import db


class Doacao(db.Model):
    __tablename__ = 'doacoes'

    id             = db.Column(db.Integer, primary_key=True)
    doador         = db.Column(db.String(120), nullable=False)
    categoria      = db.Column(db.String(50),  nullable=False)
    quantidade     = db.Column(db.Integer,     nullable=False)
    descricao      = db.Column(db.Text,        default='')
    data_doacao    = db.Column(db.DateTime,    default=datetime.utcnow)
    status         = db.Column(db.String(20),  default='pendente')  # pendente | entregue | cancelado
    criado_em      = db.Column(db.DateTime,    default=datetime.utcnow)

    # Chaves estrangeiras
    beneficiario_id = db.Column(db.Integer, db.ForeignKey('beneficiarios.id'), nullable=True)
    usuario_id      = db.Column(db.Integer, db.ForeignKey('usuarios.id'),      nullable=False)

    def __repr__(self) -> str:
        return f'<Doacao #{self.id} | {self.doador} | {self.categoria} | {self.status}>'
