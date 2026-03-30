"""
Script de Seed Data - Cognix
Popula o banco de dados com dados de teste realistas para demonstração da Zyra
"""

import sqlite3
from datetime import datetime, timedelta
import random
from werkzeug.security import generate_password_hash

# Conectar ao banco
DATABASE = 'gestao_empresarial.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def seed_database():
    """Popula o banco com dados de teste realistas"""
    conn = get_db()
    cursor = conn.cursor()

    print("🌱 Iniciando seed do banco de dados...")

    # Usar o usuário ID 1 (Teste) para os dados
    usuario_id = 1

    # ==================== CATEGORIAS ====================
    print("📂 Criando categorias...")
    categorias = [
        ("Eletrônicos", "Produtos eletrônicos e gadgets"),
        ("Roupas", "Vestuário e acessórios"),
        ("Alimentos", "Produtos alimentícios e bebidas"),
        ("Casa e Jardim", "Itens para casa e jardinagem"),
        ("Esportes", "Equipamentos esportivos"),
        ("Livros", "Livros e materiais educacionais"),
        ("Beleza", "Produtos de beleza e cuidados pessoais"),
        ("Automotivo", "Peças e acessórios automotivos")
    ]

    categoria_ids = {}
    for nome, descricao in categorias:
        cursor.execute('''
            INSERT INTO categorias (usuario_id, nome, descricao)
            VALUES (?, ?, ?)
        ''', (usuario_id, nome, descricao))
        categoria_ids[nome] = cursor.lastrowid

    # ==================== PRODUTOS ====================
    print("📦 Criando produtos...")
    produtos = [
        # Eletrônicos
        ("Smartphone Samsung Galaxy A54", 50, 1899.99, categoria_ids["Eletrônicos"], "Smartphone Android com câmera de 50MP", 5),
        ("Notebook Dell Inspiron 15", 20, 3299.99, categoria_ids["Eletrônicos"], "Notebook com processador i5 e 8GB RAM", 3),
        ("Fone de Ouvido Bluetooth JBL", 100, 299.99, categoria_ids["Eletrônicos"], "Fone wireless com cancelamento de ruído", 10),
        ("Smart TV LG 43\"", 15, 2199.99, categoria_ids["Eletrônicos"], "TV LED 4K com HDR", 2),
        ("Mouse Gamer Logitech", 80, 149.99, categoria_ids["Eletrônicos"], "Mouse óptico com 6 botões programáveis", 8),

        # Roupas
        ("Camiseta Básica Algodão", 200, 39.99, categoria_ids["Roupas"], "Camiseta 100% algodão, cores sortidas", 20),
        ("Calça Jeans Masculina", 60, 129.99, categoria_ids["Roupas"], "Calça jeans azul escuro, tamanho M", 8),
        ("Tênis Nike Air Max", 40, 499.99, categoria_ids["Roupas"], "Tênis esportivo com amortecimento", 5),
        ("Jaqueta de Couro Sintético", 25, 249.99, categoria_ids["Roupas"], "Jaqueta preta tamanho único", 3),
        ("Vestido Floral", 35, 89.99, categoria_ids["Roupas"], "Vestido estampado, tamanho P ao G", 6),

        # Alimentos
        ("Café Torrado em Grão", 150, 24.99, categoria_ids["Alimentos"], "Café especial 500g", 15),
        ("Chocolate ao Leite Garoto", 120, 8.99, categoria_ids["Alimentos"], "Barra de chocolate 90g", 25),
        ("Refrigerante Coca-Cola 2L", 200, 7.99, categoria_ids["Alimentos"], "Refrigerante cola garrafa 2L", 30),
        ("Arroz Branco Tipo 1", 80, 19.99, categoria_ids["Alimentos"], "Arroz 5kg pacote", 10),
        ("Leite Integral", 100, 4.99, categoria_ids["Alimentos"], "Leite longa vida 1L", 20),

        # Casa e Jardim
        ("Jogo de Talheres Inox", 45, 79.99, categoria_ids["Casa e Jardim"], "Conjunto de 24 peças", 5),
        ("Vaso de Planta Decorativo", 30, 34.99, categoria_ids["Casa e Jardim"], "Vaso cerâmico 20cm", 8),
        ("Jogo de Cama Queen Size", 20, 199.99, categoria_ids["Casa e Jardim"], "Jogo completo com fronha", 3),
        ("Aspirador de Pó Vertical", 25, 349.99, categoria_ids["Casa e Jardim"], "Aspirador sem fio 2000W", 4),
        ("Conjunto de Panelas Antiaderente", 35, 159.99, categoria_ids["Casa e Jardim"], "5 peças com revestimento cerâmico", 6),

        # Esportes
        ("Bola de Futebol Campo", 40, 89.99, categoria_ids["Esportes"], "Bola oficial tamanho 5", 8),
        ("Esteira Elétrica", 8, 1899.99, categoria_ids["Esportes"], "Esteira motorizada com inclinação", 2),
        ("Raquete de Tênis Wilson", 15, 299.99, categoria_ids["Esportes"], "Raquete profissional carbono", 3),
        ("Bicicleta Mountain Bike", 12, 1299.99, categoria_ids["Esportes"], "Bike alumínio 29\" com 21 marchas", 2),
        ("Tapete de Yoga", 50, 49.99, categoria_ids["Esportes"], "Tapete antiderrapante 6mm", 10),

        # Livros
        ("Dom Casmurro - Machado de Assis", 30, 29.99, categoria_ids["Livros"], "Clássico da literatura brasileira", 5),
        ("O Senhor dos Anéis", 25, 79.99, categoria_ids["Livros"], "Trilogia completa em um volume", 4),
        ("Python para Iniciantes", 40, 59.99, categoria_ids["Livros"], "Guia completo de programação", 8),
        ("Harry Potter e a Pedra Filosofal", 35, 39.99, categoria_ids["Livros"], "Primeiro volume da saga", 6),
        ("Mindset - Carol Dweck", 20, 34.99, categoria_ids["Livros"], "Sobre psicologia do sucesso", 4),

        # Beleza
        ("Shampoo Anticaspa Clear", 80, 19.99, categoria_ids["Beleza"], "Shampoo para cabelos oleosos 200ml", 12),
        ("Perfume Masculino Dior", 15, 299.99, categoria_ids["Beleza"], "Eau de Toilette 100ml", 3),
        ("Base Líquida L'Oréal", 40, 49.99, categoria_ids["Beleza"], "Base matte cobertura média", 7),
        ("Creme Hidratante Nivea", 90, 12.99, categoria_ids["Beleza"], "Creme para pele seca 200ml", 15),
        ("Máscara Capilar Óleo de Argan", 25, 39.99, categoria_ids["Beleza"], "Tratamento intensivo 300ml", 5),

        # Automotivo
        ("Óleo de Motor 5W30", 60, 29.99, categoria_ids["Automotivo"], "Óleo sintético 1L", 10),
        ("Pneu Aro 15", 20, 399.99, categoria_ids["Automotivo"], "Pneu 195/65R15", 4),
        ("Kit Limpador de Para-brisa", 70, 14.99, categoria_ids["Automotivo"], "6 unidades + lavador", 12),
        ("Bateria Automotiva 60Ah", 12, 299.99, categoria_ids["Automotivo"], "Bateria chumbo-ácido", 2),
        ("Tapete Automotivo", 30, 79.99, categoria_ids["Automotivo"], "Conjunto para carro completo", 6)
    ]

    produto_ids = {}
    for nome, quantidade, preco, categoria_id, descricao, estoque_minimo in produtos:
        cursor.execute('''
            INSERT INTO produtos (usuario_id, nome, quantidade, preco, categoria, descricao)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (usuario_id, nome, quantidade, preco, categoria_id, descricao))
        produto_ids[nome] = cursor.lastrowid

    # ==================== CLIENTES ====================
    print("👥 Criando clientes...")
    clientes = [
        ("João Silva", "joao.silva@email.com", "(11) 99999-0001", "123.456.789-00", "Rua das Flores, 123 - São Paulo/SP"),
        ("Maria Santos", "maria.santos@email.com", "(11) 99999-0002", "987.654.321-00", "Av. Paulista, 456 - São Paulo/SP"),
        ("Pedro Oliveira", "pedro.oliveira@email.com", "(11) 99999-0003", "456.789.123-00", "Rua Augusta, 789 - São Paulo/SP"),
        ("Ana Costa", "ana.costa@email.com", "(11) 99999-0004", "321.654.987-00", "Rua Oscar Freire, 321 - São Paulo/SP"),
        ("Carlos Rodrigues", "carlos.rodrigues@email.com", "(11) 99999-0005", "789.123.456-00", "Av. Brigadeiro, 654 - São Paulo/SP"),
        ("Fernanda Lima", "fernanda.lima@email.com", "(11) 99999-0006", "147.258.369-00", "Rua da Consolação, 987 - São Paulo/SP"),
        ("Roberto Alves", "roberto.alves@email.com", "(11) 99999-0007", "963.852.741-00", "Rua Vergueiro, 147 - São Paulo/SP"),
        ("Juliana Pereira", "juliana.pereira@email.com", "(11) 99999-0008", "852.741.963-00", "Av. Ipiranga, 258 - São Paulo/SP"),
        ("Marcos Souza", "marcos.souza@email.com", "(11) 99999-0009", "741.963.852-00", "Rua São João, 369 - São Paulo/SP"),
        ("Patricia Gomes", "patricia.gomes@email.com", "(11) 99999-0010", "369.258.147-00", "Rua Direita, 741 - São Paulo/SP")
    ]

    cliente_ids = {}
    for nome, email, telefone, cpf, endereco in clientes:
        cursor.execute('''
            INSERT INTO clientes (usuario_id, nome, email, telefone, cpf_cnpj, endereco)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (usuario_id, nome, email, telefone, cpf, endereco))
        cliente_ids[nome] = cursor.lastrowid

    # ==================== FUNCIONÁRIOS ====================
    print("👷 Criando funcionários...")
    funcionarios = [
        ("Carlos Vendedor", "carlos@empresa.com", "Vendedor", "(11) 88888-0001", "111.222.333-44", "2023-01-15", 2500.00, 5.0),
        ("Ana Atendente", "ana@empresa.com", "Atendente", "(11) 88888-0002", "222.333.444-55", "2023-02-01", 1800.00, 3.0),
        ("Roberto Gerente", "roberto@empresa.com", "Gerente de Vendas", "(11) 88888-0003", "333.444.555-66", "2022-12-01", 4500.00, 8.0),
        ("Mariana Caixa", "mariana@empresa.com", "Caixa", "(11) 88888-0004", "444.555.666-77", "2023-03-10", 1600.00, 2.0),
        ("Lucas Estoquista", "lucas@empresa.com", "Estoquista", "(11) 88888-0005", "555.666.777-88", "2023-01-20", 1900.00, 2.5)
    ]

    funcionario_ids = {}
    for nome, email, cargo, telefone, cpf, data_admissao, salario, comissao in funcionarios:
        cursor.execute('''
            INSERT INTO funcionarios (usuario_id, nome, email, cargo, telefone, cpf, data_admissao, salario, comissao_percentual)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, nome, email, cargo, telefone, cpf, data_admissao, salario, comissao))
        funcionario_ids[nome] = cursor.lastrowid

    # ==================== VENDAS ====================
    print("💰 Criando vendas...")

    # Produtos mais vendidos (IDs dos primeiros produtos)
    produtos_populares = list(produto_ids.values())[:15]  # Top 15 produtos
    clientes_lista = list(cliente_ids.values())
    funcionarios_lista = list(funcionario_ids.values())

    # Gerar vendas dos últimos 30 dias
    hoje = datetime.now()
    vendas_data = []

    for dias_atras in range(30, 0, -1):
        data_venda = hoje - timedelta(days=dias_atras)

        # Vendas diárias variam entre 3-8 por dia
        vendas_dia = random.randint(3, 8)

        for _ in range(vendas_dia):
            cliente_id = random.choice(clientes_lista)
            cliente_nome = [k for k, v in cliente_ids.items() if v == cliente_id][0]
            funcionario_id = random.choice(funcionarios_lista) if random.random() > 0.3 else None

            # Itens da venda (1-5 produtos por venda)
            num_itens = random.randint(1, 5)
            itens_venda = []
            valor_total = 0

            for _ in range(num_itens):
                produto_id = random.choice(produtos_populares)
                quantidade = random.randint(1, 3)

                # Buscar preço do produto
                cursor.execute('SELECT preco FROM produtos WHERE id = ?', (produto_id,))
                preco_unitario = cursor.fetchone()[0]

                subtotal = quantidade * preco_unitario
                valor_total += subtotal

                itens_venda.append((produto_id, quantidade, preco_unitario, subtotal))

            # Inserir venda
            cursor.execute('''
                INSERT INTO vendas (usuario_id, cliente_nome, valor_total, data_venda)
                VALUES (?, ?, ?, ?)
            ''', (usuario_id, cliente_nome, valor_total, data_venda.strftime('%Y-%m-%d %H:%M:%S')))

            venda_id = cursor.lastrowid

            # Inserir itens da venda
            for produto_id, quantidade, preco_unitario, subtotal in itens_venda:
                cursor.execute('''
                    INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                ''', (venda_id, produto_id, quantidade, preco_unitario, subtotal))

                # Atualizar estoque do produto
                cursor.execute('''
                    UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?
                ''', (quantidade, produto_id))

    # ==================== ATUALIZAR PREÇOS DE CUSTO ====================
    print("💸 Adicionando preços de custo aos produtos...")
    for produto_id in produto_ids.values():
        cursor.execute('SELECT preco FROM produtos WHERE id = ?', (produto_id,))
        preco_venda = cursor.fetchone()[0]

        # Preço de custo = 60-80% do preço de venda
        preco_custo = preco_venda * random.uniform(0.6, 0.8)

        try:
            cursor.execute('UPDATE produtos SET preco_custo = ? WHERE id = ?', (preco_custo, produto_id))
        except sqlite3.OperationalError:
            # Campo pode não existir ainda
            pass

    # ==================== LOGS DE AÇÃO ====================
    print("📝 Criando logs de auditoria...")
    acoes = [
        ("LOGIN", None, "Usuário fez login no sistema"),
        ("VENDA_CRIADA", None, "Nova venda registrada"),
        ("PRODUTO_ATUALIZADO", None, "Produto teve estoque atualizado"),
        ("CLIENTE_CADASTRADO", None, "Novo cliente cadastrado"),
        ("CHAT_PERGUNTA", None, "Pergunta feita para a Zyra")
    ]

    for _ in range(50):
        tipo_acao, tabela, descricao = random.choice(acoes)
        data_acao = hoje - timedelta(days=random.randint(0, 30))

        cursor.execute('''
            INSERT INTO logs_acao (usuario_id, tipo_acao, tabela, descricao, data_acao)
            VALUES (?, ?, ?, ?, ?)
        ''', (usuario_id, tipo_acao, tabela, descricao, data_acao.strftime('%Y-%m-%d %H:%M:%S')))

    # Commit das mudanças
    conn.commit()
    conn.close()

    print("✅ Seed concluído com sucesso!")
    print(f"📊 Dados criados:")
    print(f"   • {len(categorias)} categorias")
    print(f"   • {len(produtos)} produtos")
    print(f"   • {len(clientes)} clientes")
    print(f"   • {len(funcionarios)} funcionários")
    print(f"   • ~150-240 vendas (últimos 30 dias)")
    print(f"   • ~400-1200 itens de venda")
    print(f"   • 50 logs de auditoria")

if __name__ == "__main__":
    seed_database()