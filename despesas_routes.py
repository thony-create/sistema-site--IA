from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Despesa, Log
from permissions import require_login
from datetime import datetime

despesas_bp = Blueprint('despesas', __name__)

@despesas_bp.route('/despesas')
@require_login
def listar_despesas():
    usuario_id = session['user_id']
    hoje = datetime.now()
    despesas = Despesa.obter_despesas_mes(usuario_id, hoje.month, hoje.year)
    
    # Calcular total do mês
    total_mes = sum(d['valor'] for d in despesas)
    
    return render_template('despesas.html', 
                         despesas=despesas, 
                         total_mes=total_mes,
                         mes_atual=hoje.strftime('%B/%Y'))

@despesas_bp.route('/despesas/adicionar', methods=['POST'])
@require_login
def adicionar_despesa():
    usuario_id = session['user_id']
    descricao = request.form.get('descricao')
    valor = float(request.form.get('valor', 0))
    categoria = request.form.get('categoria')
    data_str = request.form.get('data')
    
    data_despesa = datetime.strptime(data_str, '%Y-%m-%d') if data_str else datetime.now()
    
    despesa_id = Despesa.criar_despesa(usuario_id, descricao, valor, categoria, data_despesa)
    
    if despesa_id:
        Log.registrar_acao(usuario_id, 'CRIAR', 'despesas', despesa_id, f'Despesa adicionada: {descricao}')
        flash('Despesa registrada com sucesso!', 'success')
    else:
        flash('Erro ao registrar despesa.', 'danger')
        
    return redirect(url_for('despesas.listar_despesas'))
