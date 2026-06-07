"""
Blueprint de Beneficiários — CRUD completo.

CORREÇÕES APLICADAS:
  - Bug #5: get_or_404() depreciado substituído por db.get_or_404()
  - Bug #6: int() protegido com try/except em membros
  - Bug #11: validação server-side de campo nome vazio após strip
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models.beneficiario import Beneficiario

beneficiarios_bp = Blueprint('beneficiarios', __name__)


def _parse_membros(valor: str) -> int:
    """
    Converte string para inteiro positivo com fallback 1.
    Bug #6: evita crash com int() direto.
    """
    try:
        m = int(valor)
        return max(1, m)
    except (ValueError, TypeError):
        return 1


@beneficiarios_bp.route('/')
@login_required
def listar():
    apenas_ativos = request.args.get('ativos', '1')
    query = Beneficiario.query

    if apenas_ativos == '1':
        query = query.filter_by(ativo=True)

    beneficiarios = query.order_by(Beneficiario.nome).all()
    return render_template(
        'beneficiarios/listar.html',
        beneficiarios=beneficiarios,
        apenas_ativos=apenas_ativos,
    )


@beneficiarios_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        # FIX #11: validação server-side de campo obrigatório
        if not nome:
            flash('O nome do beneficiário não pode estar vazio.', 'danger')
            return render_template('beneficiarios/form.html')

        b = Beneficiario(
            nome        = nome,
            regiao      = request.form.get('regiao', '').strip(),
            membros     = _parse_membros(request.form.get('membros', '1')),
            necessidade = request.form.get('necessidade', '').strip(),
            ativo       = True,
        )
        db.session.add(b)
        db.session.commit()
        flash(f'{b.nome} cadastrado com sucesso!', 'success')
        return redirect(url_for('beneficiarios.listar'))

    return render_template('beneficiarios/form.html')


@beneficiarios_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    # FIX #5: db.get_or_404() substitui o depreciado query.get_or_404()
    b = db.get_or_404(Beneficiario, id)

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        # FIX #11: validação server-side
        if not nome:
            flash('O nome do beneficiário não pode estar vazio.', 'danger')
            return render_template('beneficiarios/form.html', beneficiario=b)

        b.nome        = nome
        b.regiao      = request.form.get('regiao', '').strip()
        b.membros     = _parse_membros(request.form.get('membros', '1'))
        b.necessidade = request.form.get('necessidade', '').strip()
        b.ativo       = 'ativo' in request.form

        db.session.commit()
        flash(f'{b.nome} atualizado com sucesso!', 'success')
        return redirect(url_for('beneficiarios.listar'))

    return render_template('beneficiarios/form.html', beneficiario=b)
