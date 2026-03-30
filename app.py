"""
Cognix - Gestão Inteligente com IA
Backend Principal - Flask
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_file
from datetime import datetime, timedelta
import os

from config import Config, DevelopmentConfig, get_config
from models import init_db, get_db, User, Log
from auth import auth_bp, hash_password, verify_password
from ai_module import ai_bp, AnalysisEngine
from admin import admin_bp
from chat_routes import chat_bp
from permissions import require_login, require_admin, require_gerente, require_permission
from security_routes import security_bp, password_confirmation_required
from pdf_reports import gerar_pdf
from despesas_routes import despesas_bp
from models import Despesa, Meta
app = Flask(__name__)
app.config.from_object(Config)

# ----------------------------------------------------------------
# CONFIGURAÇÃO SEGURA DE SESSÃO
# secret_key lida da variável de ambiente (nunca hardcodar em produção)
# ----------------------------------------------------------------
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-chave-local-mude-em-producao-abc123!')

# Cookie de sessão seguro
app.config['SESSION_COOKIE_HTTPONLY']  = True      # JS não acessa o cookie
app.config['SESSION_COOKIE_SAMESITE']  = 'Lax'    # Protege contra CSRF básico
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)  # Sessão expira em 8h

# Inicializar banco de dados
init_db()

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(security_bp, url_prefix='/auth')
app.register_blueprint(despesas_bp)

@app.route('/')
def home():
    """Página inicial - redireciona para login ou dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
@require_login
def dashboard():
    """Dashboard principal com indicadores e gráficos"""
    db = get_db()
    user_id = session['user_id']
    
    # Faturamento do dia, semana e mês
    hoje = datetime.now().date()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    inicio_mes = hoje.replace(day=1)
    
    faturamento_dia = db.execute('''
        SELECT COALESCE(SUM(v.valor_total), 0) FROM vendas v
        WHERE v.usuario_id = ? AND DATE(v.data_venda) = ?
    ''', (user_id, hoje)).fetchone()[0]
    
    faturamento_semana = db.execute('''
        SELECT COALESCE(SUM(v.valor_total), 0) FROM vendas v
        WHERE v.usuario_id = ? AND DATE(v.data_venda) >= ?
    ''', (user_id, inicio_semana)).fetchone()[0]
    
    faturamento_mes = db.execute('''
        SELECT COALESCE(SUM(v.valor_total), 0) FROM vendas v
        WHERE v.usuario_id = ? AND DATE(v.data_venda) >= ?
    ''', (user_id, inicio_mes)).fetchone()[0]
    
    # Produtos com estoque baixo (< 10)
    produtos_baixos = db.execute('''
        SELECT id, nome, quantidade, preco FROM produtos
        WHERE usuario_id = ? AND quantidade < 10
        ORDER BY quantidade ASC LIMIT 5
    ''', (user_id,)).fetchall()
    
    # Produto mais vendido
    produto_top = db.execute('''
        SELECT p.id, p.nome, COUNT(iv.id) as vendas 
        FROM itens_venda iv
        JOIN produtos p ON iv.produto_id = p.id
        JOIN vendas v ON iv.venda_id = v.id
        WHERE v.usuario_id = ? AND DATE(v.data_venda) = ?
        GROUP BY p.id, p.nome
        ORDER BY vendas DESC LIMIT 1
    ''', (user_id, hoje)).fetchone()
    
    # Análises com IA
    analysis_engine = AnalysisEngine(user_id)
    insights = analysis_engine.gerar_insights()
    
    dados_graficos = analysis_engine.gerar_dados_graficos()
    
    alertas_zyra = analysis_engine.gerar_alertas_proativos()
    recomendacoes_zyra = analysis_engine.gerar_recomendacoes()
    
    # Módulo Financeiro & Metas
    # Módulo Financeiro & Metas
    despesas_lista = Despesa.obter_despesas_mes(user_id, hoje.month, hoje.year)
    total_despesas = sum(d['valor'] for d in despesas_lista)
    
    # Calcular faturamento do mês atual usando a conexão db já aberta
    data_inicio_mes = hoje.replace(day=1).strftime('%Y-%m-%d')
    faturamento_mes = db.execute('SELECT SUM(valor_total) FROM vendas WHERE usuario_id = ? AND data_venda >= ?', (user_id, data_inicio_mes)).fetchone()[0] or 0
    
    lucro_mes = faturamento_mes - total_despesas
    
    # Metas
    meta_valor = Meta.obter_meta(user_id, hoje.month, hoje.year) or 10000 # Default meta
    progresso_meta = (faturamento_mes / meta_valor) * 100 if meta_valor > 0 else 0
    progresso_meta = min(progresso_meta, 100) # Cap at 100% for display

    return render_template('dashboard.html',
                         faturamento_dia=faturamento_dia,
                         faturamento_semana=faturamento_semana,
                         produtos_baixos=produtos_baixos,
                         produto_top=produto_top,
                         insights=insights,
                         dados_graficos=dados_graficos,
                         alertas_zyra=alertas_zyra,
                         recomendacoes_zyra=recomendacoes_zyra,
                         total_despesas=total_despesas,
                         lucro_mes=lucro_mes,
                         faturamento_mes=faturamento_mes,
                         meta_valor=meta_valor,
                         progresso_meta=progresso_meta)

