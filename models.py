import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from contextlib import contextmanager

DATABASE = 'gestao_empresarial.db'

def get_db():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_row_value(row, key, default=None):
    """
    Safely get value from sqlite3.Row object
    
    Args:
        row: sqlite3.Row object
        key: column name
        default: value to return if key doesn't exist
    
    Returns:
        Value from row or default value
    """
    if row is None:
        return default
    try:
        return row[key] if key in row.keys() else default
    except (KeyError, TypeError):
        return default

@contextmanager
def get_db_context():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Garantir row factory em TODAS as conexões
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Initialize database with all tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Adicionar colunas faltantes em tabelas existentes (migration)
    try:
        cursor.execute('ALTER TABLE usuarios ADD COLUMN tipo TEXT DEFAULT "funcionario"')
    except sqlite3.OperationalError:
        pass  # Coluna já existe
    
    try:
        cursor.execute('ALTER TABLE usuarios ADD COLUMN ativo BOOLEAN DEFAULT 1')
    except sqlite3.OperationalError:
        pass  # Coluna já existe
    
    try:
        cursor.execute('ALTER TABLE usuarios ADD COLUMN ultimo_acesso TIMESTAMP')
    except sqlite3.OperationalError:
        pass  # Coluna já existe
    
    # Campos empresariais (preparação para futuro)
    try:
        cursor.execute('ALTER TABLE usuarios ADD COLUMN empresa_nome TEXT')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE usuarios ADD COLUMN empresa_cnpj TEXT')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE usuarios ADD COLUMN empresa_localizacao TEXT')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE usuarios ADD COLUMN empresa_endereco TEXT')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE usuarios ADD COLUMN empresa_cep TEXT')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE usuarios ADD COLUMN responsavel_nome TEXT')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE usuarios ADD COLUMN responsavel_cpf TEXT')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE usuarios ADD COLUMN empresa_ano_fundacao INTEGER')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE usuarios ADD COLUMN empresa_telefone TEXT')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE usuarios ADD COLUMN empresa_email TEXT')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE produtos ADD COLUMN ativo BOOLEAN DEFAULT 1')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE clientes ADD COLUMN ativo BOOLEAN DEFAULT 1')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE funcionarios ADD COLUMN ativo BOOLEAN DEFAULT 1')
    except sqlite3.OperationalError:
        pass
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT DEFAULT 'funcionario' CHECK(tipo IN ('admin', 'gerente', 'funcionario')),
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ultimo_acesso TIMESTAMP,
            ativo BOOLEAN DEFAULT 1,
            -- Campos empresariais (preparação para futuro)
            empresa_nome TEXT,
            empresa_cnpj TEXT,
            empresa_localizacao TEXT,
            empresa_endereco TEXT,
            empresa_cep TEXT,
            responsavel_nome TEXT,
            responsavel_cpf TEXT,
            empresa_ano_fundacao INTEGER,
            empresa_telefone TEXT,
            empresa_email TEXT
        )
    ''')
    
    # Tabela de categorias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            descricao TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ''')
    
    # Tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            quantidade INTEGER DEFAULT 0,
            preco REAL NOT NULL,
            categoria_id INTEGER,
            descricao TEXT,
            estoque_minimo INTEGER DEFAULT 5,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ativo BOOLEAN DEFAULT 1,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
        )
    ''')
    
    # Tabela de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT,
            cpf TEXT,
            endereco TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ativo BOOLEAN DEFAULT 1,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ''')
    
    # Tabela de vendas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            cliente_id INTEGER,
            cliente_nome TEXT,
            valor_total REAL NOT NULL,
            data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            observacoes TEXT,
            funcionario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE SET NULL,
            FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE SET NULL
        )
    ''')
    
    # Tabela de itens de venda
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens_venda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venda_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (venda_id) REFERENCES vendas(id) ON DELETE CASCADE,
            FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE RESTRICT
        )
    ''')
    
    # Tabela de funcionários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            usuario_funcionario_id INTEGER,
            nome TEXT NOT NULL,
            email TEXT,
            cargo TEXT,
            telefone TEXT,
            cpf TEXT UNIQUE,
            data_admissao DATE NOT NULL,
            salario REAL DEFAULT 0,
            comissao_percentual REAL DEFAULT 0,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ativo BOOLEAN DEFAULT 1,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (usuario_funcionario_id) REFERENCES usuarios(id) ON DELETE SET NULL
        )
    ''')
    
    # Tabela de vendas por funcionário (tracking de comissões)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas_funcionario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario_id INTEGER NOT NULL,
            venda_id INTEGER NOT NULL,
            comissao_ganho REAL NOT NULL,
            data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE CASCADE,
            FOREIGN KEY (venda_id) REFERENCES vendas(id) ON DELETE CASCADE
        )
    ''')
    
    # Tabela de logs de ação (auditoria)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs_acao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            funcionario_id INTEGER,
            tipo_acao TEXT NOT NULL,
            tabela TEXT,
            id_registro INTEGER,
            descricao TEXT,
            dados_antigos TEXT,
            dados_novos TEXT,
            data_acao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            endereco_ip TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
            FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE SET NULL
        )
    ''')
    
    # Tabela de histórico de chat
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            pergunta TEXT NOT NULL,
            resposta TEXT NOT NULL,
            tipo_pergunta TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ''')
    
    # Tabela de alertas e notificações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            mensagem TEXT NOT NULL,
            lido BOOLEAN DEFAULT 0,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_leitura TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ''')
    
    # Tabela de despesas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria TEXT NOT NULL,
            data_despesa TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ''')
    
    # Tabela de metas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            ano INTEGER NOT NULL,
            valor_meta REAL NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            UNIQUE(usuario_id, mes, ano)
        )
    ''')
    
    # Criar índices para melhor performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_produtos_usuario ON produtos(usuario_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_vendas_usuario ON vendas(usuario_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_vendas_data ON vendas(data_venda)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_funcionarios_usuario ON funcionarios(usuario_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_usuario ON logs_acao(usuario_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_usuario ON chat_historico(usuario_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_despesas_usuario ON despesas(usuario_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_metas_usuario ON metas(usuario_id)')
    
    conn.commit()
    conn.close()

class User:
    @staticmethod
    def criar_usuario(nome, email, senha, tipo='funcionario', **kwargs):
        """Create a new user"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO usuarios (nome, email, senha, tipo, empresa_nome, empresa_cnpj, 
                                       empresa_localizacao, empresa_endereco, empresa_cep,
                                       responsavel_nome, responsavel_cpf, empresa_ano_fundacao,
                                       empresa_telefone, empresa_email)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (nome, email, generate_password_hash(senha), tipo,
                      kwargs.get('empresa_nome'), kwargs.get('empresa_cnpj'),
                      kwargs.get('empresa_localizacao'), kwargs.get('empresa_endereco'),
                      kwargs.get('empresa_cep'), kwargs.get('responsavel_nome'),
                      kwargs.get('responsavel_cpf'), kwargs.get('empresa_ano_fundacao'),
                      kwargs.get('empresa_telefone'), kwargs.get('empresa_email')))
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                return None
    
    @staticmethod
    def obter_usuario_por_email(email):
        """Get user by email"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE email = ? AND ativo = 1', (email,))
            return cursor.fetchone()
    
    @staticmethod
    def obter_usuario_por_id(user_id):
        """Get user by ID"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE id = ? AND ativo = 1', (user_id,))
            return cursor.fetchone()
    
    @staticmethod
    def verificar_senha(user_id, senha):
        """Verify user password"""
        user = User.obter_usuario_por_id(user_id)
        if user:
            return check_password_hash(user['senha'], senha)
        return False
    
    @staticmethod
    def atualizar_ultimo_acesso(user_id):
        """Update last access time"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE usuarios SET ultimo_acesso = CURRENT_TIMESTAMP WHERE id = ?
            ''', (user_id,))
    
    @staticmethod
    def listar_usuarios():
        """List all active users"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, nome, email, tipo, data_criacao FROM usuarios WHERE ativo = 1
                ORDER BY data_criacao DESC
            ''')
            return cursor.fetchall()

class Produto:
    @staticmethod
    def criar_produto(usuario_id, nome, quantidade, preco, categoria_id=None, estoque_minimo=5):
        """Create a new product"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO produtos (usuario_id, nome, quantidade, preco, categoria_id, estoque_minimo)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (usuario_id, nome, quantidade, preco, categoria_id, estoque_minimo))
            return cursor.lastrowid
    
    @staticmethod
    def obter_produtos_usuario(usuario_id):
        """Get all products for a user"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, c.nome as categoria_nome 
                FROM produtos p
                LEFT JOIN categorias c ON p.categoria_id = c.id
                WHERE p.usuario_id = ? AND p.ativo = 1
                ORDER BY p.nome
            ''', (usuario_id,))
            return cursor.fetchall()
    
    @staticmethod
    def obter_produto(produto_id, usuario_id):
        """Get specific product"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, c.nome as categoria_nome 
                FROM produtos p
                LEFT JOIN categorias c ON p.categoria_id = c.id
                WHERE p.id = ? AND p.usuario_id = ? AND p.ativo = 1
            ''', (produto_id, usuario_id))
            return cursor.fetchone()
    
    @staticmethod
    def atualizar_estoque(produto_id, quantidade_alteracao):
        """Update product stock"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE produtos SET quantidade = quantidade + ?, data_atualizacao = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (quantidade_alteracao, produto_id))

class Venda:
    @staticmethod
    def criar_venda(usuario_id, valor_total, cliente_id=None, cliente_nome=None, funcionario_id=None):
        """Create a new sale"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO vendas (usuario_id, cliente_id, cliente_nome, valor_total, funcionario_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuario_id, cliente_id, cliente_nome, valor_total, funcionario_id))
            return cursor.lastrowid
    
    @staticmethod
    def adicionar_item_venda(venda_id, produto_id, quantidade, preco_unitario):
        """Add item to sale"""
        subtotal = quantidade * preco_unitario
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?)
            ''', (venda_id, produto_id, quantidade, preco_unitario, subtotal))
    
    @staticmethod
    def obter_vendas_usuario(usuario_id, limite=None):
        """Get all sales for a user"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            query = '''
                SELECT * FROM vendas 
                WHERE usuario_id = ?
                ORDER BY data_venda DESC
            '''
            if limite:
                query += f' LIMIT {limite}'
            cursor.execute(query, (usuario_id,))
            return cursor.fetchall()
    
    @staticmethod
    def obter_venda_detalhes(venda_id):
        """Get complete sale details with items"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM vendas WHERE id = ?', (venda_id,))
            venda = cursor.fetchone()
            if venda:
                cursor.execute('''
                    SELECT iv.*, p.nome as produto_nome FROM itens_venda iv
                    JOIN produtos p ON iv.produto_id = p.id
                    WHERE iv.venda_id = ?
                ''', (venda_id,))
                itens = cursor.fetchall()
                return {'venda': venda, 'itens': itens}
            return None

