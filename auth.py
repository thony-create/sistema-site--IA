from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from functools import wraps
from models import User, Log, get_db_context
from datetime import datetime, timedelta
auth_bp = Blueprint('auth', __name__)
#teste para commit
def get_user_field(user, field, default=None):
    """Safely get field from sqlite3.Row object"""
    if user is None:
        return default
    return user[field] if field in user.keys() else default

def login_required(f):
    """Decorator to require login — supports ?next= redirect"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login para continuar.', 'warning')
            # Preserve the intended destination so we can redirect after login
            next_url = request.url
            return redirect(url_for('auth.login', next=next_url))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(min_level=None, allowed_types=None):
    """Decorator to check user permissions"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Por favor, faça login para continuar.', 'warning')
                return redirect(url_for('auth.login', next=request.url))
            
            user = User.obter_usuario_por_id(session['user_id'])
            if not user:
                flash('Usuário não encontrado.', 'danger')
                session.clear()
                return redirect(url_for('auth.login'))
            
            # Garantir que 'tipo' existe
            user_tipo = get_user_field(user, 'tipo', 'funcionario')
            
            # Check if user type is allowed
            if allowed_types and user_tipo not in allowed_types:
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('dashboard'))
            
            # Check permission levels: admin > gerente > funcionario
            nivel_usuarios = {'admin': 3, 'gerente': 2, 'funcionario': 1}
            if min_level and nivel_usuarios.get(user_tipo, 0) < min_level:
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    # If already logged in, go to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        
        if not email or not senha:
            flash('Email e senha são obrigatórios.', 'warning')
            return redirect(url_for('auth.login'))
        
        user = User.obter_usuario_por_email(email)
        
        if user and User.verificar_senha(user['id'], senha):
            # ----------------------------------------------------------------
            # PREVENÇÃO DE SESSION FIXATION — forma correta no Flask:
            # Limpar completamente a sessão anterior antes de atribuir dados
            # novos. O Flask irá emitir um novo cookie de sessão automaticamente.
            # NÃO usar session.regenerate() — esse método não existe em Flask.
            # ----------------------------------------------------------------
            session.clear()

            # Armazenar dados do usuário na sessão
            session['user_id']    = user['id']
            session['user_nome']  = user['nome']
            session['user_tipo']  = get_user_field(user, 'tipo', 'funcionario')
            session['logged_in']  = True
            session['login_at']   = datetime.now().isoformat()
            session.permanent     = True

            User.atualizar_ultimo_acesso(user['id'])

            flash(f'Bem-vindo, {user["nome"]}!', 'success')

            # Redirecionar para ?next= se houver, ou para o dashboard
            next_url = request.args.get('next') or request.form.get('next')
            # Segurança: só aceita redirect interno (começa com /)
            if next_url and next_url.startswith('/') and not next_url.startswith('//'):
                return redirect(next_url)
            return redirect(url_for('dashboard'))

        elif not user:
            flash('Usuário não encontrado. Verifique o e-mail digitado.', 'danger')
        else:
            flash('Senha incorreta. Tente novamente.', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """User registration route"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        # Validations
        if not all([nome, email, senha, confirmar_senha]):
            flash('Todos os campos são obrigatórios.', 'warning')
            return redirect(url_for('auth.registro'))
        
        # Validar formato do email
        import re
        if not re.match(r'^[a-zA-Z0-9](?:[a-zA-Z0-9._-]*[a-zA-Z0-9])?@[a-zA-Z0-9](?:[a-zA-Z0-9.-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}$', email) or '..' in email:
            flash('Por favor, insira um endereço de e-mail válido.', 'warning')
            return redirect(url_for('auth.registro'))
        
        if len(senha) < 8:
            flash('A senha deve ter no mínimo 8 caracteres.', 'warning')
            return redirect(url_for('auth.registro'))
        
        # Validar força da senha
        if not validar_senha_forte(senha):
            flash('A senha deve conter pelo menos uma letra maiúscula, uma minúscula, um número e um caractere especial.', 'warning')
            return redirect(url_for('auth.registro'))
        
        if senha != confirmar_senha:
            flash('As senhas não coincidem.', 'warning')
            return redirect(url_for('auth.registro'))
        
        # Check if email already exists
        if User.obter_usuario_por_email(email):
            flash('Este email já está cadastrado.', 'warning')
            return redirect(url_for('auth.registro'))
        
        # Create user
        usuario_id = User.criar_usuario(nome, email, senha, tipo='funcionario')
        
        if usuario_id:
            Log.registrar_acao(usuario_id, 'CRIAR', 'usuarios', usuario_id, f'Novo usuário criado: {nome}')
            flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Erro ao criar usuário. Tente novamente.', 'danger')
    
    return render_template('registro.html')

@auth_bp.route('/logout')
def logout():
    """Logout route"""
    user_id = session.get('user_id')
    if user_id:
        Log.registrar_acao(user_id, 'LOGOUT', 'sessoes', user_id, 'Usuário fez logout')
    session.clear()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    """User profile page"""
    user_id = session.get('user_id')
    user = User.obter_usuario_por_id(user_id)
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha_atual = request.form.get('senha_atual')
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        # Update name
        if nome and nome != user['nome']:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE usuarios SET nome = ? WHERE id = ?', (nome, user_id))
            Log.registrar_acao(user_id, 'ATUALIZAR', 'usuarios', user_id, f'Alterado nome para: {nome}')
            session['user_nome'] = nome
            flash('Nome atualizado com sucesso!', 'success')
        
        # Update password
        if nova_senha:
            if not senha_atual or not User.verificar_senha(user_id, senha_atual):
                flash('Senha atual incorreta.', 'danger')
                return render_template('perfil.html', user=user)
            
            if len(nova_senha) < 8:
                flash('A nova senha deve ter no mínimo 8 caracteres.', 'warning')
                return render_template('perfil.html', user=user)
            
            if not validar_senha_forte(nova_senha):
                flash('A nova senha deve conter pelo menos uma letra maiúscula, uma minúscula, um número e um caractere especial.', 'warning')
                return render_template('perfil.html', user=user)
            
            if nova_senha != confirmar_senha:
                flash('As novas senhas não coincidem.', 'warning')
                return render_template('perfil.html', user=user)
            
            from werkzeug.security import generate_password_hash
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE usuarios SET senha = ? WHERE id = ?', 
                             (generate_password_hash(nova_senha), user_id))
            Log.registrar_acao(user_id, 'ATUALIZAR', 'usuarios', user_id, 'Senha alterada')
            flash('Senha atualizada com sucesso!', 'success')
        
        user = User.obter_usuario_por_id(user_id)
    
    return render_template('perfil.html', user=user)

@auth_bp.route('/check-email', methods=['POST'])
def check_email():
    """Check if email already exists (API endpoint)"""
    email = request.form.get('email')
    if User.obter_usuario_por_email(email):
        return jsonify({'exists': True})
    return jsonify({'exists': False})

def hash_password(password):
    """Hash a password"""
    from werkzeug.security import generate_password_hash
    return generate_password_hash(password)

def verify_password(user_id, password):
    """Verify a password for a user"""
    return User.verificar_senha(user_id, password)

def validar_senha_forte(senha):
    """Validar se a senha é forte o suficiente"""
    import re
    if len(senha) < 8:
        return False
    if not re.search(r'[A-Z]', senha):
        return False
    if not re.search(r'[a-z]', senha):
        return False
    if not re.search(r'[0-9]', senha):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        return False
    return True
