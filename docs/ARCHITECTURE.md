# ARQUITETURA DO SISTEMA

## 🏗️ Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                  CAMADA DE APRESENTAÇÃO                 │
│             (Frontend - HTML/CSS/JavaScript)            │
└────────────────┬────────────────────────────────────────┘
                 │
┌─────────────────▼────────────────────────────────────────┐
│                  CAMADA DE APLICAÇÃO                     │
│                   (Flask Blueprints)                      │
│  ┌─────────────┬──────────┬──────────┬──────────────┐   │
│  │  auth.py    │ admin.py │chat_bp   │security_bp   │   │
│  │  Autenticação│ Admin   │ Chat/IA  │ Segurança    │   │
│  └─────────────┴──────────┴──────────┴──────────────┘   │
└────────────────┬────────────────────────────────────────┘
                 │
┌─────────────────▼────────────────────────────────────────┐
│                  CAMADA DE LÓGICA                        │
│  ┌─────────────┬──────────┬──────────┬──────────────┐   │
│  │permissions  │ai_module │config.py │models.py     │   │
│  │(RBAC)       │(IA)      │(Config)  │(ORM)         │   │
│  └─────────────┴──────────┴──────────┴──────────────┘   │
└────────────────┬────────────────────────────────────────┘
                 │
┌─────────────────▼────────────────────────────────────────┐
│                  CAMADA DE DADOS                         │
│            SQLite (gestao_empresarial.db)                │
│  ┌─────────────────────────────────────────────────┐   │
│  │ usuarios │ produtos │ vendas │ funcionarios    │   │
│  │ logs │ chat │ alertas │ categorias │ comissões   │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Estrutura de Blueprints

### auth.py - Autenticação
```python
auth_bp = Blueprint('auth', __name__)

Routes:
    /login          → Página de login
    /registro       → Criar nova conta
    /logout         → Encerrar sessão
    /perfil         → Gerenciar perfil
    /perfil/edit    → Editar informações
    /perfil/senha   → Mudar senha

Decorators:
    @auth.before_app_request → Verificar usuário ativo
    @login_required         → Proteger rotas
```

### admin.py - Administração
```python
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

Routes:
    /dashboard      → Painel administrativo
    /usuarios       → Gerenciar usuários (CRUD)
    /funcionarios   → Gerenciar funcionários (CRUD)
    /ranking        → Ranking de vendedores
    /logs           → Visualizar audit logs
    /config         → Configurações

Decorators:
    @require_admin  → Apenas admin
    @require_gerente → Admin ou Gerente
```

### chat_routes.py - Chat IA
```python
chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

Routes:
    /              → Página do chat
    /api/enviar    → Processar pergunta (POST)
    /api/historico → Obter histórico (GET)
    /api/sugestoes → Sugestões inteligentes (GET)
    /api/limpar    → Limpar histórico (POST)
    /api/exportar  → Exportar conversa (GET)

Funcionalidades:
    - NLP para classificação de perguntas
    - 8 categorias automáticas
    - Salvamento de histórico
    - Integração com AnalysisEngine
```

### security_routes.py - Segurança
```python
security_bp = Blueprint('security', __name__)

Routes:
    /confirm-password         → Página de confirmação
    /api/confirm-password     → Processar confirmação (POST)
    /api/can-access/<resource> → Verificar acesso (GET)

Funcionalidades:
    - Session tracking de confirmação
    - Timeout de 15 minutos
    - Logging de tentativas falhas
    - Isolamento por usuário
```

### ai_module.py - Inteligência Artificial
```python
class AnalysisEngine:
    
    Métodos:
        gerar_insights()           → Análises automáticas
        gerar_dados_graficos()     → Dados para gráficos
        analisar_vendas()          → Análise de vendas
        prever_estoque()           → Previsão de estoque
        obter_recomendacoes()      → Recomendações
        processar_pergunta()       → Responder dúvidas
```

---

## 🔒 Sistema de Permissões

### Hierarquia de Acesso
```
ADMIN (nível 3)
├── Gerenciar usuários
├── Acessar relatórios financeiros
├── Ver audit logs
└── Configurações do sistema

GERENTE (nível 2)
├── Criar/editar vendas
├── Gerenciar estoque
├── Ver relatórios
└── Gerenciar clientes

FUNCIONÁRIO (nível 1)
├── Registrar vendas
├── Visualizar estoque
├── Chat com IA
└── Ver seu perfil
```

### Tabela de Permissões
```
Função            | Vendas | Estoque | Relatórios | Admin | Chat
─────────────────────────────────────────────────────────────
Admin             |   ✓    |   ✓     |     ✓      |  ✓   |  ✓
Gerente           |   ✓    |   ✓     |     ✓      |  ✗   |  ✓
Funcionário       |   ✓    |   ✓     |     ✗      |  ✗   |  ✓
```