class Funcionario:
    @staticmethod
    def criar_funcionario(usuario_id, nome, email, cargo, data_admissao, salario=0, comissao_percentual=0):
        """Create a new employee"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO funcionarios (usuario_id, nome, email, cargo, data_admissao, salario, comissao_percentual)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (usuario_id, nome, email, cargo, data_admissao, salario, comissao_percentual))
            return cursor.lastrowid
    
    @staticmethod
    def obter_funcionarios_usuario(usuario_id):
        """Get all employees for a user"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM funcionarios 
                WHERE usuario_id = ? AND ativo = 1
                ORDER BY nome
            ''', (usuario_id,))
            return cursor.fetchall()
    
    @staticmethod
    def obter_ranking_vendedores(usuario_id):
        """Get employee sales ranking"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT f.id, f.nome, COUNT(DISTINCT v.id) as total_vendas, COALESCE(SUM(v.valor_total), 0) as valor_total
                FROM funcionarios f
                LEFT JOIN vendas v ON f.id = v.funcionario_id
                WHERE f.usuario_id = ? AND f.ativo = 1
                GROUP BY f.id, f.nome
                ORDER BY valor_total DESC, total_vendas DESC
            ''', (usuario_id,))
            return cursor.fetchall()

class Log:
    @staticmethod
    def registrar_acao(usuario_id, tipo_acao, tabela, id_registro, descricao, funcionario_id=None, endereco_ip=None):
        """Register an action in audit log"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO logs_acao (usuario_id, funcionario_id, tipo_acao, tabela, id_registro, descricao, endereco_ip)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (usuario_id, funcionario_id, tipo_acao, tabela, id_registro, descricao, endereco_ip))

class ChatHistorico:
    @staticmethod
    def salvar_conversa(usuario_id, pergunta, resposta, tipo_pergunta=None):
        """Save chat conversation"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO chat_historico (usuario_id, pergunta, resposta, tipo_pergunta)
                VALUES (?, ?, ?, ?)
            ''', (usuario_id, pergunta, resposta, tipo_pergunta))
    
    @staticmethod
    def obter_historico_usuario(usuario_id, limite=50):
        """Get chat history for user"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM chat_historico 
                WHERE usuario_id = ?
                ORDER BY data_criacao DESC
                LIMIT ?
            ''', (usuario_id, limite))
            return cursor.fetchall()

