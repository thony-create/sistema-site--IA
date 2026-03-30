import io
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from models import get_db
from ai_module import AnalysisEngine

def gerar_pdf(usuario_id, tipo):
    # Definir período
    hoje = datetime.now().date()
    if tipo == 'semanal':
        data_inicio = hoje - timedelta(days=7)
        titulo_relatorio = "Relatório Semanal de Desempenho"
    else:  # mensal
        data_inicio = hoje.replace(day=1)
        titulo_relatorio = "Relatório Mensal de Desempenho"

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        alignment=1, # Center
        spaceAfter=20
    )
    subtitle_style = ParagraphStyle(
        'SubTitleStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=1,
        spaceAfter=30
    )
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceBefore=20,
        spaceAfter=10
    )
    normal_style = styles['Normal']
    
    # Cabeçalho
    elements.append(Paragraph("COGNIX", title_style))
    elements.append(Paragraph(titulo_relatorio, subtitle_style))
    elements.append(Paragraph(f"Período: {data_inicio.strftime('%d/%m/%Y')} a {hoje.strftime('%d/%m/%Y')}", normal_style))
    elements.append(Spacer(1, 20))
    
    # Buscar Dados Reais
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Faturamento
    cursor.execute('''
        SELECT COALESCE(SUM(valor_total), 0), COUNT(id)
        FROM vendas
        WHERE usuario_id = ? AND DATE(data_venda) >= ?
    ''', (usuario_id, data_inicio))
    fat_total, qtd_vendas = cursor.fetchone()
    
    elements.append(Paragraph("1. Resumo Financeiro", section_style))
    financeiro_data = [
        ['Indicador', 'Valor'],
        ['Faturamento Total', f'R$ {fat_total:.2f}'],
        ['Quantidade de Vendas', str(qtd_vendas)],
        ['Ticket Médio', f'R$ {(fat_total / qtd_vendas if qtd_vendas > 0 else 0):.2f}']
    ]
    t_fin = Table(financeiro_data, colWidths=[250, 250])
    t_fin.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
    ]))
    elements.append(t_fin)
    
    # 2. Produtos Mais Vendidos
    elements.append(Paragraph("2. Produtos Mais Vendidos", section_style))
    cursor.execute('''
        SELECT p.nome, SUM(iv.quantidade), SUM(iv.subtotal)
        FROM itens_venda iv
        JOIN produtos p ON iv.produto_id = p.id
        JOIN vendas v ON iv.venda_id = v.id
        WHERE v.usuario_id = ? AND DATE(v.data_venda) >= ?
        GROUP BY p.id
        ORDER BY SUM(iv.quantidade) DESC
        LIMIT 5
    ''', (usuario_id, data_inicio))
    top_produtos = cursor.fetchall()
    
    if top_produtos:
        prod_data = [['Produto', 'Qtd Vendida', 'Receita Gerada']]
        for p in top_produtos:
            prod_data.append([p[0], str(p[1]), f'R$ {p[2]:.2f}'])
            
        t_prod = Table(prod_data, colWidths=[200, 150, 150])
        t_prod.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff'))
        ]))
        elements.append(t_prod)
    else:
        elements.append(Paragraph("Nenhuma venda registrada no período.", normal_style))
        
    # 3. Clientes Principais
    elements.append(Paragraph("3. Clientes Principais", section_style))
    cursor.execute('''
        SELECT COALESCE(cliente_nome, 'Cliente Avulso'), COUNT(id), SUM(valor_total)
        FROM vendas
        WHERE usuario_id = ? AND DATE(data_venda) >= ?
        GROUP BY cliente_nome
        ORDER BY SUM(valor_total) DESC
        LIMIT 5
    ''', (usuario_id, data_inicio))
    top_clientes = cursor.fetchall()
    
    if top_clientes:
        cli_data = [['Cliente', 'Nº de Compras', 'Valor Gasto']]
        for c in top_clientes:
            cli_data.append([c[0], str(c[1]), f'R$ {c[2]:.2f}'])
            
        t_cli = Table(cli_data, colWidths=[200, 150, 150])
        t_cli.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
        ]))
        elements.append(t_cli)
    else:
        elements.append(Paragraph("Nenhum cliente registrado no período.", normal_style))
        
    # 4. Insights da Zyra
    elements.append(Paragraph("4. Inteligência Zyra (Insights)", section_style))
    engine = AnalysisEngine(usuario_id)
    alertas = engine.gerar_alertas_proativos()
    recomendacoes = engine.gerar_recomendacoes()
    
    zyra_style = ParagraphStyle(
        'ZyraStyle',
        parent=normal_style,
        fontSize=11,
        textColor=colors.HexColor('#2c3e50'),
        spaceBefore=10,
        spaceAfter=5,
        leftIndent=20,
        bulletIndent=10
    )
    
    if not alertas and not recomendacoes:
        elements.append(Paragraph("A Zyra não gerou insights ou recomendações no momento.", normal_style))
    else:
        if alertas:
            elements.append(Paragraph("<b>Alertas de Atenção:</b>", normal_style))
            for a in alertas:
                elements.append(Paragraph(f"• {a['mensagem']}", zyra_style))
                
        if recomendacoes:
            elements.append(Spacer(1, 10))
            elements.append(Paragraph("<b>Recomendações Estratégicas:</b>", normal_style))
            for r in recomendacoes:
                elements.append(Paragraph(f"• {r['mensagem']}", zyra_style))
                
    # Footer
    elements.append(Spacer(1, 50))
    elements.append(Paragraph("Relatório gerado automaticamente pela Cognix Inteligência Artificial.", ParagraphStyle(
        'Footer', parent=normal_style, fontSize=9, textColor=colors.gray, alignment=1
    )))

    # Gerar PDF fechando o documento
    doc.build(elements)
    buffer.seek(0)
    conn.close()
    
    return buffer
