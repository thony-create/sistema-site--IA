#!/usr/bin/env python3
"""
Script de teste da autenticação
Uso: python test_auth_system.py
"""

from models import User, init_db
from auth import validar_senha_forte
import re

def testar_autenticacao():
    """Testar sistema de autenticação"""
    print("=== Teste do Sistema de Autenticação ===\n")

    # Inicializar banco
    init_db()

    # Teste 1: Validação de senha forte
    print("1. Teste de validação de senha forte:")
    senhas_teste = [
        ("123456", False, "Muito curta"),
        ("senhafraca", False, "Sem maiúscula, número, especial"),
        ("Senha123", False, "Sem caractere especial"),
        ("MinhaSenha@123", True, "Senha forte válida (12+ chars)"),
        ("MinhaSenh@F0rte2024!", True, "Senha muito forte")
    ]

    for senha, esperado, descricao in senhas_teste:
        resultado = validar_senha_forte(senha)
        status = "✅" if resultado == esperado else "❌"
        print(f"   {status} '{senha}' - {descricao}: {resultado}")

    print()

    # Teste 2: Validação de email
    print("2. Teste de validação de e-mail:")
    emails_teste = [
        ("usuario@dominio.com", True, "E-mail válido"),
        ("usuario@dominio", False, "Sem domínio"),
        ("usuario", False, "Sem @"),
        ("@dominio.com", False, "Sem usuário"),
        ("usuario@.com", False, "Domínio inválido"),
        ("usuario..teste@dominio.com", False, "Pontos consecutivos")
    ]

    for email, esperado, descricao in emails_teste:
        resultado = bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))
        status = "✅" if resultado == esperado else "❌"
        print(f"   {status} '{email}' - {descricao}: {resultado}")

    print()

    # Teste 3: Verificar usuários existentes
    print("3. Usuários cadastrados no sistema:")
    usuarios = User.listar_usuarios()
    if usuarios:
        for usuario in usuarios:
            print(f"   ID: {usuario['id']}, Nome: {usuario['nome']}, Email: {usuario['email']}, Tipo: {usuario['tipo']}")
    else:
        print("   Nenhum usuário cadastrado.")

    print()

    # Teste 4: Teste de login (se houver usuários)
    if usuarios:
        print("4. Teste de verificação de senha:")
        for usuario in usuarios[:2]:  # Testar apenas os primeiros 2
            print(f"   Testando usuário: {usuario['nome']} ({usuario['email']})")

            # Tentar senha conhecida (se soubermos)
            if usuario['email'] == 'admin@teste.com':
                teste_senha = 'admin123'
                resultado = User.verificar_senha(usuario['id'], teste_senha)
                status = "✅" if resultado else "❌"
                print(f"      {status} Senha 'admin123': {resultado}")

            # Tentar senha errada
            resultado_errada = User.verificar_senha(usuario['id'], 'senha_errada_123')
            status = "✅" if not resultado_errada else "❌"
            print(f"      {status} Senha errada rejeitada: {not resultado_errada}")

    print("\n=== Teste Concluído ===")

if __name__ == "__main__":
    testar_autenticacao()