class Alerta:
    @staticmethod
    def criar_alerta(usuario_id, tipo, mensagem):
        """Create an alert for user"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO alertas (usuario_id, tipo, mensagem)
                VALUES (?, ?, ?)
            ''', (usuario_id, tipo, mensagem))
    
    @staticmethod
    def obter_alertas_nao_lidos(usuario_id):
        """Get unread alerts for user"""
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM alertas 
                WHERE usuario_id = ? AND lido = 0
                ORDER BY data_criacao DESC
            ''', (usuario_id,))
            return cursor.fetchall()

class Despesa:
    @staticmethod
    def criar_despesa(usuario_id, descricao, valor, categoria, data_despesa=None):
        if not data_despesa:
            data_despesa = datetime.now()
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO despesas (usuario_id, descricao, valor, categoria, data_despesa)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuario_id, descricao, valor, categoria, data_despesa))
            return cursor.lastrowid
            
    @staticmethod
    def obter_despesas_mes(usuario_id, mes, ano):
        with get_db_context() as conn:
            cursor = conn.cursor()
            data_inicio = f"{ano}-{mes:02d}-01"
            if mes == 12:
                data_fim = f"{ano+1}-01-01"
            else:
                data_fim = f"{ano}-{mes+1:02d}-01"
                
            cursor.execute('''
                SELECT * FROM despesas 
                WHERE usuario_id = ? AND data_despesa >= ? AND data_despesa < ?
                ORDER BY data_despesa DESC
            ''', (usuario_id, data_inicio, data_fim))
            return cursor.fetchall()

class Meta:
    @staticmethod
    def obter_meta(usuario_id, mes, ano):
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT valor_meta FROM metas 
                WHERE usuario_id = ? AND mes = ? AND ano = ?
            ''', (usuario_id, mes, ano))
            row = cursor.fetchone()
            return row['valor_meta'] if row else None
            
    @staticmethod
    def definir_meta(usuario_id, mes, ano, valor_meta):
        meta_atual = Meta.obter_meta(usuario_id, mes, ano)
        with get_db_context() as conn:
            cursor = conn.cursor()
            if meta_atual is not None:
                cursor.execute('''
                    UPDATE metas SET valor_meta = ? 
                    WHERE usuario_id = ? AND mes = ? AND ano = ?
                ''', (valor_meta, usuario_id, mes, ano))
            else:
                cursor.execute('''
                    INSERT INTO metas (usuario_id, mes, ano, valor_meta)
                    VALUES (?, ?, ?, ?)
                ''', (usuario_id, mes, ano, valor_meta))
