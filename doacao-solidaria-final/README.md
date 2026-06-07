# 🤝 Doação Solidária

> **Projeto de Extensão — Web Back-End com Python/Flask**

Sistema web para gestão de doações destinadas a comunidades em situação de vulnerabilidade social.

---

## 🚀 Como Rodar

```bash
# 1. Clone o repositório
git clone https://github.com/SEU-USUARIO/doacao-solidaria.git
cd doacao-solidaria

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute
python run.py
```

Acesse: **http://127.0.0.1:5000**

### Login de demonstração
| Perfil | E-mail | Senha |
|---|---|---|
| Admin | admin@solidaria.org | admin123 |
| Voluntário | maria@solidaria.org | senha123 |

---

## 🛠️ Tecnologias

- Python 3.11 + Flask 3.x
- Flask-SQLAlchemy + SQLite
- Flask-Login (autenticação)
- Jinja2 (templates)
- pytest (testes)
- GitHub Actions (CI)

---

## 🧪 Testes

```bash
pytest tests/ -v
```

---

## 📁 Estrutura

```
doacao-solidaria/
├── run.py
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── models/         (usuario, doacao, beneficiario)
│   ├── routes/         (auth, main, doacoes, beneficiarios, relatorios)
│   └── templates/      (base, login, dashboard, CRUDs, relatorios)
└── tests/
    └── test_app.py
```

---

## ✨ Funcionalidades

- Dashboard com métricas
- CRUD completo de doações (registrar, editar, filtrar, excluir)
- CRUD completo de beneficiários
- Relatórios com gráficos de barra
- API JSON (`/relatorios/api/resumo` e `/relatorios/api/categorias`)
- Autenticação com perfis Admin e Voluntário

---

*Projeto de Extensão — Disciplina de Desenvolvimento Web Back-End com Python*
