"""
Blueprint de Doações — CRUD completo.

CORREÇÕES APLICADAS:
  - Bug #5: get_or_404() depreciado substituído por db.get_or_404()
  - Bug #6: int() protegido com try/except em quantidade
  - Bug #8: beneficiario_id convertido explicitamente para int
  - Bug #11: validação server-side de campo doador vazio após strip
  - Bug #12: status validado contra STATUS_OPCOES antes de salvar
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.doacao import Doacao
from app.models.beneficiario import Beneficiario

doacoes_bp = Blueprint('doacoes', __name__)

CATEGORIAS    = ['Alimentos', 'Roupas', 'Medicamentos', 'Higiene', 'Brinquedos', 'Outros']
STATUS_OPCOES = ['pendente', 'entregue', 'cancelado']


def _parse_quantidade(valor: str) -> int | None:
    """
    Converte string para inteiro positivo.
    Retorna None se inválido (Bug #6).
    """
    try:
        q = int(valor)
        if q < 1:
            raise ValueError
        return q
    except (ValueError, TypeError):
        return None


def _parse_beneficiario_id(valor: str) -> int | None:
    """
    Converte string do formulário para int ou None.
    Bug #8: garantir que o tipo é int, não string.
    """
    if not valor or not valor.strip():
        return None
    try:
        return int(valor)
    except (ValueError, TypeError):
        return None


@doacoes_bp.route('/')
@login_required
def listar():
    status    = request.args.get('status', '')
    categoria = request.args.get('categoria', '')

    query = Doacao.query

    if status:
        query = query.filter_by(status=status)
    if categoria:
        query = query.filter_by(categoria=categoria)

    doacoes = query.order_by(Doacao.criado_em.desc()).all()

    return render_template(
        'doacoes/listar.html',
        doacoes=doacoes,
        categorias=CATEGORIAS,
        status_opcoes=STATUS_OPCOES,
    )


@doacoes_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova():
    beneficiarios = Beneficiario.query.filter_by(ativo=True).order_by(Beneficiario.nome).all()

    if request.method == 'POST':
        doador = request.form.get('doador', '').strip()
        # FIX #11: validação server-side de campo obrigatório
        if not doador:
            flash('O nome do doador não pode estar vazio.', 'danger')
            return render_template('doacoes/form.html',
                                   beneficiarios=beneficiarios,
                                   categorias=CATEGORIAS,
                                   status_opcoes=STATUS_OPCOES)

        # FIX #6: parse seguro de quantidade
        quantidade = _parse_quantidade(request.form.get('quantidade', ''))
        if quantidade is None:
            flash('Quantidade inválida. Informe um número inteiro maior que zero.', 'danger')
            return render_template('doacoes/form.html',
                                   beneficiarios=beneficiarios,
                                   categorias=CATEGORIAS,
                                   status_opcoes=STATUS_OPCOES)

        # FIX #8: beneficiario_id como int ou None
        beneficiario_id = _parse_beneficiario_id(request.form.get('beneficiario_id', ''))

        doacao = Doacao(
            doador          = doador,
            categoria       = request.form.get('categoria', CATEGORIAS[0]),
            quantidade      = quantidade,
            descricao       = request.form.get('descricao', '').strip(),
            beneficiario_id = beneficiario_id,
            usuario_id      = current_user.id,
            status          = 'pendente',
        )
        db.session.add(doacao)
        db.session.commit()
        flash(f'Doação de {doacao.doador} registrada com sucesso!', 'success')
        return redirect(url_for('doacoes.listar'))

    return render_template(
        'doacoes/form.html',
        beneficiarios=beneficiarios,
        categorias=CATEGORIAS,
        status_opcoes=STATUS_OPCOES,
    )


@doacoes_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    # FIX #5: db.get_or_404() substitui o depreciado query.get_or_404()
    doacao        = db.get_or_404(Doacao, id)
    beneficiarios = Beneficiario.query.filter_by(ativo=True).order_by(Beneficiario.nome).all()

    if request.method == 'POST':
        doador = request.form.get('doador', '').strip()
        # FIX #11: validação server-side
        if not doador:
            flash('O nome do doador não pode estar vazio.', 'danger')
            return render_template('doacoes/form.html',
                                   doacao=doacao,
                                   beneficiarios=beneficiarios,
                                   categorias=CATEGORIAS,
                                   status_opcoes=STATUS_OPCOES)

        # FIX #6: parse seguro de quantidade
        quantidade = _parse_quantidade(request.form.get('quantidade', ''))
        if quantidade is None:
            flash('Quantidade inválida. Informe um número inteiro maior que zero.', 'danger')
            return render_template('doacoes/form.html',
                                   doacao=doacao,
                                   beneficiarios=beneficiarios,
                                   categorias=CATEGORIAS,
                                   status_opcoes=STATUS_OPCOES)

        # FIX #12: status validado antes de salvar
        novo_status = request.form.get('status', '')
        if novo_status not in STATUS_OPCOES:
            abort(400)

        # FIX #8: beneficiario_id como int ou None
        beneficiario_id = _parse_beneficiario_id(request.form.get('beneficiario_id', ''))

        doacao.doador          = doador
        doacao.categoria       = request.form.get('categoria', CATEGORIAS[0])
        doacao.quantidade      = quantidade
        doacao.descricao       = request.form.get('descricao', '').strip()
        doacao.beneficiario_id = beneficiario_id
        doacao.status          = novo_status

        db.session.commit()
        flash('Doação atualizada com sucesso!', 'success')
        return redirect(url_for('doacoes.listar'))

    return render_template(
        'doacoes/form.html',
        doacao=doacao,
        beneficiarios=beneficiarios,
        categorias=CATEGORIAS,
        status_opcoes=STATUS_OPCOES,
    )


@doacoes_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    # FIX #5: db.get_or_404() substitui o depreciado query.get_or_404()
    doacao = db.get_or_404(Doacao, id)
    nome_doador = doacao.doador
    db.session.delete(doacao)
    db.session.commit()
    flash(f'Doação de {nome_doador} removida.', 'info')
    return redirect(url_for('doacoes.listar'))
