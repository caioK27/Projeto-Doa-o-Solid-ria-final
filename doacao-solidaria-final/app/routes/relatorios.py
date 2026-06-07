from datetime import datetime, timedelta
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from sqlalchemy import func
from app import db
from app.models.doacao import Doacao
from app.models.beneficiario import Beneficiario

relatorios_bp = Blueprint('relatorios', __name__)


@relatorios_bp.route('/')
@login_required
def index():
    por_categoria = (
        db.session.query(Doacao.categoria, func.count(Doacao.id).label('total'))
        .group_by(Doacao.categoria)
        .order_by(func.count(Doacao.id).desc())
        .all()
    )

    por_status = (
        db.session.query(Doacao.status, func.count(Doacao.id).label('total'))
        .group_by(Doacao.status)
        .all()
    )

    top_beneficiarios = (
        db.session.query(Beneficiario.nome, func.count(Doacao.id).label('total'))
        .join(Doacao, Doacao.beneficiario_id == Beneficiario.id)
        .group_by(Beneficiario.nome)
        .order_by(func.count(Doacao.id).desc())
        .limit(5)
        .all()
    )

    seis_meses = datetime.utcnow() - timedelta(days=180)
    doacoes_recentes = Doacao.query.filter(Doacao.data_doacao >= seis_meses).all()

    por_mes_raw: dict = {}
    for d in doacoes_recentes:
        chave_dt = (d.data_doacao.year, d.data_doacao.month)
        por_mes_raw[chave_dt] = por_mes_raw.get(chave_dt, 0) + 1

    por_mes_lista = [
        (f'{m:02d}/{a}', qtd)
        for (a, m), qtd in sorted(por_mes_raw.items())
    ]

    trinta_dias    = datetime.utcnow() - timedelta(days=30)
    total_recentes = Doacao.query.filter(Doacao.data_doacao >= trinta_dias).count()

    return render_template(
        'relatorios/index.html',
        por_categoria=por_categoria,
        por_status=por_status,
        top_beneficiarios=top_beneficiarios,
        por_mes_lista=por_mes_lista,
        total_recentes=total_recentes,
    )


@relatorios_bp.route('/api/categorias')
@login_required
def api_categorias():
    """Retorna doações por categoria em JSON."""
    dados = (
        db.session.query(Doacao.categoria, func.count(Doacao.id))
        .group_by(Doacao.categoria)
        .all()
    )
    return jsonify([{'categoria': c, 'total': t} for c, t in dados])


@relatorios_bp.route('/api/resumo')
@login_required
def api_resumo():
    """Retorna resumo geral do sistema em JSON."""
    return jsonify({
        'total_doacoes':       Doacao.query.count(),
        'pendentes':           Doacao.query.filter_by(status='pendente').count(),
        'entregues':           Doacao.query.filter_by(status='entregue').count(),
        'cancelados':          Doacao.query.filter_by(status='cancelado').count(),
        'total_beneficiarios': Beneficiario.query.filter_by(ativo=True).count(),
    })
