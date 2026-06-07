from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id         = db.Column(db.Integer, primary_key=True)
    nome       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    perfil     = db.Column(db.String(20), default='voluntario')  
    criado_em  = db.Column(db.DateTime, default=datetime.utcnow)

    doacoes = db.relationship('Doacao', backref='registrado_por', lazy=True)

    def set_password(self, senha: str) -> None:
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)

    @property
    def is_admin(self) -> bool:
        return self.perfil == 'admin'

    def __repr__(self) -> str:
        return f'<Usuario {self.email} [{self.perfil}]>'


@login_manager.user_loader
def load_user(user_id: str) -> 'Usuario':
    return db.session.get(Usuario, int(user_id))
