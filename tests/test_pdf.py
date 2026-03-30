from app import app
from pdf_reports import gerar_pdf

with app.app_context():
    try:
        pdf_buffer = gerar_pdf(3, 'mensal')
        print("PDF Mensal gerado com sucesso!")
        pdf_buffer = gerar_pdf(3, 'semanal')
        print("PDF Semanal gerado com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")
