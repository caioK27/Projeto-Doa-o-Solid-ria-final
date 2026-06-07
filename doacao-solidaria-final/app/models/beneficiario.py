"""
Model de Beneficiário.
Representa famílias ou indivíduos em situação de vulnerabilidade social.
"""

from datetime import datetime
from app import db


class Beneficiario(db.Model):
    __tablename__ = 'beneficiarios'

    id          = db.Column(db.Integer, primary_key=True)
    nome        = db.Column(db.String(120), nullable=False)
    regiao      = db.Column(db.String(80),  default='')
    membros     = db.Column(db.Integer,     default=1)
    necessidade = db.Column(db.String(200), default='')
    ativo       = db.Column(db.Boolean,     default=True)
    criado_em   = db.Column(db.DateTime,    default=datetime.utcnow)

    # Relacionamentos
    doacoes = db.relationship('Doacao', backref='beneficiario', lazy=True)

    @property
    def total_doacoes(self) -> int:
        return len(self.doacoes)

    @property
    def doacoes_entregues(self) -> int:
        return sum(1 for d in self.doacoes if d.status == 'entregue')

    def __repr__(self) -> str:
        return f'<Beneficiario {self.nome} | {self.regiao}>'
