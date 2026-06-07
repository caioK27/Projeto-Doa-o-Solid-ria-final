"""
Doação Solidária — Sistema de Gestão de Doações para Comunidades Vulneráveis
Ponto de entrada da aplicação Flask.

CORREÇÕES APLICADAS:
  - Bug #10: host alterado para 127.0.0.1 (apenas local, sem expor na rede)
             debug lido de variável de ambiente FLASK_DEBUG

Uso:
    python run.py
    ou
    flask run
"""

import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # FIX #10: host 127.0.0.1 não expõe na rede local.
    # Para acessar de outro dispositivo, altere para '0.0.0.0' SOMENTE em dev controlado.
    debug_mode = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(
        debug=debug_mode,
        host='127.0.0.1',
        port=5000,
    )