### Decorators de Permissão
```python
@require_login              # Qualquer usuário autenticado
@require_admin              # Apenas admin
@require_gerente            # Admin ou gerente
@require_funcionario        # Qualquer permissão (padrão)
@password_confirmation_required  # Requer confirmação
```

---

## 📊 Fluxo de Autenticação

```
1. Usuário acessa /login
   ↓
2. Preenche email e senha
   ↓
3. Sistema verifica no banco (usuarios)
   ↓
4. Compara hash da senha com verify_password()
   ↓
5. Se válido:
   ├── Cria sessão com user_id
   ├── Atualiza ultimo_acesso
   ├── Redireciona para /dashboard
   └── Usuário logado ✓
   
6. Se inválido:
   ├── Exibe mensagem de erro
   └── Permanece em /login
```

---

## 💾 Modelo de Dados

### Tabela: usuarios
```
id              INT PRIMARY KEY
nome            TEXT NOT NULL
email           TEXT UNIQUE NOT NULL
senha           TEXT NOT NULL (hash)
tipo            TEXT (admin|gerente|funcionario)
data_criacao    TIMESTAMP
ultimo_acesso   TIMESTAMP
ativo           BOOLEAN
```

### Tabela: vendas
```
id              INT PRIMARY KEY
usuario_id      INT FOREIGN KEY
cliente_nome    TEXT
valor_total     FLOAT
data_venda      TIMESTAMP
funcionario_id  INT FOREIGN KEY (opcional)
```

### Tabela: produtos
```
id              INT PRIMARY KEY
usuario_id      INT FOREIGN KEY
nome            TEXT
quantidade      INT
preco           FLOAT
categoria_id    INT FOREIGN KEY
estoque_minimo  INT
ativo           BOOLEAN
```

### Tabela: logs_acao
```
id              INT PRIMARY KEY
usuario_id      INT FOREIGN KEY
tipo_acao       TEXT (CRIAR|ATUALIZAR|DELETAR)
tabela          TEXT (tabela afetada)
descricao       TEXT
data_acao       TIMESTAMP
funcionario_id  INT FOREIGN KEY
```

---

## 🔄 Fluxo de Venda

```
1. Admin vai para /vendas/nova
   ↓
2. Seleciona produtos e quantidades
   ↓
3. Sistema valida estoque
   ├── Se não houver estoque
   └── Retorna erro
   
4. Se validado:
   ├── Calcula valor total
   ├── Cria registro em vendas
   ├── Cria itens_venda para cada produto
   ├── Atualiza quantidade em produtos
   ├── Registra log em logs_acao
   └── Exibe sucesso
   
5. Dashboard atualiza automaticamente
```

---

## 🤖 Fluxo de IA Chat

```
1. Usuário digita pergunta em /chat
   ↓
2. JavaScript envia via AJAX para /chat/api/enviar
   ↓
3. Backend em chat_routes.py:
   ├── Classifica pergunta (NLP)
   ├── Determina categoria
   └── Seleciona processador
   
4. AnalysisEngine processa:
   ├── Analisa dados do banco
   ├── Gera insights
   └── Formula resposta
   
5. Resposta é:
   ├── Salva em chat_historico
   ├── Retornada ao frontend
   └── Exibida no chat

6. Sugestões carregam via /chat/api/sugestoes
   ├── Analisa histórico
   ├── Gera 3-4 sugestões
   └── Exibe como botões
```

---

## 🔐 Fluxo de Confirmação de Senha (Relatórios)

```
1. Admin tenta acessar /relatorios
   ↓
2. Sistema verifica se senha foi confirmada
   ├── Se SIM (menos de 15 min)
   └── Permite acesso
   
3. Se NÃO:
   ├── Redireciona para /security/confirm-password
   ├── Usuário digita senha
   └── Sistema verifica contra hash
   
4. Se válido:
   ├── Marca confirmação na sessão
   ├── Registra tempo
   ├── Cria log de acesso
   └── Permite acesso a relatórios
   
5. Timeout automático após 15 minutos
   └── Requer confirmação novamente
```

---

## 📱 Design Responsivo

### Breakpoints CSS
```
Desktop (> 1200px)
├── Sidebar 260px fixo à esquerda
├── Main área com 3+ colunas
└── Todos os elementos visíveis

Tablet (768px - 1200px)
├── Sidebar 260px
├── Main 1-2 colunas
└── Alguns elementos hidden

Mobile (< 768px)
├── Sidebar colapsável
├── Main full width
├── Stack vertical
└── Menu hamburger
```

