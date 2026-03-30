from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from functools import wraps
from models import User, Funcionario, Log, Venda, Produto, get_db_context
from permissions import require_admin, can_edit_user, can_delete_user, can_manage_employees, get_user_field
from werkzeug.security import generate_password_hash
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ==================== DECORATORS ====================

def admin_required(f):
    """Require admin access"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login para continuar.', 'warning')
            return redirect(url_for('auth.login'))
        
        user = User.obter_usuario_por_id(session['user_id'])
        user_tipo = get_user_field(user, 'tipo', 'funcionario')
        if not user or user_tipo != 'admin':
            flash('Você não tem permissão para acessar esta página.', 'danger')
            return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated

# ==================== ADMIN PAINEL ====================

@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin dashboard"""
    admin_id = session.get('user_id')
    admin = User.obter_usuario_por_id(admin_id)
    
    with get_db_context() as conn:
        cursor = conn.cursor()
        
        # Statistics
        total_usuarios = cursor.execute('''
            SELECT COUNT(*) FROM usuarios WHERE ativo = 1
        ''').fetchone()[0]
        
        total_vendas = cursor.execute('''
            SELECT COUNT(*) FROM vendas WHERE usuario_id = ?
        ''', (admin_id,)).fetchone()[0]
        
        total_funcionarios = cursor.execute('''
            SELECT COUNT(*) FROM funcionarios WHERE usuario_id = ? AND ativo = 1
        ''', (admin_id,)).fetchone()[0]
        
        revenue_total = cursor.execute('''
            SELECT COALESCE(SUM(valor_total), 0) FROM vendas WHERE usuario_id = ?
        ''', (admin_id,)).fetchone()[0]
    
    stats = {
        'total_usuarios': total_usuarios,
        'total_vendas': total_vendas,
        'total_funcionarios': total_funcionarios,
        'revenue_total': revenue_total
    }
    
    return render_template('admin/dashboard.html', admin=admin, stats=stats)

# ==================== GERENCIAMENTO DE USUÁRIOS ====================

@admin_bp.route('/usuarios')
@admin_required
def listar_usuarios():
    """List all users"""
    usuarios = User.listar_usuarios()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@admin_bp.route('/usuarios/criar', methods=['GET', 'POST'])
