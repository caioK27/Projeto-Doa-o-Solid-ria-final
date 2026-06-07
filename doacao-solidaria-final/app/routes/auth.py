from urllib.parse import urlparse, urljoin
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)


def _url_segura(url: str) -> bool:
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
        email  = request.form.get('email', '').strip().lower()
        senha  = request.form.get('senha', '')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_password(senha):
            login_user(usuario, remember=True)
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