@app.route('/gerar_relatorio/<tipo>')
@require_login
def gerar_relatorio(tipo):
    """Gera o relatório mensal ou semanal em PDF"""
    if tipo not in ['semanal', 'mensal']:
        flash('Tipo de relatório inválido.', 'danger')
        return redirect(url_for('dashboard'))
        
    usuario_id = session['user_id']
    
    try:
        pdf_buffer = gerar_pdf(usuario_id, tipo)
        nome_arquivo = f"Relatorio_Cognix_{tipo}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=nome_arquivo,
            mimetype='application/pdf'
        )
    except Exception as e:
        flash(f'Erro ao gerar relatório: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/chat')
@require_login
def chat():
    """Página dedicada à Zyra - Consultora Inteligente - Redireciona para /chat/"""
    return redirect(url_for('chat.index'))

@app.route('/estoque')
@require_login
def estoque():
    """Página de controle de estoque"""
    db = get_db()
    user_id = session['user_id']
    
    produtos = db.execute('''
        SELECT id, nome, quantidade, preco, categoria, data_criacao
        FROM produtos
        WHERE usuario_id = ?
        ORDER BY nome ASC
    ''', (user_id,)).fetchall()
    
    return render_template('estoque.html', produtos=produtos)

@app.route('/estoque/adicionar', methods=['GET', 'POST'])
@require_login
def adicionar_produto():
    """Adicionar novo produto ao estoque"""
    if request.method == 'POST':
        db = get_db()
        user_id = session['user_id']
        
        nome = request.form.get('nome')
        quantidade = int(request.form.get('quantidade', 0))
        preco = float(request.form.get('preco', 0))
        categoria = request.form.get('categoria')
        
        if nome and quantidade >= 0 and preco > 0:
            db.execute('''
                INSERT INTO produtos (usuario_id, nome, quantidade, preco, categoria)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, nome, quantidade, preco, categoria))
            db.commit()
            flash(f'Produto "{nome}" adicionado com sucesso!', 'success')
            return redirect(url_for('estoque'))
        else:
            flash('Dados inválidos. Verifique os valores.', 'error')
    
    return render_template('adicionar_produto.html')

@app.route('/estoque/editar/<int:produto_id>', methods=['GET', 'POST'])
@require_login
def editar_produto(produto_id):
    """Editar informações do produto"""
    db = get_db()
    user_id = session['user_id']
    
    produto = db.execute('''
        SELECT id, nome, quantidade, preco, categoria
        FROM produtos
        WHERE id = ? AND usuario_id = ?
    ''', (produto_id, user_id)).fetchone()
    
    if not produto:
        flash('Produto não encontrado.', 'error')
        return redirect(url_for('estoque'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        quantidade = int(request.form.get('quantidade', 0))
        preco = float(request.form.get('preco', 0))
        categoria = request.form.get('categoria')
        
        if nome and quantidade >= 0 and preco > 0:
            db.execute('''
                UPDATE produtos
                SET nome = ?, quantidade = ?, preco = ?, categoria = ?
                WHERE id = ? AND usuario_id = ?
            ''', (nome, quantidade, preco, categoria, produto_id, user_id))
            db.commit()
            flash(f'Produto atualizado com sucesso!', 'success')
            return redirect(url_for('estoque'))
    
    return render_template('editar_produto.html', produto=produto)

@app.route('/estoque/deletar/<int:produto_id>', methods=['POST'])
@require_login
def deletar_produto(produto_id):
    """Deletar produto do estoque"""
    db = get_db()
    user_id = session['user_id']
    
    db.execute('''
        DELETE FROM produtos
        WHERE id = ? AND usuario_id = ?
    ''', (produto_id, user_id))
    db.commit()
    
    flash('Produto deletado com sucesso!', 'success')
    return redirect(url_for('estoque'))

@app.route('/vendas')
@require_login
def vendas():
    """Página de histórico de vendas"""
    db = get_db()
    user_id = session['user_id']
    
    pagina = request.args.get('pagina', 1, type=int)
    itens_por_pagina = 10
    offset = (pagina - 1) * itens_por_pagina
    
    vendas = db.execute('''
        SELECT v.id, v.data_venda, v.valor_total, COUNT(iv.id) as quantidade_itens
        FROM vendas v
        LEFT JOIN itens_venda iv ON v.id = iv.venda_id
        WHERE v.usuario_id = ?
        GROUP BY v.id
        ORDER BY v.data_venda DESC
        LIMIT ? OFFSET ?
    ''', (user_id, itens_por_pagina, offset)).fetchall()
    
    total_vendas = db.execute('''
        SELECT COUNT(DISTINCT v.id) FROM vendas v
        WHERE v.usuario_id = ?
    ''', (user_id,)).fetchone()[0]
    
    total_paginas = (total_vendas + itens_por_pagina - 1) // itens_por_pagina
    
    return render_template('vendas.html',
                         vendas=vendas,
                         pagina_atual=pagina,
                         total_paginas=total_paginas)

@app.route('/vendas/nova', methods=['GET', 'POST'])
@require_login
def nova_venda():
    """Registrar nova venda"""
    db = get_db()
    user_id = session['user_id']
    
    if request.method == 'POST':
        # Obter dados do formulário
        cliente_nome = request.form.get('cliente_nome')
        produtos_selecionados = request.form.getlist('produto_id')
        quantidades = request.form.getlist('quantidade')
        
        if not produtos_selecionados:
            flash('Selecione pelo menos um produto.', 'error')
            return render_template('nova_venda.html',
                                 produtos=db.execute('''
                                     SELECT id, nome, preco FROM produtos
                                     WHERE usuario_id = ? AND quantidade > 0
                                     ORDER BY nome
                                 ''', (user_id,)).fetchall())
        
        valor_total = 0
        itens_venda = []
        
        # Validar e calcular valor total
        for prod_id, qtd in zip(produtos_selecionados, quantidades):
            qtd = int(qtd)
            produto = db.execute('''
                SELECT id, nome, quantidade, preco FROM produtos
                WHERE id = ? AND usuario_id = ?
            ''', (prod_id, user_id)).fetchone()
            
            if not produto or produto[2] < qtd:
                flash(f'Estoque insuficiente para {produto[1]}.', 'error')
                return render_template('nova_venda.html',
                                     produtos=db.execute('''
                                         SELECT id, nome, preco FROM produtos
                                         WHERE usuario_id = ? AND quantidade > 0
                                         ORDER BY nome
                                     ''', (user_id,)).fetchall())
            
            itens_venda.append((prod_id, qtd, produto[3]))
            valor_total += qtd * produto[3]
        
        # Registrar venda
        cursor = db.execute('''
            INSERT INTO vendas (usuario_id, valor_total, cliente_nome)
            VALUES (?, ?, ?)
        ''', (user_id, valor_total, cliente_nome or 'Cliente Padrão'))
        db.commit()
        venda_id = cursor.lastrowid
        
        # Registrar itens da venda e atualizar estoque
        for prod_id, qtd, preco in itens_venda:
            # Garantir tipos e calcular subtotal (Correção do IntegrityError)
            qtd_int = int(qtd)
            preco_float = float(preco)
            subtotal = round(qtd_int * preco_float, 2)
            
            # Log de diagnóstico temporário
            print(f"[DEBUG] Inserindo Item: Venda={venda_id}, Prod={prod_id}, Qtd={qtd_int}, Preço={preco_float}, Subtotal={subtotal}")
            
            db.execute('''
                INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?)
            ''', (venda_id, prod_id, qtd_int, preco_float, subtotal))
            
            db.execute('''
                UPDATE produtos
                SET quantidade = quantidade - ?
                WHERE id = ?
            ''', (qtd, prod_id))
        
        db.commit()
        flash(f'Venda registrada com sucesso! ID: {venda_id}', 'success')
        return redirect(url_for('vendas'))
    
    produtos = db.execute('''
        SELECT id, nome, preco, quantidade FROM produtos
        WHERE usuario_id = ? AND quantidade > 0
        ORDER BY nome
    ''', (user_id,)).fetchall()
    
    return render_template('nova_venda.html', produtos=produtos)

@app.route('/clientes')
@require_login
def clientes():
    """Página de gestão inteligente de clientes"""
    user_id = session['user_id']
    
    # Motor de inteligência
    analysis_engine = AnalysisEngine(user_id)
    clientes_data = analysis_engine.obter_clientes_inteligentes()
    insights_clientes = analysis_engine.gerar_insights_clientes()
    
    # Filtro
    filtro = request.args.get('filtro', 'todos')
    if filtro != 'todos':
        mapa_filtros = {
            'vip': 'VIP',
            'regular': 'Regular',
            'esporadico': 'Esporádico',
            'inativo': 'Inativo'
        }
        classificacao_filtro = mapa_filtros.get(filtro)
        if classificacao_filtro:
            clientes_data = [c for c in clientes_data if c['classificacao'] == classificacao_filtro]
    
    # Estatísticas resumidas (sempre do total, não filtrado)
    all_clientes = analysis_engine.obter_clientes_inteligentes()
    total_clientes = len(all_clientes)
    total_vips = len([c for c in all_clientes if c['classificacao'] == 'VIP'])
    total_inativos = len([c for c in all_clientes if c['classificacao'] == 'Inativo'])
    score_medio = round(sum(c['score'] for c in all_clientes) / total_clientes, 1) if total_clientes > 0 else 0
    
    return render_template('clientes.html',
                         clientes=clientes_data,
                         insights_clientes=insights_clientes,
                         filtro_atual=filtro,
                         total_clientes=total_clientes,
                         total_vips=total_vips,
                         total_inativos=total_inativos,
                         score_medio=score_medio)

@app.route('/relatorios')
@require_gerente
@password_confirmation_required
def relatorios():
    """Página de relatórios - Protegida com confirmação de senha"""
    db = get_db()
    user_id = session['user_id']
    
    periodo = request.args.get('periodo', 'mes')
    hoje = datetime.now().date()
    
    if periodo == 'dia':
        data_inicio = hoje
    elif periodo == 'semana':
        data_inicio = hoje - timedelta(days=hoje.weekday())
    else:  # mês
        data_inicio = hoje.replace(day=1)
    
    # Total de vendas
    vendas_periodo = db.execute('''
        SELECT COUNT(id) as total, SUM(valor_total) as valor
        FROM vendas
        WHERE usuario_id = ? AND DATE(data_venda) >= ?
    ''', (user_id, data_inicio)).fetchone()
    
    # Produtos mais vendidos
    top_produtos = db.execute('''
        SELECT p.nome, SUM(iv.quantidade) as total_vendido, SUM(iv.quantidade * iv.preco_unitario) as receita
        FROM itens_venda iv
        JOIN produtos p ON iv.produto_id = p.id
        JOIN vendas v ON iv.venda_id = v.id
        WHERE v.usuario_id = ? AND DATE(v.data_venda) >= ?
        GROUP BY p.id
        ORDER BY total_vendido DESC
        LIMIT 10
    ''', (user_id, data_inicio)).fetchall()
    
    # Produtos com menor saída
    bottom_produtos = db.execute('''
        SELECT p.nome, COALESCE(SUM(iv.quantidade), 0) as total_vendido
        FROM produtos p
        LEFT JOIN itens_venda iv ON p.id = iv.produto_id
        LEFT JOIN vendas v ON iv.venda_id = v.id AND DATE(v.data_venda) >= ?
        WHERE p.usuario_id = ?
        GROUP BY p.id
        ORDER BY total_vendido ASC
        LIMIT 10
    ''', (data_inicio, user_id)).fetchall()
    
    return render_template('relatorios.html',
                         periodo=periodo,
                         vendas_periodo=vendas_periodo,
                         top_produtos=top_produtos,
                         bottom_produtos=bottom_produtos)

# ============= ROTAS DE GESTÃO DE FUNCIONÁRIOS =============

# Centralized logging is now handled by Log.registrar_acao from models.py

@app.route('/funcionarios')
@require_login
def funcionarios():
    """Listar todos os funcionários"""
    db = get_db()
    user_id = session['user_id']
    
    funcionarios = db.execute('''
        SELECT id, nome, email, cargo, data_admissao, ativo, salario, comissao_percentual
        FROM funcionarios
        WHERE usuario_id = ? AND ativo = 1
        ORDER BY nome ASC
    ''', (user_id,)).fetchall()
    
    return render_template('funcionarios.html', funcionarios=funcionarios)

@app.route('/funcionarios/adicionar', methods=['GET', 'POST'])
@require_login
def adicionar_funcionario():
    """Adicionar novo funcionário"""
    if request.method == 'POST':
        db = get_db()
        user_id = session['user_id']
        
        nome = request.form.get('nome')
        email = request.form.get('email')
        cargo = request.form.get('cargo')
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        data_admissao = request.form.get('data_admissao')
        salario = float(request.form.get('salario', 0))
        comissao = float(request.form.get('comissao_percentual', 0))
        
        if not nome or not cargo or not data_admissao:
            flash('Preencha todos os campos obrigatórios.', 'error')
            return render_template('adicionar_funcionario.html')
        
        try:
            cursor = db.execute('''
                INSERT INTO funcionarios (usuario_id, nome, email, cargo, telefone, cpf, 
                                         data_admissao, salario, comissao_percentual)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, nome, email, cargo, telefone, cpf, data_admissao, salario, comissao))
            db.commit()
            
            Log.registrar_acao(user_id, 'CRIAR', 'funcionarios', cursor.lastrowid, f'Funcionário {nome} criado')
            
            flash(f'Funcionário "{nome}" adicionado com sucesso!', 'success')
            return redirect(url_for('funcionarios'))
        except Exception as e:
            flash(f'Erro ao adicionar funcionário: {str(e)}', 'error')
    
    return render_template('adicionar_funcionario.html')

