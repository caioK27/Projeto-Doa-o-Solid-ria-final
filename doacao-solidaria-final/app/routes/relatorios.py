"""
Blueprint de Relatórios — Métricas e API JSON.

CORREÇÕES APLICADAS:
  - Bug #4: por_mes_lista ordenado por data real, não por string lexicográfica
"""

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
    # Doações por categoria
    por_categoria = (
        db.session.query(Doacao.categoria, func.count(Doacao.id).label('total'))
        .group_by(Doacao.categoria)
        .order_by(func.count(Doacao.id).desc())
        .all()
    )

    # Doações por status
    por_status = (
        db.session.query(Doacao.status, func.count(Doacao.id).label('total'))
        .group_by(Doacao.status)
        .all()
    )

    # Top 5 beneficiários com mais doações recebidas
    top_beneficiarios = (
        db.session.query(Beneficiario.nome, func.count(Doacao.id).label('total'))
        .join(Doacao, Doacao.beneficiario_id == Beneficiario.id)
        .group_by(Beneficiario.nome)
        .order_by(func.count(Doacao.id).desc())
        .limit(5)
        .all()
    )

    # Doações por mês (últimos 6 meses)
    seis_meses = datetime.utcnow() - timedelta(days=180)
    doacoes_recentes = Doacao.query.filter(Doacao.data_doacao >= seis_meses).all()

    # FIX #4: chave de agrupamento como objeto date para ordenação cronológica correta.
    # Antes era '%m/%Y' (string), que ordena '01/2025' antes de '12/2024' (ERRADO).
    # Agora agrupamos por (ano, mês) como ints, garantindo ordem cronológica.
    por_mes_raw: dict = {}
    for d in doacoes_recentes:
        chave_dt = (d.data_doacao.year, d.data_doacao.month)
        por_mes_raw[chave_dt] = por_mes_raw.get(chave_dt, 0) + 1

    # Ordena cronologicamente e converte para exibição 'MM/AAAA'
    por_mes_lista = [
        (f'{m:02d}/{a}', qtd)
        for (a, m), qtd in sorted(por_mes_raw.items())
    ]

    # Doações últimos 30 dias
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


# ── API JSON ─────────────────────────────────────────────────────────────────

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
