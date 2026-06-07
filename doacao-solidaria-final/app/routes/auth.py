"""
Blueprint de autenticação — Login e Logout.

CORREÇÕES APLICADAS:
  - Bug #7: parâmetro 'next' validado para evitar open redirect
"""

from urllib.parse import urlparse, urljoin
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)


def _url_segura(url: str) -> bool:
    """
    Verifica se a URL de redirecionamento aponta para o próprio host.
    Previne open redirect (Bug #7).
    """
    if not url:
        return False
    ref = urlparse(urljoin(request.host_url, url))
    host = urlparse(request.host_url)
    return ref.scheme in ('http', 'https') and ref.netloc == host.netloc


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        # Normaliza e-mail: strip + lower para evitar falha de login por caixa
        email  = request.form.get('email', '').strip().lower()
        senha  = request.form.get('senha', '')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_password(senha):
            login_user(usuario, remember=True)
            # FIX #7: valida 'next' antes de redirecionar
            proximo = request.args.get('next', '')
            return redirect(proximo if _url_segura(proximo) else url_for('main.index'))

        flash('E-mail ou senha incorretos. Tente novamente.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))
