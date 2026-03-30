#!/usr/bin/env python
"""
Script para testar a configuração do sistema
"""
import os
import sys

print("="*60)
print("TESTE DE CONFIGURAÇÃO DO SISTEMA")
print("="*60)

# 1. Verificar Python
print("\n✓ Python Version:", sys.version.split()[0])

# 2. Verificar arquivos essenciais
print("\n📁 Verificando arquivos essenciais...")
required_files = [
    'app.py',
    'models.py',
    'auth.py',
    'permissions.py',
    'config.py',
    'requirements.txt',
    'static/style.css',
    'templates/dashboard.html'
]

for file in required_files:
    exists = os.path.exists(file)
    status = "✓" if exists else "✗"
    print(f"  {status} {file}")

# 3. Verificar importações
print("\n📦 Verificando importações principais...")
try:
    from flask import Flask
    print("  ✓ Flask")
except ImportError as e:
    print(f"  ✗ Flask: {e}")

try:
    from models import init_db, get_db
    print("  ✓ Models")
except ImportError as e:
    print(f"  ✗ Models: {e}")

try:
    from auth import auth_bp
    print("  ✓ Auth")
except ImportError as e:
    print(f"  ✗ Auth: {e}")

try:
    from config import Config
    print("  ✓ Config")
except ImportError as e:
    print(f"  ✗ Config: {e}")

try:
    from permissions import require_login, require_admin, require_gerente
    print("  ✓ Permissions")
except ImportError as e:
    print(f"  ✗ Permissions: {e}")

# 4. Testar inicialização do banco
print("\n🗄️  Testando banco de dados...")
try:
    from models import init_db
    print("  ✓ Banco de dados será inicializado ao executar app.py")
except Exception as e:
    print(f"  ✗ Erro: {e}")

# 5. Resumo final
print("\n" + "="*60)
print("✅ TESTE COMPLETO!")
print("="*60)
print("\nPróximos passos:")
print("1. Execute: pip install -r requirements.txt")
print("2. Execute: python app.py")
print("3. Acesse: http://localhost:5000")
print("\n" + "="*60)
