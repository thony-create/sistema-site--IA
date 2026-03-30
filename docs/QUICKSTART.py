#!/usr/bin/env python
"""
QUICKSTART - Cognix: Gestão Inteligente com Zyra
Siga os passos abaixo para executar o projeto
"""

print("""
╔════════════════════════════════════════════════════════════╗
║            COGNIX: GESTÃO INTELIGENTE COM ZYRA            ║
║                   🚀 GUIA DE INÍCIO RÁPIDO                 ║
╚════════════════════════════════════════════════════════════╝

📋 PRÉ-REQUISITOS:
   • Python 3.8 ou superior
   • pip (gerenciador de pacotes)
   • ~100MB de espaço em disco

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASSO 1️⃣  - CRIAR AMBIENTE VIRTUAL (Recomendado)
─────────────────────────────────────────────

   Windows (PowerShell):
   $ python -m venv venv
   $ .\\venv\\Scripts\\activate

   Windows (CMD):
   > python -m venv venv
   > venv\\Scripts\\activate

   Mac/Linux:
   $ python -m venv venv
   $ source venv/bin/activate

   Você saberá que funcionou quando seu prompt tiver (venv) no início.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASSO 2️⃣  - INSTALAR DEPENDÊNCIAS
────────────────────────────────

   $ pip install -r requirements.txt

   Isso instalará:
   • Flask 2.3.2 (web framework)
   • Werkzeug 2.3.6 (segurança)
   • Jinja2 3.1.2 (templates)
   • python-dotenv 1.0.0 (variáveis ambiente)
   • requests 2.31.0 (HTTP)
   • E mais...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASSO 3️⃣  - EXECUTAR O SERVIDOR
──────────────────────────

   $ python app.py

   Você deve ver:
   ⚠️  WARNING in app.runserver
   * Running on http://127.0.0.1:5000
   * Debug mode: on

   💡 Se vir mensagens de erro, veja a seção "TROUBLESHOOTING" abaixo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASSO 4️⃣  - ACESSAR A APLICAÇÃO
──────────────────────────────

   🌐 Navegue até: http://localhost:5000

   Você será redirecionado para a página de login.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASSO 5️⃣  - CRIAR PRIMEIRA CONTA
──────────────────────────────

   ✍️  Clique em "Registrar" (ou vá para /registro)
   
   Preencha:
   • Nome: Seu Nome
   • Email: seu@email.com
   • Senha: Uma senha segura
   
   Confirme a senha e clique em "Criar Conta"

   🎉 A primeira conta criada será automaticamente ADMIN!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧪 TESTE RAPIDO DA CONFIGURAÇÃO:

   $ python test_setup.py

   Isso verificará todos os arquivos e importações necessárias.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🐛 TROUBLESHOOTING:

ERRO: ModuleNotFoundError: No module named 'flask'
┌─────────────────────────────────────────────────────
└─ Solução: pip install -r requirements.txt

ERRO: Address already in use (porta 5000 ocupada)
┌─────────────────────────────────────────────────────
└─ Solução: 
   • Feche outras aplicações usando a porta 5000
   • Ou mude a porta em app.py (última linha):
     app.run(debug=True, port=5001)

ERRO: database is locked
┌─────────────────────────────────────────────────────
└─ Solução:
   • Feche todas as abas do navegador
   • Reinicie o servidor

ERRO: template not found
┌─────────────────────────────────────────────────────
└─ Solução: Certifique-se que está no diretório correto
   $ pwd  (Mac/Linux)
   $ cd  (Windows)
   Deve estar em: .../progamação

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 DOCUMENTAÇÃO COMPLETA:

   Leia: README.md

   Ele contém:
   • Todas as funcionalidades do sistema
   • Estrutura do projeto
   • Perfis de acesso
   • Como usar cada mó dulo
   • Guia de segurança para produção
   • Palavras-chave para o chat de IA

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ FUNCIONALIDADES PRINCIPAIS:

   ✓ Autenticação segura com senhas hasheadas
   ✓ Dashboard com indicadores de vendas em tempo real
   ✓ Gestão de estoque com alertas automáticos
   ✓ Registro de vendas com associação de clientes
   ✓ Relatórios com confirmação de senha
   ✓ Assistente IA com chat inteligente
   ✓ Gestão de funcionários e comissões
   ✓ Ranking de vendedores
   ✓ Auditoria completa de ações
   ✓ Interface moderna estilo SaaS
   ✓ Responsivo para mobile

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRÓXIMOS PASSOS APÓS LOGIN:

   1. Adicione alguns PRODUTOS em "Estoque → Adicionar Produto"
   2. Registre VENDAS em "Vendas → Nova Venda"
   3. Veja insights automáticos no DASHBOARD
   4. Converse com IA em "Assistente"
   5. Gerencie FUNCIONÁRIOS em "Operações"
   6. Visualize RELATÓRIOS (acesso protegido)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ PRECISA DE AJUDA?

   1. Leia o README.md para documentação completa
   2. Verifique o console do navegador para erros
   3. Veja os logs do servidor no terminal
   4. Todos os arquivos Python têm comentários explicativos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 Aproveite! Bem-vindo ao Cognix! 🎉

""")

input("Pressione ENTER para fechar...")
