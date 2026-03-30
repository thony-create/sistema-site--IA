from ai_module import AnalysisEngine
import sqlite3

# Test outside of app context to simplify
conn = sqlite3.connect('gestao_empresarial.db')
cursor = conn.cursor()
cursor.execute('SELECT id FROM usuarios LIMIT 1')
user = cursor.fetchone()

if user:
    user_id = user[0]
    print(f"Testando alertas para o usuario ID: {user_id}")
    engine = AnalysisEngine(user_id)
    alertas = engine.gerar_alertas_proativos()
    
    print("\n=== ALERTAS DA ZYRA ===")
    if not alertas:
        print("Nenhum alerta gerado.")
    else:
        for alerta in alertas:
            print(f"[{alerta['tipo'].upper()}] - {alerta['mensagem']}")
else:
    print("Nenhum usuario no bd.")
