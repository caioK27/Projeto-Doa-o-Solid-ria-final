import pytest
from app import create_app, db as _db
from app.models.usuario import Usuario

TEST_CONFIG = {
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    'WTF_CSRF_ENABLED': False,
    'SECRET_KEY': 'test-secret-key',
    'LOGIN_DISABLED': False,
}



@pytest.fixture(scope='session')
def app():
    _app = create_app(test_config=TEST_CONFIG)
    with _app.app_context():
        yield _app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def logado(client):
    r = client.post('/auth/login', data={
        'email': 'admin@solidaria.org',
        'senha': 'admin123',
    }, follow_redirects=True)
    assert r.status_code == 200, "Falha no login do admin — verifique o seed"
    return client



class TestAuth:

    def test_pagina_login_ok(self, client):
        r = client.get('/auth/login')
        assert r.status_code == 200
        assert 'login' in r.data.decode().lower()

    def test_dashboard_redireciona_sem_login(self, client):
        r = client.get('/')
        assert r.status_code == 302
        assert 'login' in r.headers['Location'].lower()

    def test_login_credenciais_erradas(self, client):
        r = client.post('/auth/login', data={
            'email': 'ninguem@test.com',
            'senha': 'senhaerrada',
        }, follow_redirects=True)
        assert r.status_code == 200
        assert 'incorretos' in r.data.decode().lower()

    def test_login_admin_valido(self, client):
        r = client.post('/auth/login', data={
            'email': 'admin@solidaria.org',
            'senha': 'admin123',
        }, follow_redirects=True)
        assert r.status_code == 200

    def test_login_voluntario_valido(self, client):
        r = client.post('/auth/login', data={
            'email': 'maria@solidaria.org',
            'senha': 'senha123',
        }, follow_redirects=True)
        assert r.status_code == 200

    def test_logout(self, logado):
        r = logado.get('/auth/logout', follow_redirects=False)
        assert r.status_code == 302

    def test_next_seguro_rejeitado(self, client):
        r = client.post(
            '/auth/login?next=https://site-malicioso.com',
            data={'email': 'admin@solidaria.org', 'senha': 'admin123'},
            follow_redirects=False,
        )
        location = r.headers.get('Location', '')
        assert 'site-malicioso.com' not in location



class TestDashboard:

    def test_dashboard_autenticado(self, logado):
        r = logado.get('/')
        assert r.status_code == 200
        assert 'Dashboard' in r.data.decode()



class TestDoacoes:

    def test_listar_doacoes(self, logado):
        r = logado.get('/doacoes/')
        assert r.status_code == 200

    def test_form_nova_doacao(self, logado):
        r = logado.get('/doacoes/nova')
        assert r.status_code == 200

    def test_registrar_doacao(self, logado):
        r = logado.post('/doacoes/nova', data={
            'doador':          'Empresa Teste LTDA',
            'categoria':       'Alimentos',
            'quantidade':      '20',
            'descricao':       'Caixas de macarrão',
            'beneficiario_id': '',
        }, follow_redirects=True)
        assert r.status_code == 200
        assert 'Empresa Teste LTDA' in r.data.decode()

    def test_quantidade_invalida_retorna_erro(self, logado):
        r = logado.post('/doacoes/nova', data={
            'doador':     'Teste',
            'categoria':  'Alimentos',
            'quantidade': 'abc',
        }, follow_redirects=True)
        assert r.status_code == 200
        assert 'inv' in r.data.decode().lower()  

    def test_doador_vazio_retorna_erro(self, logado):
        r = logado.post('/doacoes/nova', data={
            'doador':     '   ',
            'categoria':  'Alimentos',
            'quantidade': '5',
        }, follow_redirects=True)
        assert r.status_code == 200
        assert 'vazio' in r.data.decode().lower()

    def test_filtrar_por_status(self, logado):
        r = logado.get('/doacoes/?status=pendente')
        assert r.status_code == 200

    def test_filtrar_por_categoria(self, logado):
        r = logado.get('/doacoes/?categoria=Alimentos')
        assert r.status_code == 200



class TestBeneficiarios:

    def test_listar_beneficiarios(self, logado):
        r = logado.get('/beneficiarios/')
        assert r.status_code == 200

    def test_form_novo_beneficiario(self, logado):
        r = logado.get('/beneficiarios/novo')
        assert r.status_code == 200

    def test_cadastrar_beneficiario(self, logado):
        r = logado.post('/beneficiarios/novo', data={
            'nome':        'Família Teste da Silva',
            'regiao':      'Zona Sul',
            'membros':     '4',
            'necessidade': 'Alimentos e roupas',
        }, follow_redirects=True)
        assert r.status_code == 200
        assert 'Família Teste da Silva' in r.data.decode()

    def test_nome_vazio_retorna_erro(self, logado):
        r = logado.post('/beneficiarios/novo', data={
            'nome':    '   ',
            'membros': '2',
        }, follow_redirects=True)
        assert r.status_code == 200
        assert 'vazio' in r.data.decode().lower()

    def test_membros_invalido_usa_fallback(self, logado):
        r = logado.post('/beneficiarios/novo', data={
            'nome':    'Família Fallback',
            'membros': 'xyz',
        }, follow_redirects=True)
        assert r.status_code == 200



class TestRelatorios:

    def test_pagina_relatorios(self, logado):
        r = logado.get('/relatorios/')
        assert r.status_code == 200

    def test_api_resumo_json(self, logado):
        r = logado.get('/relatorios/api/resumo')
        assert r.status_code == 200
        data = r.get_json()
        assert 'total_doacoes'       in data
        assert 'pendentes'           in data
        assert 'entregues'           in data
        assert 'cancelados'          in data
        assert 'total_beneficiarios' in data

    def test_api_categorias_json(self, logado):
        r = logado.get('/relatorios/api/categorias')
        assert r.status_code == 200
        data = r.get_json()
        assert isinstance(data, list)
