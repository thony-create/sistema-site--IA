from app import app
from flask import url_for

print("Testing route generation...")
with app.test_request_context():
    print('Chat index:', url_for('chat.index'))
    print('Chat enviar:', url_for('chat.enviar_pergunta'))
    print('Chat sugestoes:', url_for('chat.obter_sugestoes'))
    print('Chat limpar:', url_for('chat.limpar_historico'))