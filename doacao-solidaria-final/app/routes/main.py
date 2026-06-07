"""
Blueprint principal — Dashboard com métricas gerais.
"""

from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func
from app import db
from app.models.doacao import Doacao
from app.models.beneficiario import Beneficiario
from app.models.usuario import Usuario

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def index():
    # ── Totais ───────────────────────────────────────────────────────────────
    total_doacoes      = Doacao.query.count()
    total_beneficiarios = Beneficiario.query.filter_by(ativo=True).count()
    total_voluntarios  = Usuario.query.count()
    pendentes          = Doacao.query.filter_by(status='pendente').count()
    entregues          = Doacao.query.filter_by(status='entregue').count()
    cancelados         = Doacao.query.filter_by(status='cancelado').count()

    # ── Doações por categoria ────────────────────────────────────────────────
    por_categoria = (
        db.session.query(Doacao.categoria, func.count(Doacao.id).label('total'))
        .group_by(Doacao.categoria)
        .order_by(func.count(Doacao.id).desc())
        .all()
    )

    # ── Últimas 6 doações ────────────────────────────────────────────────────
    ultimas = Doacao.query.order_by(Doacao.criado_em.desc()).limit(6).all()

    return render_template(
        'index.html',
        total_doacoes=total_doacoes,
        total_beneficiarios=total_beneficiarios,
        total_voluntarios=total_voluntarios,
        pendentes=pendentes,
        entregues=entregues,
        cancelados=cancelados,
        por_categoria=por_categoria,
        ultimas=ultimas,
    )
