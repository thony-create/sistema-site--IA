from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
from functools import wraps
from models import ChatHistorico, User, Log, get_db_context
from ai_module import AnalysisEngine
from permissions import require_login
import json
from datetime import datetime

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

def login_required_for_chat(f):
    """Decorator to require login for chat"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'erro': 'Não autorizado'}), 401
        return f(*args, **kwargs)
    return decorated

@chat_bp.route('/')
@require_login
def index():
    """Chat main page"""
    user_id = session.get('user_id')
    user = User.obter_usuario_por_id(user_id)
    
    # Get recent chat history
    historico = ChatHistorico.obter_historico_usuario(user_id, limite=20)
    historico_invertido = list(reversed(historico)) if historico else []
    
    return render_template('chat/index.html', user=user, historico=historico_invertido)

@chat_bp.route('/api/enviar', methods=['POST'])
@login_required_for_chat
def enviar_pergunta():
    """API endpoint to send question and get response"""
    user_id = session.get('user_id')
    
    try:
        data = request.get_json()
        pergunta = data.get('pergunta', '').strip()
        
        if not pergunta:
            return jsonify({'erro': 'Pergunta vazia'}), 400
        
        if len(pergunta) > 500:
            return jsonify({'erro': 'Pergunta muito longa (máximo 500 caracteres)'}), 400
        
        # Generate response using AnalysisEngine
        engine = AnalysisEngine(user_id)
        resposta = engine.analisar_pergunta(pergunta)
        
        # Save to chat history
        tipo_pergunta = classificar_pergunta(pergunta)
        ChatHistorico.salvar_conversa(user_id, pergunta, resposta, tipo_pergunta)
        
        # Log the action
        Log.registrar_acao(user_id, 'CHAT_PERGUNTA', 'chat_historico', user_id, 
                         f'Pergunta: {pergunta[:50]}...')
        
        return jsonify({
            'sucesso': True,
            'pergunta': pergunta,
            'resposta': resposta,
            'tipo': tipo_pergunta,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@chat_bp.route('/api/historico')
@login_required_for_chat
def obter_historico():
    """API endpoint to get chat history"""
    user_id = session.get('user_id')
    pagina = request.args.get('pagina', 1, type=int)
    limite = request.args.get('limite', 50, type=int)
    
    # Get all history
    historico = ChatHistorico.obter_historico_usuario(user_id, limite=limite)
    
    historico_formatado = []
    for chat in historico:
        historico_formatado.append({
            'id': chat['id'],
            'pergunta': chat['pergunta'],
            'resposta': chat['resposta'],
            'tipo': chat['tipo_pergunta'],
            'data': chat['data_criacao'],
            'timestamp': datetime.fromisoformat(chat['data_criacao']).strftime('%d/%m/%Y %H:%M:% S')
        })
    
    return jsonify({
        'sucesso': True,
        'historico': historico_formatado,
        'total': len(historico_formatado)
    })

@chat_bp.route('/api/sugestoes')
@login_required_for_chat
def obter_sugestoes():
    """API endpoint to get chat suggestions"""
    user_id = session.get('user_id')
    user = User.obter_usuario_por_id(user_id)
    
    try:
        engine = AnalysisEngine(user_id)
        
        # Get key metrics for suggestions
        sugestoes = [
            {
                'titulo': 'Vendas de Hoje',
                'pergunta': 'Quanto eu vendi hoje?',
                'icon': 'bar-chart',
                'categoria': 'vendas'
            },
            {
                'titulo': 'Produto Mais Vendido',
                'pergunta': 'Qual meu produto mais vendido?',
                'icon': 'trophy',
                'categoria': 'produtos'
            },
            {
                'titulo': 'Estoque Baixo',
                'pergunta': 'Qual produto está com estoque baixo?',
                'icon': 'alert-triangle',
                'categoria': 'estoque'
            },
            {
                'titulo': 'Total em Estoque',
                'pergunta': 'Quanto eu tenho em estoque?',
                'icon': 'packages',
                'categoria': 'estoque'
            },
            {
                'titulo': 'Faturamento da Semana',
                'pergunta': 'Quanto vendi nesta semana?',
                'icon': 'trending-up',
                'categoria': 'vendas'
            },
            {
                'titulo': 'Clientes',
                'pergunta': 'Quantos clientes eu tenho?',
                'icon': 'users',
                'categoria': 'clientes'
            },
            {
                'titulo': 'Previsão de Estoque',
                'pergunta': 'Quando meu estoque vai acabar?',
                'icon': 'calendar',
                'categoria': 'previsao'
            },
            {
                'titulo': 'Recomendações',
                'pergunta': 'Que sugestões você tem para mim?',
                'icon': 'lightbulb',
                'categoria': 'insights'
            }
        ]
        
        return jsonify({
            'sucesso': True,
            'sugestoes': sugestoes
        })
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@chat_bp.route('/api/limpar-historico', methods=['POST'])
@login_required_for_chat
def limpar_historico():
    """API endpoint to clear chat history"""
    user_id = session.get('user_id')
    
    try:
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM chat_historico WHERE usuario_id = ?', (user_id,))
        
        Log.registrar_acao(user_id, 'LIMPAR_CHAT', 'chat_historico', user_id, 'Histórico de chat limpo')
        
        return jsonify({
            'sucesso': True,
            'mensagem': 'Histórico de chat limpo com sucesso'
        })
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@chat_bp.route('/api/exportar-historico')
@login_required_for_chat
def exportar_historico():
    """API endpoint to export chat history as JSON"""
    user_id = session.get('user_id')
    
    try:
        historico = ChatHistorico.obter_historico_usuario(user_id, limite=1000)
        
        historico_formatado = []
        for chat in historico:
            historico_formatado.append({
                'pergunta': chat['pergunta'],
                'resposta': chat['resposta'],
                'tipo': chat['tipo_pergunta'],
                'data': chat['data_criacao']
            })
        
        return jsonify({
            'sucesso': True,
            'exportacao': json.dumps(historico_formatado, ensure_ascii=False, indent=2),
            'data_exportacao': datetime.now().isoformat(),
            'total_registros': len(historico_formatado)
        })
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@chat_bp.route('/api/insights-rapidos')
@login_required_for_chat
def insights_rapidos():
    """API endpoint to get quick insights for chat sidebar"""
    user_id = session.get('user_id')
    
    try:
        engine = AnalysisEngine(user_id)
        
        # Get quick insights
        with get_db_context() as conn:
            cursor = conn.cursor()
            
            # Today's sales
            vendas_hoje = cursor.execute('''
                SELECT COALESCE(SUM(valor_total), 0) FROM vendas
                WHERE usuario_id = ? AND DATE(data_venda) = DATE('now')
            ''', (user_id,)).fetchone()[0]
            
            # Total sales
            total_vendas = cursor.execute('''
                SELECT COUNT(*) FROM vendas WHERE usuario_id = ?
            ''', (user_id,)).fetchone()[0]
            
            # Clients
            total_clientes = cursor.execute('''
                SELECT COUNT(DISTINCT cliente_nome) FROM vendas WHERE usuario_id = ?
            ''', (user_id,)).fetchone()[0]
            
            # Low stock
            estoque_baixo = cursor.execute('''
                SELECT COUNT(*) FROM produtos
                WHERE usuario_id = ? AND quantidade < 10
            ''', (user_id,)).fetchone()[0]
        
        return jsonify({
            'sucesso': True,
            'vendas_hoje': round(vendas_hoje, 2),
            'total_vendas': total_vendas,
            'total_clientes': total_clientes,
            'estoque_baixo': estoque_baixo
        })
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

def classificar_pergunta(pergunta):
    """Classify question type based on keywords"""
    pergunta_lower = pergunta.lower()
    
    # Classification patterns
    patterns = {
        'vendas': ['vendi', 'venda', 'faturamento', 'faturei', 'receita', 'quanto vendi'],
        'produtos': ['produto', 'melhores', 'destaque', 'mais vendido'],
        'estoque': ['estoque', 'quantidade', 'stock', 'quantidade', 'estoque baixo'],
        'clientes': ['cliente', 'clientes', 'quantos clientes', 'meus clientes'],
        'financeiro': ['lucro', 'ganho', 'ganhos', 'margem', 'custo', 'preço'],
        'previsao': ['quando', 'vai acabar', 'previsão', 'próximos dias'],
        'comportamento': ['crescimento', 'tendência', 'padrão', 'frequência'],
        'geral': ['ajuda', 'sugestão', 'recomendação', 'o que fazer']
    }
    
    # Check which pattern matches
    for tipo, palavras in patterns.items():
        if any(palavra in pergunta_lower for palavra in palavras):
            return tipo
    
    return 'outro'

@chat_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors in chat blueprint"""
    return jsonify({'erro': 'Página não encontrada'}), 404

@chat_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors in chat blueprint"""
    return jsonify({'erro': 'Erro interno do servidor'}), 500
