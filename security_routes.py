from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from functools import wraps
from datetime import datetime, timedelta
from models import User, Log
from permissions import require_login, can_view_financial_data, get_user_field
from config import Config

security_bp = Blueprint('security', __name__, url_prefix='/security')

# Session-based password confirmation tracking
PASSWORD_CONFIRMATIONS = {}

def password_confirmation_required(f):
    """Decorator to require password confirmation for sensitive operations"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        
        if not user_id:
            flash('Por favor, faça login para continuar.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Check if password was recently confirmed
        if not is_password_confirmed(user_id):
            # Store the requested URL to redirect after confirmation
            session['password_confirm_redirect'] = request.url
            return redirect(url_for('security.confirm_password'))
        
        return f(*args, **kwargs)
    return decorated_function

def is_password_confirmed(user_id, timeout_minutes=None):
    """Check if user has recently confirmed password"""
    if timeout_minutes is None:
        timeout_minutes = Config.RELATORIO_TIMEOUT_MINUTOS
    
    if user_id not in PASSWORD_CONFIRMATIONS:
        return False
    
    confirmation_time = PASSWORD_CONFIRMATIONS[user_id]
    expiry_time = confirmation_time + timedelta(minutes=timeout_minutes)
    
    if datetime.now() > expiry_time:
        # Confirmation expired
        del PASSWORD_CONFIRMATIONS[user_id]
        return False
    
    return True

def mark_password_confirmed(user_id):
    """Mark that user has confirmed their password"""
    PASSWORD_CONFIRMATIONS[user_id] = datetime.now()

@security_bp.route('/confirm-password', methods=['GET', 'POST'])
@require_login
def confirm_password():
    """Confirm password for accessing sensitive data"""
    user_id = session.get('user_id')
    user = User.obter_usuario_por_id(user_id)
    
    if request.method == 'POST':
        senha = request.form.get('senha')
        
        if not senha:
            flash('Por favor, digite sua senha.', 'warning')
            return render_template('security/confirm_password.html', user=user)
        
        # Verify password
        if not User.verificar_senha(user_id, senha):
            flash('Senha incorreta. Tente novamente.', 'danger')
            Log.registrar_acao(user_id, 'FALHA_AUTENTICAÇÃO', 'seguranca', user_id, 
                             'Tentativa de confirmação de senha falhou')
            return render_template('security/confirm_password.html', user=user)
        
        # Mark password as confirmed
        mark_password_confirmed(user_id)
        Log.registrar_acao(user_id, 'CONFIRMACAO_SENHA', 'seguranca', user_id, 
                         'Senha confirmada para acesso a dados sensíveis')
        
        # Redirect to original page or dashboard
        redirect_url = session.pop('password_confirm_redirect', url_for('dashboard'))
        flash('Acesso concedido!', 'success')
        return redirect(redirect_url)
    
    return render_template('security/confirm_password.html', user=user)

@security_bp.route('/clear-confirmation')
@require_login
def clear_password_confirmation():
    """Clear password confirmation"""
    user_id = session.get('user_id')
    if user_id in PASSWORD_CONFIRMATIONS:
        del PASSWORD_CONFIRMATIONS[user_id]
    flash('Confirmação de senha limpa.', 'info')
    return redirect(url_for('dashboard'))

@security_bp.route('/check-confirmation')
@require_login
def check_password_confirmation():
    """API endpoint to check if password is confirmed (AJAX)"""
    user_id = session.get('user_id')
    confirmed = is_password_confirmed(user_id)
    return jsonify({'confirmed': confirmed})

@security_bp.route('/unauthorized')
def unauthorized():
    """Unauthorized access page"""
    return render_template('security/unauthorized.html'), 403

@security_bp.route('/access-denied')
def access_denied():
    """Access denied page"""
    return render_template('security/access_denied.html'), 403

@security_bp.route('/session-expired')
def session_expired():
    """Session expired page"""
    session.clear()
    return render_template('security/session_expired.html'), 401

# API endpoint for checking access permissions
@security_bp.route('/api/can-access/<resource_type>', methods=['GET'])
@require_login
def api_can_access(resource_type):
    """Check if user can access specific resource (API endpoint)"""
    user_id = session.get('user_id')
    user = User.obter_usuario_por_id(user_id)
    
    if not user:
        return jsonify({'access': False, 'message': 'User not found'})
    
    # Check resource-specific permissions
    user_tipo = get_user_field(user, 'tipo', 'funcionario')
    access_rules = {
        'financial_reports': can_view_financial_data(user_id),
        'employee_data': user_tipo in ['admin', 'gerente'],
        'audit_logs': user_tipo == 'admin',
        'user_management': user_tipo == 'admin',
        'sales': True,  # All users can view sales
        'inventory': user_tipo in ['admin', 'gerente'],
    }
    
    can_access = access_rules.get(resource_type, False)
    
    return jsonify({
        'access': can_access,
        'user_type': user_tipo,
        'requires_confirmation': resource_type in ['financial_reports', 'employee_data', 'audit_logs']
    })
