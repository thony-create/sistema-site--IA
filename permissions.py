from functools import wraps
from flask import request, session, redirect, url_for, flash, render_template
from models import User

# Permission levels
PERMISSION_LEVELS = {
    'admin': 3,
    'gerente': 2,
    'funcionario': 1
}

def get_user_field(user, field, default=None):
    """Safely get field from sqlite3.Row object"""
    if user is None:
        return default
    return user[field] if field in user.keys() else default

def get_user_permission_level(user_id):
    """Get user permission level"""
    user = User.obter_usuario_por_id(user_id)
    if user:
        user_tipo = get_user_field(user, 'tipo', 'funcionario')
        return PERMISSION_LEVELS.get(user_tipo, 0)
    return 0

def require_login(f):
    """Require user to be logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login para continuar.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        user = User.obter_usuario_por_id(session['user_id'])
        if not user or not user['ativo']:
            session.clear()
            flash('Sua conta foi desativada ou não foi encontrada.', 'danger')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function

def require_permission(min_level=None, allowed_types=None):
    """
    Decorator to check user permission level
    
    Args:
        min_level: Minimum permission level needed (1=funcionario, 2=gerente, 3=admin)
        allowed_types: List of allowed user types (e.g., ['admin', 'gerente'])
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Por favor, faça login para continuar.', 'warning')
                return redirect(url_for('auth.login', next=request.url))
            
            user = User.obter_usuario_por_id(session['user_id'])
            if not user:
                session.clear()
                flash('Usuário não encontrado.', 'danger')
                return redirect(url_for('auth.login'))
            
            if not user['ativo']:
                session.clear()
                flash('Sua conta foi desativada.', 'danger')
                return redirect(url_for('auth.login'))
            
            # Check specific allowed types
            user_tipo = get_user_field(user, 'tipo', 'funcionario')
            if allowed_types and user_tipo not in allowed_types:
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('dashboard'))
            
            # Check minimum permission level
            user_level = PERMISSION_LEVELS.get(user_tipo, 0)
            if min_level and user_level < min_level:
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_admin(f):
    """Require admin access"""
    return require_permission(allowed_types=['admin'])(f)

def require_gerente(f):
    """Require gerente or admin access"""
    return require_permission(allowed_types=['admin', 'gerente'])(f)

def require_funcionario(f):
    """Allow any logged-in user (funcionario level or higher)"""
    return require_login(f)

def can_edit_user(current_user_id, target_user_id):
    """Check if current user can edit target user"""
    current_user = User.obter_usuario_por_id(current_user_id)
    target_user = User.obter_usuario_por_id(target_user_id)
    
    if not current_user or not target_user:
        return False
    
    # Only admin can edit users
    if get_user_field(current_user, 'tipo', 'funcionario') != 'admin':
        return False
    
    # Admin can edit any user except themselves and other admins (optional rule)
    return True

def can_delete_user(current_user_id, target_user_id):
    """Check if current user can delete target user"""
    if current_user_id == target_user_id:
        return False  # Cannot delete yourself
    
    current_user = User.obter_usuario_por_id(current_user_id)
    if not current_user or get_user_field(current_user, 'tipo', 'funcionario') != 'admin':
        return False
    
    return True

def can_view_financial_data(user_id):
    """Check if user can view financial data"""
    user = User.obter_usuario_por_id(user_id)
    if not user:
        return False
    
    # Admin and gerente can view financial data
    return get_user_field(user, 'tipo', 'funcionario') in ['admin', 'gerente']

def can_register_sales(user_id):
    """Check if user can register sales"""
    user = User.obter_usuario_por_id(user_id)
    if not user:
        return False
    
    # All user types can register sales
    return True

def can_manage_inventory(user_id):
    """Check if user can manage inventory"""
    user = User.obter_usuario_por_id(user_id)
    if not user:
        return False
    
    # Admin and gerente can manage inventory
    return get_user_field(user, 'tipo', 'funcionario') in ['admin', 'gerente']

def can_manage_employees(user_id):
    """Check if user can manage employees"""
    user = User.obter_usuario_por_id(user_id)
    if not user:
        return False
    
    # Only admin can manage employees
    return get_user_field(user, 'tipo', 'funcionario') == 'admin'

def can_view_reports(user_id):
    """Check if user can view reports"""
    user = User.obter_usuario_por_id(user_id)
    if not user:
        return False
    
    # Admin and gerente can view reports
    return get_user_field(user, 'tipo', 'funcionario') in ['admin', 'gerente']

def can_view_logs(user_id):
    """Check if user can view audit logs"""
    user = User.obter_usuario_por_id(user_id)
    if not user:
        return False
    
    # Only admin can view logs
    return get_user_field(user, 'tipo', 'funcionario') == 'admin'

# User type descriptions
USER_TYPE_DESCRIPTIONS = {
    'admin': {
        'nome': 'Administrador',
        'descricao': 'Acesso total ao sistema. Pode gerenciar usuários, inventário, vendas, funcionários e relatórios.',
        'icon': 'shield'
    },
    'gerente': {
        'nome': 'Gerente',
        'descricao': 'Pode visualizar relatórios financeiros, gerenciar inventário e registrar vendas.',
        'icon': 'briefcase'
    },
    'funcionario': {
        'nome': 'Funcionário',
        'descricao': 'Pode registrar vendas e visualizar informações básicas do sistema.',
        'icon': 'user'
    }
}

# Permission matrix
PERMISSION_MATRIX = {
    'admin': {
        'dashboard': True,
        'vendas_registrar': True,
        'vendas_visualizar': True,
        'estoque_gerenciar': True,
        'clientes_gerenciar': True,
        'usuarios_gerenciar': True,
        'funcionarios_gerenciar': True,
        'relatorios_visualizar': True,
        'relatorios_exportar': True,
        'logs_visualizar': True,
        'chat_ia': True,
        'configuracoes': True
    },
    'gerente': {
        'dashboard': True,
        'vendas_registrar': True,
        'vendas_visualizar': True,
        'estoque_gerenciar': True,
        'clientes_gerenciar': True,
        'usuarios_gerenciar': False,
        'funcionarios_gerenciar': False,
        'relatorios_visualizar': True,
        'relatorios_exportar': True,
        'logs_visualizar': False,
        'chat_ia': True,
        'configuracoes': False
    },
    'funcionario': {
        'dashboard': True,
        'vendas_registrar': True,
        'vendas_visualizar': True,
        'estoque_gerenciar': False,
        'clientes_gerenciar': False,
        'usuarios_gerenciar': False,
        'funcionarios_gerenciar': False,
        'relatorios_visualizar': False,
        'relatorios_exportar': False,
        'logs_visualizar': False,
        'chat_ia': True,
        'configuracoes': False
    }
}

def has_permission(user_id, permission_key):
    """Check if user has specific permission"""
    user = User.obter_usuario_por_id(user_id)
    if not user:
        return False
    
    user_type = user['tipo']
    matrix = PERMISSION_MATRIX.get(user_type, {})
    return matrix.get(permission_key, False)