### Componentes Responsivos
```
KPI Cards        → 1 coluna mobile, 2 tablet, 4 desktop
Tabelas          → Scroll horizontal mobile
Formulários      → Full width em mobile
Modais           → Ajustam tamanho automaticamente
Sidebar          → Oculta com toggle em mobile
```

---

## 🚀 Performance

### Otimizações Implementadas
- ✅ Índices no banco de dados
- ✅ Queries otimizadas com JOINs eficientes
- ✅ Paginação (10-20 itens por página)
- ✅ CSS variables (tema único)
- ✅ JavaScript vanilla (sem frameworks pesados)
- ✅ Lazy loading aonde possível

### Tempos Esperados
```
Carregar dashboard      ~ 200-300ms
Registrar venda         ~ 150-200ms
Buscar relatório        ~ 300-500ms
Obter resposta IA       ~ 100-200ms (local)
```

---

## 🎯 Fluxo de Navegação

```
GUEST
└── / (redireciona para login)
    └── /login (/auth/login)
        └── Preenche credenciais
            ├── Inválido → Erro
            └── Válido ↓

USUÁRIO AUTENTICADO
├── /dashboard
│   ├── KPI Cards (vendas dia/semana/mês)
│   ├── Produtos estoque baixo
│   ├── Produto mais vendido
│   └── Insights do dia
│
├── /estoque
│   ├── Listar produtos
│   ├── /estoque/adicionar
│   ├── /estoque/editar/<id>
│   └── /estoque/deletar/<id>
│
├── /vendas
│   ├── Histórico de vendas
│   ├── /vendas/nova
│   └── Filtros por período
│
├── /chat
│   ├── Interface de conversa
│   ├── Histórico
│   ├── Sugestões inteligentes
│   └── /chat/api/* (API endpoints)
│
└── /relatorios (requer confirmação)
    ├── Top 10 produtos vendidos
    ├── Bottom 10 produtos
    ├── Filter por período
    └── Exportar dados

ADMIN ADICIONAL
├── /admin/dashboard
├── /admin/usuarios
├── /admin/funcionarios
├── /admin/ranking
├── /admin/logs
└── /admin/config

TODOS
└── /perfil
    ├── Ver informações pessoais
    ├── Editar nome
    └── Mudar senha
```

---

## 📚 Arquivos Importantes

### Arquivos Essenciais
```
app.py              - Ponto de entrada
models.py           - Banco de dados
config.py           - Configurações
permissions.py      - Autenticação/Autorização
```

### Blueprints
```
auth.py             - Sistema de login
admin.py            - Painel admin
chat_routes.py      - Chat IA
security_routes.py  - Segurança
ai_module.py        - Motor IA
```

### Diretórios
```
static/             - CSS, JS, imagens
templates/          - HTML Jinja2
templates/components/ - Includes reutilizáveis
templates/admin/    - Templates admin
templates/chat/     - Templates chat
templates/security/ - Templates segurança
```

---

## 🔄 Ciclo de Desenvolvimento

### Para Adicionar Nova Feature

1. **Adicionar rota em app.py ou novo blueprint**
   ```python
   @app.route('/nova-feature')
   @require_login
   def nova_feature():
       return render_template('nova_feature.html')
   ```

2. **Criar template em templates/**
   ```html
   {% extends "base.html" %}
   {% block content %}
       <!-- seu HTML aqui -->
   {% endblock %}
   ```

3. **Se precisar de dados:**
   ```python
   # Adicionar em models.py
   class NovaEntidade:
       @staticmethod
       def criar(dados):
           # SQL INSERT
   ```

4. **Proteger com permissões:**
   ```python
   @require_admin  # ou @require_gerente, @require_login
   def nova_feature():
       pass
   ```

5. **Testar:**
   - Acesse http://localhost:5000/nova-feature
   - Verifique console do navegador
   - Verifique logs do servidor

---

## 📖 Referências Rápidas

### Variáveis de Sessão
```python
session['user_id']      # ID do usuário logado
session['user_email']   # Email do usuário
session['user_tipo']    # Tipo (admin/gerente/funcionario)
```

### Funções Úteis
```python
get_db()                           # Conexão com banco
User.obter_usuario_por_id(id)      # Buscar usuário
hash_password(senha)               # Hash de senha
verify_password(senha, hash)       # Verificar senha
```

### Helpers de Template
```jinja2
{% if 'user_id' in session %}
    <!-- Usuário autenticado -->
{% endif %}

{% if session.get('user_tipo') == 'admin' %}
    <!-- Opções de admin -->
{% endif %}
```

---

**Documento de Arquitetura**
**Versão: 1.0.0**
**Data: Março 2026**
