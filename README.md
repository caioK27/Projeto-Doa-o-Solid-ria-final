# 🤝 Doação Solidária

> **Projeto de Extensão — Web Back-End com Python/Flask**

Sistema web para gestão de doações destinadas a comunidades em situação de vulnerabilidade social.

---

## 📌 Tema do Projeto

**Sistema de Gestão de Doações para Comunidades Vulneráveis**

Desenvolvido como projeto de extensão universitária aplicando conceitos de desenvolvimento
web back-end com Python, banco de dados, autenticação e boas práticas de engenharia de software.

---

## 🚨 Problema Enfrentado

Organizações voluntárias e ONGs que distribuem doações para comunidades carentes controlam
tudo em cadernos, planilhas ou grupos de WhatsApp. Isso gera:

- ❌ Perda de informação e sem histórico confiável
- ❌ Famílias atendidas duas vezes enquanto outras ficam sem nada
- ❌ Impossibilidade de prestar contas aos doadores
- ❌ Voluntários trabalhando sem visibilidade coletiva

**Solução:** Uma aplicação web centralizada que resolve todos esses pontos.

---

## ✨ Funcionalidades

- 📊 **Dashboard** — totais, últimas doações e distribuição por categoria
- 📦 **Doações** — registrar, editar, filtrar por status/categoria e excluir
- 👥 **Beneficiários** — cadastrar famílias por região, membros e necessidades
- 📈 **Relatórios** — métricas, top beneficiários, atividade por mês
- 🔌 **API JSON** — endpoints `/relatorios/api/resumo` e `/relatorios/api/categorias`
- 🔐 **Autenticação** — login seguro com perfis Admin e Voluntário

---

## 🖥️ Como Rodar no VS Code

### Pré-requisitos
- [Python 3.11+](https://www.python.org/downloads/) instalado
  - ⚠️ Durante a instalação, marque a opção **"Add Python to PATH"**
- [VS Code](https://code.visualstudio.com/) instalado

### Passo a passo

**1.** Extraia o ZIP e abra a pasta no VS Code:
```
File → Open Folder → selecione a pasta doacao-solidaria-corrigido
```

**2.** Abra o terminal do VS Code:
```
Pressione:  Ctrl + '
```

**3.** No terminal, execute os comandos abaixo **um por vez**:

```bash
python -m venv venv
```
```bash
venv\Scripts\activate
```
```bash
pip install -r requirements.txt
```
```bash
python run.py
```

**4.** Abra o navegador e acesse:
```
http://127.0.0.1:5000
```

**5.** Faça login com as credenciais abaixo.

---

## 🔑 Login de Demonstração

| Perfil | E-mail | Senha |
|---|---|---|
| Administrador | admin@solidaria.org | admin123 |
| Voluntário | maria@solidaria.org | senha123 |

> O banco de dados é criado automaticamente com dados de exemplo na primeira execução.

---

## ❗ Solução de Problemas Comuns

### `python` não foi encontrado
O Python não está instalado ou não foi adicionado ao PATH.
Baixe em **https://www.python.org/downloads/** e marque **"Add Python to PATH"** na instalação.

### Erro de permissão no PowerShell ao ativar o venv
Execute este comando antes de ativar:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Digite `S` quando perguntado e pressione Enter. Depois tente `venv\Scripts\activate` novamente.

### Erro com SQLAlchemy / Python 3.14
Se você tiver Python 3.14, substitua o conteúdo do `requirements.txt` por:
```
Flask==3.1.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.1.3
SQLAlchemy==2.0.36
Jinja2==3.1.4
click==8.1.7
itsdangerous==2.2.0
MarkupSafe==2.1.5
pytest==8.2.2
```
Depois rode `pip install -r requirements.txt` novamente.

### Para parar o servidor
Pressione `Ctrl + C` no terminal.

### Da segunda vez em diante
Você só precisa rodar:
```bash
venv\Scripts\activate
python run.py
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3.11+ | Linguagem principal |
| Flask 3.x | Framework web back-end |
| Flask-SQLAlchemy | ORM e banco de dados |
| Flask-Login | Autenticação e sessões |
| SQLite | Banco de dados (desenvolvimento) |
| Werkzeug | Hash de senhas |
| Jinja2 | Templates HTML dinâmicos |
| pytest | Testes automáticos |
| GitHub Actions | CI/CD automático |

---

## 🧪 Rodando os Testes

```bash
pytest tests/ -v
```

---

## 📁 Estrutura do Projeto

```
doacao-solidaria-corrigido/
│
├── run.py                        ← Ponto de entrada
├── requirements.txt              ← Dependências Python
├── README.md                     ← Este arquivo
├── .gitignore
│
├── .vscode/
│   ├── launch.json               ← Debug com F5
│   └── settings.json             ← Configurações do editor
│
├── .github/
│   └── workflows/ci.yml          ← Testes automáticos no GitHub
│
├── app/
│   ├── __init__.py               ← Factory Flask
│   ├── models/
│   │   ├── usuario.py            ← Model de usuários
│   │   ├── doacao.py             ← Model de doações
│   │   └── beneficiario.py       ← Model de beneficiários
│   ├── routes/
│   │   ├── auth.py               ← Login / Logout
│   │   ├── main.py               ← Dashboard
│   │   ├── doacoes.py            ← CRUD de doações
│   │   ├── beneficiarios.py      ← CRUD de beneficiários
│   │   └── relatorios.py         ← Relatórios + API JSON
│   └── templates/
│       ├── base.html             ← Layout base
│       ├── index.html            ← Dashboard
│       ├── auth/login.html
│       ├── doacoes/
│       ├── beneficiarios/
│       └── relatorios/
│
└── tests/
    └── test_app.py               ← 20 testes automáticos
```

---

## 🌐 Publicar no GitHub

```bash
git init
git add .
git commit -m "feat: projeto inicial - Doacao Solidaria"
git remote add origin https://github.com/SEU-USUARIO/doacao-solidaria.git
git push -u origin main
```

O **GitHub Actions** roda os testes automaticamente a cada `push`.

---

## 🌱 Evoluções Futuras

- [ ] Exportação de relatórios em PDF / CSV
- [ ] Notificações por e-mail ao confirmar entrega
- [ ] Mapa com localização geográfica dos beneficiários
- [ ] API REST para aplicativo mobile
- [ ] Migração para PostgreSQL (produção)
- [ ] Proteção CSRF com Flask-WTF

---

*Projeto de Extensão — Disciplina de Desenvolvimento Web Back-End com Python*
