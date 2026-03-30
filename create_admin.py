#!/usr/bin/env python3
"""
Script para criar usuário administrador inicial
Uso: python create_admin.py
"""

from models import User, init_db
import getpass

def criar_admin():
    """Criar usuário administrador"""
    print("=== Criação de Usuário Administrador ===")
    print("Este script criará o primeiro usuário administrador do sistema.")
    print()

    # Solicitar dados
    nome = input("Nome completo: ").strip()
    while not nome:
        nome = input("Nome é obrigatório. Nome completo: ").strip()

    email = input("E-mail: ").strip()
    while not email:
        email = input("E-mail é obrigatório. E-mail: ").strip()

    # Verificar se email já existe
    if User.obter_usuario_por_email(email):
        print(f"Erro: O e-mail '{email}' já está cadastrado no sistema.")
        return False

    senha = getpass.getpass("Senha (mínimo 12 caracteres): ")
    while len(senha) < 12:
        print("Erro: A senha deve ter pelo menos 12 caracteres.")
        senha = getpass.getpass("Senha (mínimo 12 caracteres): ")

    confirmar_senha = getpass.getpass("Confirmar senha: ")
    while senha != confirmar_senha:
        print("Erro: As senhas não coincidem.")
        confirmar_senha = getpass.getpass("Confirmar senha: ")

    # Validar força da senha
    import re
    if not re.search(r'[A-Z]', senha):
        print("Erro: A senha deve conter pelo menos uma letra maiúscula.")
        return False
    if not re.search(r'[a-z]', senha):
        print("Erro: A senha deve conter pelo menos uma letra minúscula.")
        return False
    if not re.search(r'[0-9]', senha):
        print("Erro: A senha deve conter pelo menos um número.")
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        print("Erro: A senha deve conter pelo menos um caractere especial.")
        return False

    # Verificar se já existe algum admin
    usuarios = User.listar_usuarios()
    admins_existentes = [u for u in usuarios if u['tipo'] == 'admin']

    if admins_existentes:
        print(f"Atenção: Já existem {len(admins_existentes)} administradores no sistema.")
        confirmar = input("Deseja criar outro administrador? (s/N): ").lower().strip()
        if confirmar != 's':
            print("Operação cancelada.")
            return False

    # Criar usuário
    try:
        usuario_id = User.criar_usuario(nome, email, senha, tipo='admin')
        if usuario_id:
            print("
✅ Usuário administrador criado com sucesso!"            print(f"ID: {usuario_id}")
            print(f"Nome: {nome}")
            print(f"E-mail: {email}")
            print(f"Tipo: admin")
            print()
            print("Você pode agora fazer login no sistema com essas credenciais.")
            return True
        else:
            print("Erro: Falha ao criar usuário. O e-mail pode já estar em uso.")
            return False
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    # Inicializar banco de dados
    init_db()

    # Executar criação
    sucesso = criar_admin()
    exit(0 if sucesso else 1)