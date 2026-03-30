"""
Zyra - Inteligência Artificial Consultiva
Análises inteligentes, previsões e recomendações do Cognix
"""

from flask import Blueprint, jsonify, request, session
from datetime import datetime, timedelta
from models import get_db
from config import Config
import json
from functools import wraps

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ia')

def login_required_api(f):
    """Decorator para proteger rotas de API que requerem login"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'erro': 'Não autorizado'}), 401
        return f(*args, **kwargs)
    return decorated

class AnalysisEngine:
    """
    Zyra - O cérebro inteligente do Cognix
    Gera insights automáticos baseados em padrões de dados reais
    """
    
    def __init__(self, usuario_id):
        self.usuario_id = usuario_id
        self.db = get_db()
        self.hoje = datetime.now().date()
        self.ontem = self.hoje - timedelta(days=1)
        self.ultima_semana = self.hoje - timedelta(days=7)
        self.ultimo_mes = self.hoje - timedelta(days=30)
    
    def _get_faturamento(self, data_inicio, data_fim=None):
        """Obter faturamento em um período"""
        if data_fim is None:
            data_fim = self.hoje
        
        return self.db.execute('''
            SELECT COALESCE(SUM(valor_total), 0)
            FROM vendas
            WHERE usuario_id = ? AND DATE(data_venda) >= ? AND DATE(data_venda) <= ?
        ''', (self.usuario_id, data_inicio, data_fim)).fetchone()[0]
    
    def _get_quantidade_vendas(self, data_inicio, data_fim=None):
        """Obter quantidade de vendas em um período"""
        if data_fim is None:
            data_fim = self.hoje
        
        return self.db.execute('''
            SELECT COUNT(*) FROM vendas
            WHERE usuario_id = ? AND DATE(data_venda) >= ? AND DATE(data_venda) <= ?
        ''', (self.usuario_id, data_inicio, data_fim)).fetchone()[0]
    
    def gerar_insights(self):
        """
        Gerar insights automáticos sobre o negócio
        Analisa tendências, padrões e oportunidades
        """
        insights = []
        
        # Verificar se há dados suficientes
        vendas_total = self.db.execute('''
            SELECT COUNT(*) FROM vendas WHERE usuario_id = ?
        ''', (self.usuario_id,)).fetchone()[0]
        
        if vendas_total < Config.AI_MIN_DADOS_PARA_ANALISE:
            return [{
                'titulo': 'Mais Dados para a Zyra',
                'descricao': f'A Zyra precisa de mais {Config.AI_MIN_DADOS_PARA_ANALISE - vendas_total} vendas para gerar insights automáticos.',
                'tipo': 'info',
                'urgencia': 'baixa'
            }]
        
        # Análise 1: Crescimento/Queda de Vendas
        insights.extend(self._analisar_crescimento_vendas())
        
        # Análise 2: Estoque Crítico
        insights.extend(self._analisar_estoque_critico())
        
        # Análise 3: Produtos Destaque
        insights.extend(self._analisar_produtos_destaque())
        
        # Análise 4: Produtos com Baixa Rotação
        insights.extend(self._analisar_baixa_rotacao())
        
        # Análise 5: Tendências de Venda
        insights.extend(self._analisar_tendencias())
        
        # Análise 6: Oportunidades de Receita
        insights.extend(self._analisar_oportunidades())
        
        return insights if insights else [{
            'titulo': 'Negócio Estável',
            'descricao': 'Seu negócio está operando normalmente. Continue monitorando.',
            'tipo': 'success',
            'urgencia': 'baixa'
        }]
    
    def _analisar_crescimento_vendas(self):
        """Analisar crescimento/queda de vendas"""
        insights = []
        
        faturamento_hoje = self._get_faturamento(self.hoje)
        faturamento_ontem = self._get_faturamento(self.ontem)
        faturamento_semana_anterior = self._get_faturamento(
            self.ultima_semana - timedelta(days=7),
            self.ultima_semana
        )
        faturamento_semana_atual = self._get_faturamento(self.ultima_semana)
        
        # Comparação diária
        if faturamento_ontem > 0:
            crescimento_diario = ((faturamento_hoje - faturamento_ontem) / faturamento_ontem) * 100
            
            if crescimento_diario > 30:
                insights.append({
                    'titulo': '🚀 Excelente Crescimento!',
                    'descricao': f'Vendas subiram {crescimento_diario:.1f}% hoje em relação a ontem!',
                    'tipo': 'success',
                    'urgencia': 'alta',
                    'valor': f'+{crescimento_diario:.1f}%'
                })
            elif crescimento_diario > 10:
                insights.append({
                    'titulo': '📈 Crescimento de Vendas',
                    'descricao': f'Você teve {crescimento_diario:.1f}% de crescimento em relação a ontem.',
                    'tipo': 'success',
                    'urgencia': 'media',
                    'valor': f'+{crescimento_diario:.1f}%'
                })
            elif crescimento_diario < -30:
                insights.append({
                    'titulo': 'Queda Acentuada de Vendas',
                    'descricao': f'Atenção: vendas caíram {abs(crescimento_diario):.1f}% em relação a ontem. Investigue as causas.',
                    'tipo': 'warning',
                    'urgencia': 'alta',
                    'valor': f'{crescimento_diario:.1f}%'
                })
            elif crescimento_diario < -10:
                insights.append({
                    'titulo': 'Queda de Vendas',
                    'descricao': f'Vendas caíram {abs(crescimento_diario):.1f}% em relação a ontem.',
                    'tipo': 'warning',
                    'urgencia': 'media',
                    'valor': f'{crescimento_diario:.1f}%'
                })
        
        # Comparação semanal
        if faturamento_semana_anterior > 0:
            crescimento_semanal = ((faturamento_semana_atual - faturamento_semana_anterior) / faturamento_semana_anterior) * 100
            
            if crescimento_semanal > Config.AI_THRESHOLD_CRESCIMENTO * 100:
                insights.append({
                    'titulo': '💰 Semana em Alta',
                    'descricao': f'Esta semana vendeu {crescimento_semanal:.1f}% mais que a anterior!',
                    'tipo': 'success',
                    'urgencia': 'media',
                    'valor': f'+{crescimento_semanal:.1f}%'
                })
        
        return insights
    
    def _analisar_estoque_critico(self):
        """Analisar produtos com estoque crítico"""
        insights = []
        
        # Produtos com estoque muito baixo
        produtos_criticos = self.db.execute('''
            SELECT id, nome, quantidade FROM produtos
            WHERE usuario_id = ? AND quantidade <= 3
            ORDER BY quantidade ASC
        ''', (self.usuario_id,)).fetchall()
        
        produtos_baixo = self.db.execute('''
            SELECT COUNT(*) FROM produtos
            WHERE usuario_id = ? AND quantidade > 3 AND quantidade < 10
        ''', (self.usuario_id,)).fetchone()[0]
        
        if produtos_criticos:
            nomes = ', '.join([f'"{p[1]}" ({p[2]} unidades)' for p in produtos_criticos[:3]])
            insights.append({
                'titulo': '🚨 Estoque Crítico',
                'descricao': f'URGENTE: {nomes} estão acabando! Reponha imediatamente.',
                'tipo': 'danger',
                'urgencia': 'critica'
            })
        
        if produtos_baixo > 0:
            insights.append({
                'titulo': 'Estoque Baixo',
                'descricao': f'{produtos_baixo} produto(s) com estoque reduzido. Considere reposição em breve.',
                'tipo': 'warning',
                'urgencia': 'alta'
            })
        
        return insights
    
    def _analisar_produtos_destaque(self):
        """Analisar produtos que estão vendendo bem"""
        insights = []
        
        # Top 3 produtos da semana
        top_produtos = self.db.execute('''
            SELECT p.nome, SUM(iv.quantidade) as total_qtd, 
                   SUM(iv.quantidade * iv.preco_unitario) as receita
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            JOIN vendas v ON iv.venda_id = v.id
            WHERE v.usuario_id = ? AND DATE(v.data_venda) >= ?
            GROUP BY p.id
            ORDER BY total_qtd DESC
            LIMIT 3
        ''', (self.usuario_id, self.ultima_semana)).fetchall()
        
        if top_produtos:
            top_1 = top_produtos[0]
            insights.append({
                'titulo': 'Produto Destaque',
                'descricao': f'"{top_1[0]}" é seu campeão! {top_1[1]} unidades vendidas (R$ {top_1[2]:.2f})',
                'tipo': 'success',
                'urgencia': 'media'
            })
        
        return insights
    
    def _analisar_baixa_rotacao(self):
        """Analisar produtos com baixa rotação"""
        insights = []
        
        # Produtos que nunca venderam ou vendem muito pouco
        sem_vendas = self.db.execute('''
            SELECT COUNT(*) FROM produtos p
            WHERE p.usuario_id = ? AND p.id NOT IN (
                SELECT DISTINCT iv.produto_id
                FROM itens_venda iv
                JOIN vendas v ON iv.venda_id = v.id
                WHERE v.usuario_id = ?
            )
        ''', (self.usuario_id, self.usuario_id)).fetchone()[0]
        
        if sem_vendas > 0:
            insights.append({
                'titulo': '📦 Produtos Sem Vendas',
                'descricao': f'{sem_vendas} produto(s) ainda não foram vendidos. Revise preços ou remova do catálogo.',
                'tipo': 'info',
                'urgencia': 'media'
            })
        
        return insights
    
    def _analisar_tendencias(self):
        """Analisar tendências e padrões"""
        insights = []
        
        # Número de vendas nos últimos 7 dias
        vendas_ultima_semana = self._get_quantidade_vendas(self.ultima_semana)
        vendas_semana_anterior = self._get_quantidade_vendas(
            self.ultima_semana - timedelta(days=7),
            self.ultima_semana
        )
        
        if vendas_semana_anterior > 0:
            crescimento_freq = ((vendas_ultima_semana - vendas_semana_anterior) / vendas_semana_anterior) * 100
            
            if crescimento_freq > 20:
                insights.append({
                    'titulo': '📊 Frequência de Vendas em Alta',
                    'descricao': f'Número de vendas aumentou {crescimento_freq:.1f}% na última semana.',
                    'tipo': 'success',
                    'urgencia': 'baixa'
                })
        
        # Ticket médio
        ticket_medio = self.db.execute('''
            SELECT AVG(valor_total) FROM vendas
            WHERE usuario_id = ? AND DATE(data_venda) >= ?
        ''', (self.usuario_id, self.ultima_semana)).fetchone()[0]
        
        if ticket_medio and ticket_medio > 100:
            insights.append({
                'titulo': '💵 Ticket Médio Alto',
                'descricao': f'Seu ticket médio é de R$ {ticket_medio:.2f}. Mantenha este padrão!',
                'tipo': 'success',
                'urgencia': 'baixa'
            })
        
        return insights
    
    def _analisar_oportunidades(self):
        """Analisar oportunidades de maximização de receita"""
        insights = []
        
        # Produtos mais vendidos - oportunidade de aumentar preço
        top_vendido = self.db.execute('''
            SELECT p.id, p.nome, SUM(iv.quantidade), p.preco
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            JOIN vendas v ON iv.venda_id = v.id
            WHERE v.usuario_id = ? AND DATE(v.data_venda) >= ?
            GROUP BY p.id
            ORDER BY SUM(iv.quantidade) DESC
            LIMIT 1
        ''', (self.usuario_id, self.ultimo_mes)).fetchone()
        
        if top_vendido and top_vendido[2] > 5:
            insights.append({
                'titulo': 'Maximize a Receita',
                'descricao': f'"{top_vendido[1]}" é ultra vendido ({top_vendido[2]} unidades). Um pequeno aumento de preço pode maximizar lucro.',
                'tipo': 'info',
                'urgencia': 'media'
            })
        
        # Média de itens por venda
        media_itens = self.db.execute('''
            SELECT AVG(total_itens) FROM (
                SELECT COUNT(iv.id) as total_itens FROM itens_venda iv
                JOIN vendas v ON iv.venda_id = v.id
                WHERE v.usuario_id = ? AND DATE(v.data_venda) >= ?
                GROUP BY v.id
            ) AS vendas_agrupadas
        ''', (self.usuario_id, self.ultima_semana)).fetchone()[0]
        
        if media_itens and media_itens < 1.5:
            insights.append({
                'titulo': '🎯 Cross-selling Opportunity',
                'descricao': f'Média de {media_itens:.1f} itens/venda. Tente vender produtos complementares.',
                'tipo': 'info',
                'urgencia': 'media'
            })
        
        return insights
    
    def prever_falta_estoque(self):
        """Prever quando cada produto vai acabar"""
        predicoes = []
        
        # Obter taxa de venda média dos últimos 7 dias
        produtos = self.db.execute('''
            SELECT id, nome, quantidade FROM produtos
            WHERE usuario_id = ?
        ''', (self.usuario_id,)).fetchall()
        
        data_inicio = datetime.now().date() - timedelta(days=7)
        
        for produto in produtos:
            produto_id, nome, qtd_atual = produto
            
            # Calcular velocidade de venda
            vendas_7dias = self.db.execute('''
                SELECT COALESCE(SUM(iv.quantidade), 0)
                FROM itens_venda iv
                JOIN vendas v ON iv.venda_id = v.id
                WHERE v.usuario_id = ? AND iv.produto_id = ? AND DATE(v.data_venda) >= ?
            ''', (self.usuario_id, produto_id, data_inicio)).fetchone()[0]
            
            if vendas_7dias > 0:
                velocidade_diaria = vendas_7dias / 7
                dias_para_acabar = qtd_atual / velocidade_diaria if velocidade_diaria > 0 else float('inf')
                
                if dias_para_acabar <= 7:
                    predicoes.append({
                        'produto': nome,
                        'dias_restantes': int(dias_para_acabar),
                        'quantidade_atual': qtd_atual,
                        'velocidade_diaria': round(velocidade_diaria, 2)
                    })
        
        return sorted(predicoes, key=lambda x: x['dias_restantes'])
    
    def gerar_recomendacoes(self):
        """Gerar recomendações inteligentes atuando como Consultora de Negócios"""
        recomendacoes = []
        
        # 1. Reposição de Estoque (Produtos mais vendidos com estoque crítico)
        top_produtos = self.db.execute('''
            SELECT p.id, p.nome, SUM(iv.quantidade) as total_vendido, p.quantidade as estoque_atual
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            JOIN vendas v ON iv.venda_id = v.id
            WHERE v.usuario_id = ? AND DATE(v.data_venda) >= ?
            GROUP BY p.id
            ORDER BY total_vendido DESC
            LIMIT 3
        ''', (self.usuario_id, datetime.now().date() - timedelta(days=30))).fetchall()
        
        for p in top_produtos:
            # Se é um top produto mas o estoque atual é <= 10
            if p[3] <= 10:
                recomendacoes.append({
                    'titulo': 'Oportunidade de Reposição',
                    'icone': 'fa-boxes',
                    'mensagem': f'A Zyra recomenda aumentar o estoque do produto "{p[1]}". Ele é um dos seus mais vendidos e está quase esgotando ({p[3]} unidades restantes).',
                    'tipo': 'success'
                })
                break # Apenas uma recomendação de estoque para não poluir

        # 2. Foco de Venda (Produtos Parados há muito tempo)
        sem_vendas = self.db.execute('''
            SELECT p.nome FROM produtos p
            WHERE p.usuario_id = ? AND p.ativo = 1 AND p.quantidade > 0 AND p.id NOT IN (
                SELECT DISTINCT iv.produto_id
                FROM itens_venda iv
                JOIN vendas v ON iv.venda_id = v.id
                WHERE v.usuario_id = ? AND DATE(v.data_venda) >= ?
            )
            LIMIT 1
        ''', (self.usuario_id, self.usuario_id, datetime.now().date() - timedelta(days=30))).fetchone()
        
        if sem_vendas:
            recomendacoes.append({
                'titulo': 'Foco de Vendas',
                'icone': 'fa-bullseye',
                'mensagem': f'A Zyra recomenda focar nas vendas do produto "{sem_vendas[0]}", que está sem saída há mais de 30 dias. Considere criar uma promoção ou combo com outros itens.',
                'tipo': 'warning'
            })

        # 3. Desempenho por Categoria / Melhoria de Desempenho
        desempenho_categorias = self.db.execute('''
            SELECT c.nome, SUM(iv.quantidade * iv.preco_unitario) as receita
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            JOIN categorias c ON p.categoria_id = c.id
            JOIN vendas v ON iv.venda_id = v.id
            WHERE v.usuario_id = ? AND DATE(v.data_venda) >= ?
            GROUP BY c.id
            ORDER BY receita ASC
            LIMIT 1
        ''', (self.usuario_id, datetime.now().date() - timedelta(days=30))).fetchone()
        
        if desempenho_categorias and desempenho_categorias[1] < 1000: # Exemplo de threshold
            recomendacoes.append({
                'titulo': 'Melhoria de Desempenho',
                'icone': 'fa-chart-pie',
                'mensagem': f'A Zyra notou que a categoria "{desempenho_categorias[0]}" está com o menor faturamento (R$ {desempenho_categorias[1]:.2f}). Recomendo criar ações de marketing direcionadas para este segmento.',
                'tipo': 'info'
            })

        return recomendacoes
    
    def gerar_dados_graficos(self):
        """Gerar dados para gráficos no dashboard"""
        # Vendas dos últimos 7 dias
        data_inicio = datetime.now().date() - timedelta(days=6)
        
        vendas_7dias = []
        despesas_7dias = []
        for i in range(7):
            data = data_inicio + timedelta(days=i)
            # Faturamento
            valor_venda = self.db.execute('''
                SELECT COALESCE(SUM(valor_total), 0)
                FROM vendas
                WHERE usuario_id = ? AND DATE(data_venda) = ?
            ''', (self.usuario_id, data)).fetchone()[0]
            
            # Despesas
            valor_despesa = self.db.execute('''
                SELECT COALESCE(SUM(valor), 0)
                FROM despesas
                WHERE usuario_id = ? AND DATE(data_despesa) = ?
            ''', (self.usuario_id, data)).fetchone()[0]
            
            vendas_7dias.append({
                'data': data.strftime('%d/%m'),
                'valor': float(valor_venda)
            })
            despesas_7dias.append({
                'data': data.strftime('%d/%m'),
                'valor': float(valor_despesa)
            })
        
        # Top 5 produtos
        top_produtos = self.db.execute('''
            SELECT p.nome, SUM(iv.quantidade) as total
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            JOIN vendas v ON iv.venda_id = v.id
            WHERE v.usuario_id = ?
            GROUP BY p.id
            ORDER BY total DESC
            LIMIT 5
        ''', (self.usuario_id,)).fetchall()
        
        return {
            'vendas_7dias': vendas_7dias,
            'despesas_7dias': despesas_7dias,
            'top_produtos': [{'nome': p[0], 'quantidade': p[1]} for p in top_produtos]
        }
    
    def gerar_alertas_proativos(self):
        """Gerar alertas automáticos sobre a saúde do negócio (Zyra Proativa)"""
        alertas = []

        # 1. Estoque Baixo ou Esgotado
        produtos_baixos = self.db.execute('''
            SELECT nome, quantidade, estoque_minimo FROM produtos
            WHERE usuario_id = ? AND quantidade <= COALESCE(estoque_minimo, 5) AND ativo = 1
        ''', (self.usuario_id,)).fetchall()
        
        for p in produtos_baixos:
            if p[1] <= 0:
                alertas.append({
                    'tipo': 'danger',
                    'icone': 'fa-triangle-exclamation',
                    'mensagem': f'A Zyra detectou que o produto "{p[0]}" está esgotado! Reponha urgente.'
                })
            else:
                alertas.append({
                    'tipo': 'warning',
                    'icone': 'fa-box-open',
                    'mensagem': f'O produto "{p[0]}" está com estoque baixo ({p[1]} unidades). Considere comprar mais.'
                })

        # 2. Dias sem venda
        ultima_venda = self.db.execute('''
            SELECT data_venda FROM vendas
            WHERE usuario_id = ?
            ORDER BY data_venda DESC LIMIT 1
        ''', (self.usuario_id,)).fetchone()
        
        if ultima_venda:
            from datetime import datetime
            data_ultima = datetime.strptime(ultima_venda[0][:10], '%Y-%m-%d').date()
            dias_sem_vender = (self.hoje - data_ultima).days
            if dias_sem_vender >= 2:
                alertas.append({
                    'tipo': 'warning',
                    'icone': 'fa-calendar-xmark',
                    'mensagem': f'Atenção: Já se passaram {dias_sem_vender} dias desde a sua última venda. Vamos movimentar o negócio?'
                })

        # 3. Tendência de Vendas (Aumento repentino ou Quêda)
        faturamento_semana_atual = self._get_faturamento(self.ultima_semana)
        faturamento_semana_anterior = self._get_faturamento(
            self.ultima_semana - timedelta(days=7),
            self.ultima_semana
        )

        if faturamento_semana_anterior > 0:
            crescimento = ((faturamento_semana_atual - faturamento_semana_anterior) / faturamento_semana_anterior) * 100
            if crescimento > 30:
                alertas.append({
                    'tipo': 'success',
                    'icone': 'fa-arrow-trend-up',
                    'mensagem': f'Que sucesso! O faturamento dos últimos 7 dias foi {crescimento:.1f}% maior que o período anterior.'
                })
            elif crescimento < -20:
                alertas.append({
                    'tipo': 'danger',
                    'icone': 'fa-arrow-trend-down',
                    'mensagem': f'Alerta de queda: O faturamento caiu {abs(crescimento):.1f}% essa semana. É hora de fazer uma promoção?'
                })

        # 4. Produto Destaque do dia (se houver vendas expressivas hoje)
        produto_top_hoje = self.db.execute('''
            SELECT p.nome, COUNT(iv.id) as vendas, SUM(iv.quantidade) as qtd_vendida
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            JOIN vendas v ON iv.venda_id = v.id
            WHERE v.usuario_id = ? AND DATE(v.data_venda) = ?
            GROUP BY p.id
            HAVING qtd_vendida >= 2
            ORDER BY qtd_vendida DESC LIMIT 1
        ''', (self.usuario_id, self.hoje)).fetchone()

        if produto_top_hoje:
            alertas.append({
                'tipo': 'success',
                'icone': 'fa-star',
                'mensagem': f'Produto em destaque! "{produto_top_hoje[0]}" está saindo bastante hoje ({produto_top_hoje[2]} vendidos).'
            })

        return alertas

    def analisar_pergunta(self, pergunta):
        """
        Analisar uma pergunta em linguagem natural usando processamento baseada em intenções.
        Organizado por: Saudações, Cálculos, Negócios, Fallback.
        """
        import re
        try:
            p = pergunta.lower().strip()
            
            # 1. ── SAUDAÇÕES ──────────────────────────────────────────────────
            saudacoes = {
                r'\b(oi|ola|olá|ei|hey|hello|hi)\b': 
                    'Oi! Eu sou a Zyra, sua consultora inteligente. Posso analisar suas vendas, estoque, clientes e muito mais. Como posso te ajudar hoje? 😊',
                r'\b(bom dia|bomdia)\b': 
                    'Bom dia! Aqui é a Zyra. O que vamos analisar hoje? Estou pronta para mergulhar nos seus dados de vendas e estoque. ☀️',
                r'\b(boa tarde|boatarde)\b': 
                    'Boa tarde! Sou a Zyra. Vamos ver como está o desempenho do seu negócio agora? ⛅',
                r'\b(boa noite|boanoite)\b': 
                    'Boa noite! Zyra aqui. Antes de encerrar, quer um resumo rápido do faturamento de hoje? 🌙',
                r'\b(tudo bem|tudo bom|como vai)\b': 
                    'Estou ótima! A Zyra está pronta para ajudar você a gerir o Cognix. O que gostaria de saber?',
                r'\b(obrigado|obrigada|valeu|thanks|show)\b': 
                    'De nada! A Zyra está sempre aqui para facilitar sua gestão no Cognix. Até a próxima! 🚀'
            }
            
            for pattern, response in saudacoes.items():
                if re.search(pattern, p):
                    return response

            # 2. ── CÁLCULOS MATEMÁTICOS SIMPLES ──────────────────────────────
            # Detecta expressões como "1+1", "2 * 2", "10 - 5", "20 / 2"
            # Regex: números seguidos de operados (+,-,*,/) seguidos de números
            math_match = re.search(r'(\d+)\s*([\+\-\*\/])\s*(\d+)', p)
            if math_match:
                n1 = float(math_match.group(1))
                op = math_match.group(2)
                n2 = float(math_match.group(3))
                
                resultado = 0
                if op == '+': resultado = n1 + n2
                elif op == '-': resultado = n1 - n2
                elif op == '*': resultado = n1 * n2
                elif op == '/': 
                    if n2 == 0: return "Não consigo dividir por zero, nem mesmo sendo uma IA! 😊"
                    resultado = n1 / n2
                
                # Formatar resultado (remover .0 se for inteiro)
                res_str = f"{resultado:g}"
                return f"O resultado de **{math_match.group(0)}** é **{res_str}**. 🔢"

            # 3. ── INTENÇÕES DE NEGÓCIO (DATA-DRIVEN) ─────────────────────────
            
            # --- FATURAMENTO / VENDAS HOJE ---
            if re.search(r'\b(vendi|vendemos|vendas|faturamento|entrou|arrecadado|ganh|receita)\b', p) and \
               re.search(r'\b(hoje|agora|neste dia|momento)\b', p):
                try:
                    valor = self._get_faturamento(self.hoje)
                    qtd = self._get_quantidade_vendas(self.hoje)
                    if valor == 0:
                        return 'A Zyra verificou e você ainda não registrou vendas hoje. Que tal registrar uma agora? 💰'
                    return f'Hoje o Cognix registrou **R$ {valor:.2f}** em **{qtd}** transação(ões). 💰'
                except Exception:
                    return 'Houve um erro ao acessar os dados de hoje, mas tente novamente em instantes.'

            # --- FATURAMENTO SEMANA ---
            if re.search(r'\b(semana|últimos 7 dias|ultimos 7 dias|esta semana)\b', p) and \
               re.search(r'\b(vendi|vendemos|vendas|faturamento|ganh|receita)\b', p):
                valor = self._get_faturamento(self.ultima_semana)
                qtd = self._get_quantidade_vendas(self.ultima_semana)
                return f'Nesta semana (últimos 7 dias) o faturamento foi de **R$ {valor:.2f}** em **{qtd}** venda(s). 📈'

            # --- FATURAMENTO MÊS ---
            if re.search(r'\b(mês|mes|últimos 30|ultimos 30|este mês)\b', p) and \
               re.search(r'\b(vendi|vendemos|vendas|faturamento|ganh|receita)\b', p):
                valor = self._get_faturamento(self.ultimo_mes)
                qtd = self._get_quantidade_vendas(self.ultimo_mes)
                return f'Nos últimos 30 dias o Cognix processou **R$ {valor:.2f}** em **{qtd}** venda(s). 📊'

            # --- PRODUTO MAIS VENDIDO ---
            if re.search(r'\b(produto|item|carro chef)\b', p) and \
               re.search(r'\b(mais vendido|melhor|campeão|destaque|top|mais sai)\b', p):
                produto = self.db.execute('''
                    SELECT p.nome, SUM(iv.quantidade) as total
                    FROM itens_venda iv
                    JOIN produtos p ON iv.produto_id = p.id
                    JOIN vendas v ON iv.venda_id = v.id
                    WHERE v.usuario_id = ?
                    GROUP BY p.id
                    ORDER BY total DESC
                    LIMIT 1
                ''', (self.usuario_id,)).fetchone()
                if produto:
                    return f'O produto campeão de vendas no seu sistema é **"{produto[0]}"** com **{produto[1]}** unidades vendidas. 🏆'
                return 'A Zyra ainda não encontrou dados de vendas para definir seu produto destaque.'

            # --- ESTOQUE BAIXO / ACABANDO ---
            if re.search(r'\b(estoque|produto|item)\b', p) and \
               re.search(r'\b(baixo|acabando|falta|reposição|pouco|crítico|critico|acabar)\b', p):
                produtos = self.db.execute('''
                    SELECT nome, quantidade FROM produtos
                    WHERE usuario_id = ? AND quantidade < 10
                    ORDER BY quantidade ASC LIMIT 5
                ''', (self.usuario_id,)).fetchall()
                if produtos:
                    lista = '\n'.join([f'- {p[0]}: {p[1]} unidade(s)' for p in produtos])
                    return f'A Zyra encontrou itens com estoque baixo (menos de 10):\n{lista}\nConsidere realizar uma reposição. ⚠️'
                return 'Excelente! Segundo o Cognix, todos os produtos têm estoque saudável (acima de 10). ✅'

            # --- TOTAL EM ESTOQUE ---
            if re.search(r'\b(estoque|produtos|itens)\b', p) and \
               re.search(r'\b(total|quanto|tenho|tem|quantidade)\b', p):
                total = self.db.execute('''
                    SELECT COALESCE(SUM(quantidade), 0) FROM produtos WHERE usuario_id = ?
                ''', (self.usuario_id,)).fetchone()[0]
                num_produtos = self.db.execute('SELECT COUNT(*) FROM produtos WHERE usuario_id = ?', (self.usuario_id,)).fetchone()[0]
                return f'Você possui **{total} itens** em estoque, distribuídos em **{num_produtos}** tipos de produtos no Cognix. 📦'

            # --- MELHORES CLIENTES / VIP ---
            if re.search(r'\b(cliente|clientes)\b', p) and \
               re.search(r'\b(melhor|melhores|vip|top|maior|gasta mais|mais comprou|destaque)\b', p):
                try:
                    clientes_data = self.obter_clientes_inteligentes()
                    vips = [c for c in clientes_data if c['classificacao'] == 'VIP']
                    if vips:
                        top5 = vips[:5]
                        lista = '\n'.join([f'⭐ **{c["nome"]}** — Score {c["score"]}, {c["total_compras"]} compras, R$ {c["valor_total"]:.2f}' for c in top5])
                        return f'Seus **{len(vips)} clientes VIP** (score ≥80):\n{lista}\n\nFoque neles para maximizar vendas! 🎯'
                    return 'Ainda não há clientes VIP identificados. Continue registrando vendas para a Zyra classificar seus clientes.'
                except Exception:
                    return 'Erro ao analisar clientes VIP. Verifique se há vendas registradas.'

            # --- CLIENTES INATIVOS / SEM COMPRAR ---
            if re.search(r'\b(cliente|clientes|quem)\b', p) and \
               re.search(r'\b(inativo|inativos|sem comprar|parado|parados|sumiu|sumiram|perdendo|não compra)\b', p):
                try:
                    clientes_data = self.obter_clientes_inteligentes()
                    inativos = [c for c in clientes_data if c['classificacao'] == 'Inativo']
                    if inativos:
                        lista = '\n'.join([f'🔴 **{c["nome"]}** — última compra há {c["dias_ultima_compra"]} dias (R$ {c["valor_total"]:.2f} total)' for c in inativos[:5]])
                        return f'A Zyra encontrou **{len(inativos)} clientes inativos**:\n{lista}\n\nConsidere uma campanha de reativação! 📩'
                    return 'Boa notícia! Todos os seus clientes estão ativos. Nenhum inativo detectado. ✅'
                except Exception:
                    return 'Erro ao buscar clientes inativos.'

            # --- CLIENTES COM POTENCIAL / OPORTUNIDADE ---
            if re.search(r'\b(cliente|clientes|quem)\b', p) and \
               re.search(r'\b(potencial|oportunidade|pode comprar|explorar|crescer|aumentar)\b', p):
                try:
                    clientes_data = self.obter_clientes_inteligentes()
                    oportunidades = [c for c in clientes_data if c.get('insight')]
                    if oportunidades:
                        lista = '\n'.join([f'💡 **{c["nome"]}**: {c["insight"]}' for c in oportunidades[:5]])
                        return f'Oportunidades detectadas pela Zyra:\n{lista}'
                    return 'Nenhuma oportunidade específica identificada no momento. Continue vendendo!'
                except Exception:
                    return 'Erro ao analisar oportunidades de clientes.'

            # --- MELHOR CLIENTE (busca simples) ---
            if re.search(r'\b(cliente)\b', p) and \
               re.search(r'\b(mais comprou|melhor|top|maior|maior faturamento)\b', p):
                cliente = self.db.execute('''
                    SELECT cliente_nome, COUNT(*) as compras, SUM(valor_total) as total
                    FROM vendas
                    WHERE usuario_id = ? AND cliente_nome IS NOT NULL AND cliente_nome != '' AND cliente_nome != 'Cliente Padrão'
                    GROUP BY cliente_nome
                    ORDER BY total DESC
                    LIMIT 1
                ''', (self.usuario_id,)).fetchone()
                if cliente:
                    return f'Seu cliente destaque é **"{cliente[0]}"**, com **{cliente[1]}** compras totalizando **R$ {cliente[2]:.2f}**. ⭐'
                return 'Ainda não tenho dados de clientes para identificar o destaque.'

            # --- LUCRO ESTIMADO ---
            if re.search(r'\b(lucro|ganho|margem|lucrei|ganhei)\b', p):
                try:
                    res = self.db.execute('''
                        SELECT COALESCE(SUM(iv.quantidade * iv.preco_unitario) - SUM(iv.quantidade * p.preco_custo), 0)
                        FROM itens_venda iv
                        JOIN produtos p ON iv.produto_id = p.id
                        JOIN vendas v ON iv.venda_id = v.id
                        WHERE v.usuario_id = ?
                    ''', (self.usuario_id,)).fetchone()[0]
                    return f'Seu lucro bruto acumulado estimado é de **R$ {res:.2f}** (venda vs custo). 📈'
                except Exception:
                    return 'Não consegui calcular o lucro. Verifique se o "preço de custo" está preenchido nos produtos.'

            # 4. ── FALLBACK INTELIGENTE (NUNCA FALHAR) ───────────────────────────
            return ('Olá! Eu sou a **Zyra**, sua consultora do Cognix. No momento, ainda não aprendi a responder sobre isso especificamente.\n\n'
                    'Mas posso te ajudar com:\n'
                    '🔹 **Vendas**: "quanto vendi hoje?", "faturamento da semana"\n'
                    '🔹 **Estoque**: "estoque baixo", "qual produto mais vendido?"\n'
                    '🔹 **Clientes**: "melhores clientes", "clientes inativos", "oportunidades"\n'
                    '🔹 **Geral**: "quem é meu melhor cliente?", "meu lucro total"\n'
                    '🔹 **Matemática**: "Quanto é 150*3?"\n\n'
                    'O que gostaria de analisar agora?')

        except Exception as e:
            # Em caso de erro crítico no processamento, retorna um fallback seguro
            return ('A Zyra encontrou um pequeno obstáculo nos dados, mas estou aqui! '
                    'Posso analisar suas vendas, estoque e clientes. '
                    'Tente perguntar por exemplo: "Zyra, quanto vendemos hoje?"')

    # ==================== INTELIGÊNCIA DE CLIENTES ====================
    
    def obter_clientes_inteligentes(self):
        """Retorna lista de clientes com score RFM, classificação e insights"""
        clientes_raw = self.db.execute('''
            SELECT 
                cliente_nome,
                COUNT(id) as total_compras,
                SUM(valor_total) as valor_total,
                MAX(data_venda) as ultima_compra,
                AVG(valor_total) as ticket_medio,
                MIN(data_venda) as primeira_compra
            FROM vendas
            WHERE usuario_id = ? 
              AND cliente_nome IS NOT NULL 
              AND cliente_nome != '' 
              AND cliente_nome != 'Cliente Padrão'
            GROUP BY cliente_nome
            ORDER BY valor_total DESC
        ''', (self.usuario_id,)).fetchall()
        
        if not clientes_raw:
            return []
        
        # Calcular máximos para normalização
        max_compras = max(c[1] for c in clientes_raw) if clientes_raw else 1
        max_valor = max(c[2] for c in clientes_raw) if clientes_raw else 1
        
        clientes = []
        for c in clientes_raw:
            nome = c[0]
            total_compras = c[1]
            valor_total = float(c[2] or 0)
            ultima_compra_str = c[3]
            ticket_medio = float(c[4] or 0)
            primeira_compra_str = c[5]
            
            # Calcular recência (dias desde última compra)
            try:
                ultima_compra_date = datetime.strptime(ultima_compra_str[:10], '%Y-%m-%d').date()
                dias_ultima_compra = (self.hoje - ultima_compra_date).days
            except (ValueError, TypeError):
                dias_ultima_compra = 999
            
            # Calcular score RFM
            score, r_score, f_score, m_score = self._calcular_score_rfm(
                dias_ultima_compra, total_compras, valor_total,
                max_compras, max_valor
            )
            
            # Classificar
            classificacao = self._classificar_cliente(score, dias_ultima_compra)
            
            # Gerar insight individual
            insight = self._gerar_insight_individual(
                nome, score, classificacao, dias_ultima_compra,
                total_compras, valor_total, ticket_medio
            )
            
            clientes.append({
                'nome': nome,
                'total_compras': total_compras,
                'valor_total': valor_total,
                'ultima_compra': ultima_compra_str[:10] if ultima_compra_str else 'N/A',
                'dias_ultima_compra': dias_ultima_compra,
                'ticket_medio': round(ticket_medio, 2),
                'score': score,
                'r_score': r_score,
                'f_score': f_score,
                'm_score': m_score,
                'classificacao': classificacao,
                'insight': insight
            })
        
        # Ordenar por score descendente
        clientes.sort(key=lambda x: x['score'], reverse=True)
        return clientes
    
    def _calcular_score_rfm(self, dias_recencia, frequencia, monetario, max_freq, max_mon):
        """Calcular score RFM (0-100) com pesos: R=40%, F=30%, M=30%"""
        # Recência: quanto menor dias, melhor (max 100)
        r_score = max(0, min(100, 100 - (dias_recencia * 1.5)))
        
        # Frequência: normalizada pelo máximo entre clientes
        f_score = min(100, (frequencia / max(max_freq, 1)) * 100)
        
        # Monetário: normalizado pelo máximo entre clientes
        m_score = min(100, (monetario / max(max_mon, 1)) * 100)
        
        # Score final ponderado
        score = int(r_score * 0.40 + f_score * 0.30 + m_score * 0.30)
        score = max(0, min(100, score))
        
        return score, int(r_score), int(f_score), int(m_score)
    
    def _classificar_cliente(self, score, dias_recencia):
        """Classificar cliente com base no score e recência"""
        if dias_recencia > 60 and score < 30:
            return 'Inativo'
        if score >= 80:
            return 'VIP'
        if score >= 50:
            return 'Regular'
        if score >= 20:
            return 'Esporádico'
        return 'Inativo'
    
    def _gerar_insight_individual(self, nome, score, classificacao, dias, compras, valor, ticket):
        """Gerar insight/sugestão para um cliente específico"""
        if classificacao == 'VIP':
            if compras >= 5:
                return f'Cliente fiel com {compras} compras — ofereça um desconto exclusivo para fidelizar ainda mais.'
            return f'Alto valor gasto (R$ {valor:.2f}) — potencial para programa de fidelidade.'
        
        if classificacao == 'Regular':
            if dias > 15:
                return f'Não compra há {dias} dias — envie uma oferta para reativá-lo.'
            return f'Cliente ativo com potencial de crescimento — sugira produtos complementares.'
        
        if classificacao == 'Esporádico':
            if valor > 100:
                return f'Gastou R$ {valor:.2f} mas compra pouco — incentive frequência com promoções.'
            return f'Poucas compras — crie uma primeira impressão forte com atendimento personalizado.'
        
        if classificacao == 'Inativo':
            return f'Sem compras há {dias} dias — campanha de reativação urgente.'
        
        return None
    
    def gerar_insights_clientes(self):
        """Gerar insights estratégicos sobre a base de clientes"""
        clientes = self.obter_clientes_inteligentes()
        if not clientes:
            return []
        
        insights = []
        
        vips = [c for c in clientes if c['classificacao'] == 'VIP']
        inativos = [c for c in clientes if c['classificacao'] == 'Inativo']
        regulares = [c for c in clientes if c['classificacao'] == 'Regular']
        
        # Insight: Clientes VIP que merecem atenção
        if vips:
            top_vip = vips[0]
            insights.append({
                'tipo': 'success',
                'icone': 'fa-crown',
                'titulo': 'Cliente VIP em Destaque',
                'mensagem': f'Foque em **{top_vip["nome"]}** — score {top_vip["score"]}, {top_vip["total_compras"]} compras. {top_vip["insight"]}'
            })
        
        # Insight: Clientes perdendo frequência
        diminuindo = [c for c in regulares if c['dias_ultima_compra'] > 20]
        if diminuindo:
            c = diminuindo[0]
            insights.append({
                'tipo': 'warning',
                'icone': 'fa-arrow-trend-down',
                'titulo': 'Atenção: Frequência Diminuindo',
                'mensagem': f'**{c["nome"]}** não compra há {c["dias_ultima_compra"]} dias. Era um cliente regular — aja antes que se torne inativo.'
            })
        
        # Insight: Clientes inativos para recuperar
        if inativos:
            insights.append({
                'tipo': 'danger',
                'icone': 'fa-user-clock',
                'titulo': f'{len(inativos)} Clientes Inativos',
                'mensagem': f'Você tem {len(inativos)} cliente(s) sem comprar há mais de 30 dias. Envie uma oferta especial para reativá-los.'
            })
        
        # Insight: Oportunidades de cross-sell
        alto_ticket = [c for c in clientes if c['ticket_medio'] > 50 and c['total_compras'] < 5]
        if alto_ticket:
            c = alto_ticket[0]
            insights.append({
                'tipo': 'info',
                'icone': 'fa-lightbulb',
                'titulo': 'Oportunidade de Crescimento',
                'mensagem': f'**{c["nome"]}** tem ticket médio alto (R$ {c["ticket_medio"]:.2f}) mas poucas compras. Alto potencial de fidelização.'
            })
        
        return insights

# ==================== ROTAS DA API ==

@ai_bp.route('/insights')
@login_required_api
def obter_insights():
    """API para obter insights de IA - análises automáticas"""
    try:
        engine = AnalysisEngine(session['user_id'])
        insights = engine.gerar_insights()
        
        # Salvar para cache
        try:
            db = get_db()
            db.execute('''
                INSERT INTO analises_ia (usuario_id, tipo, dados_json)
                VALUES (?, 'insights', ?)
            ''', (session['user_id'], json.dumps(insights)))
            db.commit()
        except Exception:
            pass  # Falha silenciosa em cache
        
        return jsonify({
            'sucesso': True,
            'insights': insights,
            'total': len(insights)
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@ai_bp.route('/previsoes')
@login_required_api
def obter_previsoes():
    """API para obter previsões de falta de estoque"""
    try:
        engine = AnalysisEngine(session['user_id'])
        previsoes = engine.prever_falta_estoque()
        return jsonify({
            'sucesso': True,
            'previsoes': previsoes,
            'critica': [p for p in previsoes if p['dias_restantes'] <= 3]
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@ai_bp.route('/recomendacoes')
@login_required_api
def obter_recomendacoes():
    """API para obter recomendações inteligentes"""
    try:
        engine = AnalysisEngine(session['user_id'])
        recomendacoes = engine.gerar_recomendacoes()
        return jsonify({
            'sucesso': True,
            'recomendacoes': recomendacoes
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@ai_bp.route('/graficos')
@login_required_api
def obter_dados_graficos():
    """API para obter dados para gráficos"""
    try:
        engine = AnalysisEngine(session['user_id'])
        dados = engine.gerar_dados_graficos()
        return jsonify({
            'sucesso': True,
            'dados': dados
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@ai_bp.route('/clientes-inteligencia')
@login_required_api
def obter_clientes_inteligencia():
    """API para obter inteligência de clientes (scoring, classificação, insights)"""
    try:
        engine = AnalysisEngine(session['user_id'])
        clientes = engine.obter_clientes_inteligentes()
        insights = engine.gerar_insights_clientes()
        
        # Estatísticas resumidas
        total = len(clientes)
        vips = len([c for c in clientes if c['classificacao'] == 'VIP'])
        inativos = len([c for c in clientes if c['classificacao'] == 'Inativo'])
        score_medio = round(sum(c['score'] for c in clientes) / total, 1) if total > 0 else 0
        
        return jsonify({
            'sucesso': True,
            'clientes': clientes,
            'insights': insights,
            'resumo': {
                'total': total,
                'vips': vips,
                'inativos': inativos,
                'score_medio': score_medio
            }
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@ai_bp.route('/chat', methods=['POST'])
@login_required_api
def chat_ia():
    """API de chat com IA - perguntas em linguagem natural"""
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Dados inválidos ou em formato incorreto'}), 400
        
        pergunta = dados.get('pergunta', '').strip()
        
        if not pergunta:
            return jsonify({'erro': 'Pergunta vazia'}), 400
        
        if len(pergunta) > 500:
            return jsonify({'erro': 'Pergunta muito longa (máximo 500 caracteres)'}), 400
        
        engine = AnalysisEngine(session['user_id'])
        resposta = engine.analisar_pergunta(pergunta)
        
        return jsonify({
            'pergunta': pergunta,
            'resposta': resposta,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'pergunta': '',
            'resposta': 'Posso te ajudar com vendas, estoque, clientes e faturamento. Exemplo: "quanto vendi hoje?"',
            'timestamp': datetime.now().isoformat()
        })