@admin_required
def criar_usuario():
    """Create a new user"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        tipo = request.form.get('tipo', 'funcionario')
        
        # Validations
        if not all([nome, email, senha, confirmar_senha]):
            flash('Todos os campos são obrigatórios.', 'warning')
            return redirect(url_for('admin.criar_usuario'))
        
        if len(senha) < 8:
            flash('A senha deve ter no mínimo 8 caracteres.', 'warning')
            return redirect(url_for('admin.criar_usuario'))
        
        if senha != confirmar_senha:
            flash('As senhas não coincidem.', 'warning')
            return redirect(url_for('admin.criar_usuario'))
        
        if User.obter_usuario_por_email(email):
            flash('Este email já está cadastrado.', 'warning')
            return redirect(url_for('admin.criar_usuario'))
        
        # Create user
        usuario_id = User.criar_usuario(nome, email, senha, tipo=tipo)
        
        if usuario_id:
            Log.registrar_acao(session['user_id'], 'CRIAR', 'usuarios', usuario_id, 
                             f'Novo usuário criado: {nome} ({tipo})')
            flash(f'Usuário {nome} criado com sucesso!', 'success')
            return redirect(url_for('admin.listar_usuarios'))
        else:
            flash('Erro ao criar usuário. Tente novamente.', 'danger')
    
    return render_template('admin/criar_usuario.html')

@admin_bp.route('/usuarios/<int:usuario_id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_usuario(usuario_id):
    """Edit a user"""
    admin_id = session.get('user_id')
    
    if not can_edit_user(admin_id, usuario_id):
        flash('Você não tem permissão para editar este usuário.', 'danger')
        return redirect(url_for('admin.listar_usuarios'))
    
    usuario = User.obter_usuario_por_id(usuario_id)
    if not usuario:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('admin.listar_usuarios'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        tipo = request.form.get('tipo')
        nova_senha = request.form.get('nova_senha')
        
        if nome:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE usuarios SET nome = ? WHERE id = ?', (nome, usuario_id))
            Log.registrar_acao(admin_id, 'ATUALIZAR', 'usuarios', usuario_id, 
                             f'Nome alterado para: {nome}')
        
        if tipo and tipo in ['admin', 'gerente', 'funcionario']:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE usuarios SET tipo = ? WHERE id = ?', (tipo, usuario_id))
            Log.registrar_acao(admin_id, 'ATUALIZAR', 'usuarios', usuario_id, 
                             f'Tipo de usuário alterado para: {tipo}')
        
        if nova_senha and len(nova_senha) >= 8:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE usuarios SET senha = ? WHERE id = ?',
                             (generate_password_hash(nova_senha), usuario_id))
            Log.registrar_acao(admin_id, 'ATUALIZAR', 'usuarios', usuario_id, 'Senha alterada')
        
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('admin.listar_usuarios'))
    
    return render_template('admin/editar_usuario.html', usuario=usuario)

@admin_bp.route('/usuarios/<int:usuario_id>/deletar', methods=['POST'])
@admin_required
def deletar_usuario(usuario_id):
    """Delete (deactivate) a user"""
    admin_id = session.get('user_id')
    
    if not can_delete_user(admin_id, usuario_id):
        return jsonify({'erro': 'Você não tem permissão para deletar este usuário'}), 403
    
    usuario = User.obter_usuario_por_id(usuario_id)
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    try:
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE usuarios SET ativo = 0 WHERE id = ?', (usuario_id,))
        
        Log.registrar_acao(admin_id, 'DELETAR', 'usuarios', usuario_id, 
                         f'Usuário desativado: {usuario["nome"]}')
        
        return jsonify({'sucesso': True, 'mensagem': 'Usuário desativado com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# ==================== GERENCIAMENTO DE FUNCIONÁRIOS ====================

@admin_bp.route('/funcionarios')
@admin_required
def listar_funcionarios():
    """List all employees"""
    admin_id = session.get('user_id')
    funcionarios = Funcionario.obter_funcionarios_usuario(admin_id)
    
    return render_template('admin/funcionarios.html', funcionarios=funcionarios)

@admin_bp.route('/funcionarios/criar', methods=['GET', 'POST'])
@admin_required
def criar_funcionario():
    """Create a new employee"""
    admin_id = session.get('user_id')
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        cargo = request.form.get('cargo')
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        data_admissao = request.form.get('data_admissao')
        salario = float(request.form.get('salario', 0))
        comissao_percentual = float(request.form.get('comissao_percentual', 0))
        usuario_funcionario_id = request.form.get('usuario_funcionario_id', type=int)
        
        if not all([nome, cargo, data_admissao]):
            flash('Nome, cargo e data de admissão são obrigatórios.', 'warning')
            return redirect(url_for('admin.criar_funcionario'))
        
        try:
            funcionario_id = Funcionario.criar_funcionario(
                admin_id, nome, email, cargo, data_admissao, salario, comissao_percentual
            )
            
            # If associated with a user
            if usuario_funcionario_id:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE funcionarios SET usuario_funcionario_id = ? WHERE id = ?',
                                 (usuario_funcionario_id, funcionario_id))
            
            Log.registrar_acao(admin_id, 'CRIAR', 'funcionarios', funcionario_id, 
                             f'Novo funcionário criado: {nome}')
            flash(f'Funcionário {nome} criado com sucesso!', 'success')
            return redirect(url_for('admin.listar_funcionarios'))
        except Exception as e:
            flash(f'Erro ao criar funcionário: {str(e)}', 'danger')
    
    # Get available users for association
    usuarios = User.listar_usuarios()
    
    return render_template('admin/criar_funcionario.html', usuarios=usuarios)

@admin_bp.route('/funcionarios/<int:funcionario_id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_funcionario(funcionario_id):
    """Edit an employee"""
    admin_id = session.get('user_id')
    
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM funcionarios WHERE id = ? AND usuario_id = ?',
                      (funcionario_id, admin_id))
        funcionario = cursor.fetchone()
    
    if not funcionario:
        flash('Funcionário não encontrado.', 'danger')
        return redirect(url_for('admin.listar_funcionarios'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        cargo = request.form.get('cargo')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        salario = float(request.form.get('salario', 0))
        comissao_percentual = float(request.form.get('comissao_percentual', 0))
        
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE funcionarios 
                    SET nome = ?, cargo = ?, email = ?, telefone = ?, salario = ?, comissao_percentual = ?
                    WHERE id = ?
                ''', (nome, cargo, email, telefone, salario, comissao_percentual, funcionario_id))
            
            Log.registrar_acao(admin_id, 'ATUALIZAR', 'funcionarios', funcionario_id,
                             f'Funcionário atualizado: {nome}')
            flash('Funcionário atualizado com sucesso!', 'success')
            return redirect(url_for('admin.listar_funcionarios'))
        except Exception as e:
            flash(f'Erro ao atualizar: {str(e)}', 'danger')
    
    usuarios = User.listar_usuarios()
    
    return render_template('admin/editar_funcionario.html', funcionario=funcionario, usuarios=usuarios)

@admin_bp.route('/funcionarios/<int:funcionario_id>/deletar', methods=['POST'])
@admin_required
def deletar_funcionario(funcionario_id):
    """Delete (deactivate) an employee"""
    admin_id = session.get('user_id')
    
    try:
        with get_db_context() as conn:
            cursor = conn.cursor()
            # Check if employee belongs to this admin
            cursor.execute('SELECT * FROM funcionarios WHERE id = ? AND usuario_id = ?',
                          (funcionario_id, admin_id))
            funcionario = cursor.fetchone()
            
            if not funcionario:
                return jsonify({'erro': 'Funcionário não encontrado'}), 404
            
            # Deactivate
            cursor.execute('UPDATE funcionarios SET ativo = 0 WHERE id = ?', (funcionario_id,))
        
        Log.registrar_acao(admin_id, 'DELETAR', 'funcionarios', funcionario_id,
                         f'Funcionário desativado: {funcionario["nome"]}')
        
        return jsonify({'sucesso': True, 'mensagem': 'Funcionário desativado'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# ==================== RANKING DE VENDEDORES ====================

@admin_bp.route('/ranking-vendedores')
@admin_required
def ranking_vendedores():
    """Employee sales ranking"""
    admin_id = session.get('user_id')
    ranking = Funcionario.obter_ranking_vendedores(admin_id)
    
    return render_template('admin/ranking_vendedores.html', ranking=ranking)

# ==================== LOGS E AUDITORIA ====================

@admin_bp.route('/logs')
@admin_required
def logs():
    """View audit logs"""
    admin_id = session.get('user_id')
    pagina = request.args.get('pagina', 1, type=int)
    limite = 50
    offset = (pagina - 1) * limite
    
    with get_db_context() as conn:
        cursor = conn.cursor()
        
        # Get logs
        cursor.execute('''
            SELECT l.id, l.usuario_id, l.funcionario_id, l.tipo_acao, l.tabela, l.id_registro, 
                   l.descricao, l.dados_antigos, l.dados_novos, l.data_acao, l.endereco_ip,
                   u.nome as usuario_nome
            FROM logs_acao l
            LEFT JOIN usuarios u ON l.usuario_id = u.id
            WHERE l.usuario_id = ? OR l.usuario_id IS NULL
            ORDER BY l.data_acao DESC
            LIMIT ? OFFSET ?
        ''', (admin_id, limite, offset))
        logs = cursor.fetchall()
        
        # Total count
        total = cursor.execute('''
            SELECT COUNT(*) FROM logs_acao
            WHERE usuario_id = ? OR usuario_id IS NULL
        ''', (admin_id,)).fetchone()[0]
    
    total_paginas = (total + limite - 1) // limite
    
    return render_template('admin/logs.html', logs=logs, pagina=pagina, total_paginas=total_paginas)

# ==================== CONFIGURAÇÕES ====================

@admin_bp.route('/configuracoes')
@admin_required
def configuracoes():
    """Admin settings"""
    admin_id = session.get('user_id')
    admin = User.obter_usuario_por_id(admin_id)
    
    return render_template('admin/configuracoes.html', admin=admin)

@admin_bp.route('/configuracoes/atualizar', methods=['POST'])
@admin_required
def atualizar_configuracoes():
    """Update admin settings"""
    admin_id = session.get('user_id')
    
    try:
        config_data = request.get_json()
        
        # Validate and save settings
        # This can be extended based on what settings you want to allow
        
        Log.registrar_acao(admin_id, 'ATUALIZAR', 'configuracoes', admin_id, 'Configurações atualizadas')
        
        return jsonify({'sucesso': True, 'mensagem': 'Configurações salvas com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@admin_bp.errorhandler(403)
def forbidden(error):
    """Handle 403 Forbidden"""
    flash('Você não tem permissão para acessar esta página.', 'danger')
    return redirect(url_for('dashboard'))

@admin_bp.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found"""
    flash('Página não encontrada.', 'warning')
    return redirect(url_for('admin.dashboard'))