@app.route('/funcionarios/editar/<int:func_id>', methods=['GET', 'POST'])
@require_login
def editar_funcionario(func_id):
    """Editar informações do funcionário"""
    db = get_db()
    user_id = session['user_id']
    
    funcionario = db.execute('''
        SELECT id, nome, email, cargo, telefone, cpf, data_admissao, salario, comissao_percentual
        FROM funcionarios
        WHERE id = ? AND usuario_id = ?
    ''', (func_id, user_id)).fetchone()
    
    if not funcionario:
        flash('Funcionário não encontrado.', 'error')
        return redirect(url_for('funcionarios'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        cargo = request.form.get('cargo')
        telefone = request.form.get('telefone')
        salario = float(request.form.get('salario', 0))
        comissao = float(request.form.get('comissao_percentual', 0))
        
        if not nome or not cargo:
            flash('Preencha todos os campos obrigatórios.', 'error')
            return render_template('editar_funcionario.html', funcionario=funcionario)
        
        db.execute('''
            UPDATE funcionarios
            SET nome = ?, email = ?, cargo = ?, telefone = ?, salario = ?, comissao_percentual = ?
            WHERE id = ? AND usuario_id = ?
        ''', (nome, email, cargo, telefone, salario, comissao, func_id, user_id))
        db.commit()
        
        Log.registrar_acao(user_id, 'ATUALIZAR', 'funcionarios', func_id, f'Funcionário {nome} atualizado')
        
        flash('Funcionário atualizado com sucesso!', 'success')
        return redirect(url_for('funcionarios'))
    
    return render_template('editar_funcionario.html', funcionario=funcionario)

@app.route('/funcionarios/deletar/<int:func_id>', methods=['POST'])
@require_login
def deletar_funcionario(func_id):
    """Desativar funcionário (soft delete)"""
    db = get_db()
    user_id = session['user_id']
    
    funcionario = db.execute('''
        SELECT nome FROM funcionarios
        WHERE id = ? AND usuario_id = ?
    ''', (func_id, user_id)).fetchone()
    
    if funcionario:
        db.execute('''
            UPDATE funcionarios
            SET ativo = 0
            WHERE id = ?
        ''', (func_id,))
        db.commit()
        
        Log.registrar_acao(user_id, 'DELETAR', 'funcionarios', func_id, f'Funcionário {funcionario[0]} desativado')
        flash(f'Funcionário "{funcionario[0]}" desativado com sucesso!', 'success')
    
    return redirect(url_for('funcionarios'))

@app.route('/funcionarios/ranking')
@require_login
def ranking_funcionarios():
    """Ranking de funcionários por vendas"""
    db = get_db()
    user_id = session['user_id']
    
    ranking = db.execute('''
        SELECT f.id, f.nome, f.cargo, COUNT(vf.id) as total_vendas, 
               SUM(v.valor_total) as valor_total, SUM(vf.comissao_ganho) as comissao_total,
               ROUND(AVG(v.valor_total), 2) as ticket_medio
        FROM funcionarios f
        LEFT JOIN vendas_funcionario vf ON f.id = vf.funcionario_id
        LEFT JOIN vendas v ON vf.venda_id = v.id AND v.usuario_id = ?
        WHERE f.usuario_id = ? AND f.ativo = 1
        GROUP BY f.id
        ORDER BY total_vendas DESC
    ''', (user_id, user_id)).fetchall()
    
    # Calcular estatísticas
    total_funcionarios = len(ranking)
    total_vendas = sum(row[3] for row in ranking) if ranking else 0
    total_faturamento = sum(row[4] for row in ranking) if ranking else 0
    
    return render_template('ranking_funcionarios.html', 
                         ranking=ranking,
                         total_funcionarios=total_funcionarios,
                         total_vendas=total_vendas,
                         total_faturamento=total_faturamento)

@app.route('/logs')
@require_gerente
def historico_logs():
    """Histórico de ações (logs)"""
    db = get_db()
    user_id = session['user_id']
    
    pagina = request.args.get('pagina', 1, type=int)
    itens_por_pagina = 20
    offset = (pagina - 1) * itens_por_pagina
    
    logs = db.execute('''
        SELECT l.id, l.tipo_acao, l.tabela, l.descricao, 
               COALESCE(f.nome, 'Sistema') as funcionario_afetado,
               u.nome as usuario_responsavel, l.data_acao
        FROM logs_acao l
        LEFT JOIN funcionarios f ON l.funcionario_id = f.id
        LEFT JOIN usuarios u ON l.usuario_id = u.id
        WHERE l.usuario_id = ?
        ORDER BY l.data_acao DESC
        LIMIT ? OFFSET ?
    ''', (user_id, itens_por_pagina, offset)).fetchall()
    
    total_logs = db.execute('''
        SELECT COUNT(*) FROM logs_acao WHERE usuario_id = ?
    ''', (user_id,)).fetchone()[0]
    
    total_paginas = (total_logs + itens_por_pagina - 1) // itens_por_pagina
    
    return render_template('historico_logs.html',
                         logs=logs,
                         pagina_atual=pagina,
                         total_paginas=total_paginas)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
