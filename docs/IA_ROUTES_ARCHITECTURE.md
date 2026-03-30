# 📡 MAPA DE ROTAS E ARQUITETURA DA IA

## 🏗️ ARQUITETURA GERAL

```
┌─────────────────────────────────────────────────────────────────────┐
│                         APLICAÇÃO FLASK                             │
│  (app.py)                                                           │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ├─ register_blueprint(auth_bp)
                              ├─ register_blueprint(ai_bp)      ← AI
                              ├─ register_blueprint(admin_bp)
                              ├─ register_blueprint(chat_bp)    ← Chat/IA
                              └─ register_blueprint(security_bp)
```

---

## 🛣️ MAPA COMPLETO DE ROTAS

### 1. BLUEPRINT: chat_bp (url_prefix='/chat')

```
📍 Rota Raiz
────────────────────────────────────────────────────────────────
GET /chat/
    Função: chat_routes.py → index()
    Nome em Flask: chat.index
    Decoradores: @require_login
    Retorna: template 'chat/index.html'
    Histórico: Carrega últimas 20 conversas
    Status: ✅ FUNCIONA

    User
    ├─ nome: string
    └─ historico: List[ChatMessage]
           ┌─────────────────────┐
           │ pergunta: string    │
           │ resposta: string    │
           │ tipo_pergunta: str  │
           │ data_criacao: ISO   │
           └─────────────────────┘

────────────────────────────────────────────────────────────────
POST /chat/api/enviar
    Função: chat_routes.py → enviar_pergunta()
    Nome em Flask: chat.enviar_pergunta
    Decoradores: @login_required_for_chat
    Content-Type: application/json
    
    INPUT:
    {
      "pergunta": "Quanto vendi hoje?"
    }
    
    PROCESSAMENTO:
    1. Valida pergunta (não vazia, < 500 caracteres)
    2. engine = AnalysisEngine(user_id)
    3. resposta = engine.analisar_pergunta(pergunta)
    4. tipo_pergunta = classificar_pergunta(pergunta)
    5. ChatHistorico.salvar_conversa(...)
    6. Log.registrar_acao(...)
    
    OUTPUT:
    {
      "sucesso": true,
      "pergunta": "Quanto vendi hoje?",
      "resposta": "Você vendeu R$ XXXX.XX hoje.",
      "tipo": "vendas",
      "timestamp": "2024-03-20T10:30:00"
    }
    
    Status: ✅ FUNCIONA
    Erros: 400 pergunta vazia, 401 não autorizado, 500 erro servidor

────────────────────────────────────────────────────────────────
GET /chat/api/historico
    Função: chat_routes.py → obter_historico()
    Nome em Flask: chat.obter_historico
    Decoradores: @login_required_for_chat
    Query Params: ?pagina=1&limite=50
    
    OUTPUT:
    {
      "sucesso": true,
      "historico": [
        {
          "id": 1,
          "pergunta": "Quanto vendi hoje?",
          "resposta": "Você vendeu R$ XXXX.XX hoje.",
          "tipo": "vendas",
          "data": "2024-03-20",
          "timestamp": "20/03/2024 10:30:00"
        },
        ...
      ],
      "total": 20
    }
    
    Status: ✅ FUNCIONA

────────────────────────────────────────────────────────────────
GET /chat/api/sugestoes
    Função: chat_routes.py → obter_sugestoes()
    Nome em Flask: chat.obter_sugestoes
    Decoradores: @login_required_for_chat
    
    OUTPUT:
    {
      "sucesso": true,
      "sugestoes": [
        {
          "titulo": "Vendas de Hoje",
          "pergunta": "Quanto eu vendi hoje?",
          "icon": "bar-chart",
          "categoria": "vendas"
        },
        {
          "titulo": "Produto Mais Vendido",
          "pergunta": "Qual meu produto mais vendido?",
          "icon": "trophy",
          "categoria": "produtos"
        },
        {
          "titulo": "Estoque Baixo",
          "pergunta": "Qual produto está com estoque baixo?",
          "icon": "alert-triangle",
          "categoria": "estoque"
        },
        {
          "titulo": "Total em Estoque",
          "pergunta": "Quanto eu tenho em estoque?",
          "icon": "packages",
          "categoria": "estoque"
        },
        {
          "titulo": "Faturamento da Semana",
          "pergunta": "Quanto vendi nesta semana?",
          "icon": "trending-up",
          "categoria": "vendas"
        },
        {
          "titulo": "Clientes",
          "pergunta": "Quantos clientes eu tenho?",
          "icon": "users",
          "categoria": "clientes"
        },
        {
          "titulo": "Previsão de Estoque",
          "pergunta": "Quando meu estoque vai acabar?",
          "icon": "calendar",
          "categoria": "previsao"
        },
        {
          "titulo": "Recomendações",
          "pergunta": "Que sugestões você tem para mim?",
          "icon": "lightbulb",
          "categoria": "insights"
        }
      ]
    }
    
    Status: ✅ FUNCIONA

────────────────────────────────────────────────────────────────
POST /chat/api/limpar-historico
    Função: chat_routes.py → limpar_historico()
    Nome em Flask: chat.limpar_historico
    Decoradores: @login_required_for_chat
    
    OUTPUT:
    {
      "sucesso": true,
      "mensagem": "Histórico de chat limpo com sucesso"
    }
    
    Status: ✅ FUNCIONA

────────────────────────────────────────────────────────────────
GET /chat/api/exportar-historico
    Função: chat_routes.py → exportar_historico()
    Nome em Flask: chat.exportar_historico
    Decoradores: @login_required_for_chat
    
    OUTPUT: JSON com todo histórico de chat do usuário
    
    Status: ✅ FUNCIONA

────────────────────────────────────────────────────────────────
GET /chat/api/insights-rapidos
    Função: chat_routes.py → insights_rapidos()
    Nome em Flask: chat.insights_rapidos
    Decoradores: @login_required_for_chat
    
    OUTPUT: Insights rápidos sobre vendas, estoque, etc.
    
    Status: ✅ FUNCIONA
```

---

### 2. BLUEPRINT: ai_bp (url_prefix='/api/ia')

```
────────────────────────────────────────────────────────────────
GET /api/ia/insights
    Função: ai_module.py → obter_insights()
    Nome em Flask: ai.obter_insights
    Decoradores: @login_required_api
    
    PROCESSAMENTO:
    1. engine = AnalysisEngine(session['user_id'])
    2. insights = engine.gerar_insights()
    3. Salva em tabela analises_ia (cache)
    
    OUTPUT:
    {
      "sucesso": true,
      "insights": [
        {
          "titulo": "🚀 Excelente Crescimento!",
          "descricao": "Vendas subiram 45.2% hoje em relação a ontem!",
          "tipo": "success",
          "urgencia": "alta",
          "valor": "+45.2%"
        },
        ...
      ],
      "total": 6
    }
    
    Métodos Internos Chamados:
    ├─ _analisar_crescimento_vendas()
    ├─ _analisar_estoque_critico()
    ├─ _analisar_produtos_destaque()
    ├─ _analisar_baixa_rotacao()
    ├─ _analisar_tendencias()
    └─ _analisar_oportunidades()
    
    Status: ✅ FUNCIONA

────────────────────────────────────────────────────────────────
GET /api/ia/previsoes
    Função: ai_module.py → obter_previsoes()
    Nome em Flask: ai.obter_previsoes
    Decoradores: @login_required_api
    
    PROCESSAMENTO:
    engine.prever_falta_estoque()
    
    OUTPUT:
    {
      "sucesso": true,
      "previsoes": [
        {
          "produto": "Produto A",
          "dias_restantes": 3,
          "quantidade_atual": 15,
          "velocidade_diaria": 5.0
        },
        ...
      ],
      "critica": [
        // Produtos com <= 3 dias de estoque
      ]
    }
    
    Status: ✅ FUNCIONA

────────────────────────────────────────────────────────────────
GET /api/ia/recomendacoes
    Função: ai_module.py → obter_recomendacoes()
    Nome em Flask: ai.obter_recomendacoes
    Decoradores: @login_required_api
    
    PROCESSAMENTO:
    engine.gerar_recomendacoes()
    
    OUTPUT:
    {
      "sucesso": true,
      "recomendacoes": [
        {
          "titulo": "Revisão de Produtos",
          "descricao": "Alguns produtos têm baixa rotação...",
          "tipo": "info"
        },
        ...
      ]
    }
    
    Status: ✅ FUNCIONA

────────────────────────────────────────────────────────────────
GET /api/ia/graficos
    Função: ai_module.py → obter_dados_graficos()
    Nome em Flask: ai.obter_dados_graficos
    Decoradores: @login_required_api
    
    PROCESSAMENTO:
    engine.gerar_dados_graficos()
    
    OUTPUT:
    {
      "sucesso": true,
      "dados": {
        "vendas_7dias": [
          {"data": "14/03", "valor": 1500.00},
          {"data": "15/03", "valor": 2000.00},
          ...
          {"data": "20/03", "valor": 1800.00}
        ],
        "top_produtos": [
          {"nome": "Produto A", "quantidade": 45},
          {"nome": "Produto B", "quantidade": 32},
          ...
        ]
      }
    }
    
    Status: ✅ FUNCIONA

────────────────────────────────────────────────────────────────
POST /api/ia/chat
    Função: ai_module.py → chat_ia()
    Nome em Flask: ai.chat_ia
    Decoradores: @login_required_api
    Content-Type: application/json
    
    INPUT:
    {
      "pergunta": "Qual é meu melhor produto?"
    }
    
    PROCESSAMENTO:
    1. Valida pergunta (não vazia)
    2. engine = AnalysisEngine(session['user_id'])
    3. resposta = engine.analisar_pergunta(pergunta)
    
    OUTPUT:
    {
      "pergunta": "Qual é meu melhor produto?",
      "resposta": "🏆 Seu melhor produto é \"Produto A\" com R$ 15000.00 de receita total.",
      "timestamp": "2024-03-20T10:30:00"
    }
    
    Status: ✅ FUNCIONA
```

---

### 3. ROTAS DIRETAS EM app.py

```
────────────────────────────────────────────────────────────────
GET /chat
    Função: app.py → chat()
    Nome em Flask: chat
    Decoradores: @require_login
    
    PROBLEMA ATUAL:
    └─ renderiza: templates/chat.html ⚠️ (com erro de rota)
    
    RECOMENDADO:
    └─ redirecionar: para url_for('chat.index') → /chat/
    
    Status: ⚠️ EM CONFLITO
```

---

## 📊 TABELA DE MÉTODOS AnalysisEngine

```
┌─────────────────────────────────────────┬──────────────────────┬──────────────────────────────┐
│ Método                                  │ Retorna              │ Descrição                    │
├─────────────────────────────────────────┼──────────────────────┼──────────────────────────────┤
│ __init__(usuario_id)                    │ -                    │ Inicializa com datas refs    │
│ gerar_insights()                        │ List[Dict]           │ 6 tipos de análise           │
│ _analisar_crescimento_vendas()          │ List[Dict]           │ Análise diária/semanal       │
│ _analisar_estoque_critico()             │ List[Dict]           │ Produtos com estoque baixo   │
│ _analisar_produtos_destaque()           │ List[Dict]           │ Tops produtos da semana      │
│ _analisar_baixa_rotacao()               │ List[Dict]           │ Produtos sem vendas          │
│ _analisar_tendencias()                  │ List[Dict]           │ Padrões de venda             │
│ _analisar_oportunidades()               │ List[Dict]           │ Chance de ganho de receita   │
│ prever_falta_estoque()                  │ List[Dict]           │ Previsões por produto        │
│ gerar_recomendacoes()                   │ List[Dict]           │ Sugestões inteligentes       │
│ gerar_dados_graficos()                  │ Dict                 │ Dados para gráficos          │
│ analisar_pergunta(pergunta)             │ String               │ Responde em linguagem nat.   │
└─────────────────────────────────────────┴──────────────────────┴──────────────────────────────┘
```

---

## 🔗 FLUXO DE DADOS: Pergunta → Resposta

### Cenário: Usuário pergunta "Quanto vendi hoje?"

```
┌────────────────────────────────────────────────────────────────────┐
│ 1. USUÁRIO INTERAGE NO FRONTEND                                   │
└────────────────────────────────────────────────────────────────────┘
            │
            ├─ Digita pergunta no <input class="chat-input">
            ├─ Clica botão "Enviar" ou pressiona Enter
            └─ JavaScript event listener dispara

┌────────────────────────────────────────────────────────────────────┐
│ 2. JAVASCRIPT ENVIA REQUISIÇÃO                                     │
└────────────────────────────────────────────────────────────────────┘
            │
            ├─ Método: POST
            ├─ URL: /chat/api/enviar
            ├─ Headers: { 'Content-Type': 'application/json' }
            ├─ Body: { "pergunta": "Quanto vendi hoje?" }
            └─ Exibe mensagem do usuário no DOM

┌────────────────────────────────────────────────────────────────────┐
│ 3. BACKEND PROCESSA (chat_routes.py)                               │
└────────────────────────────────────────────────────────────────────┘
            │
            ├─ enviar_pergunta() validação:
            │  ├─ Não vazia?  ✓
            │  ├─ < 500 chars? ✓
            │  └─ GET user_id from session
            │
            ├─ engine = AnalysisEngine(user_id)
            │
            ├─ resposta = engine.analisar_pergunta("Quanto vendi hoje?")
            │           → Busca no SELECT: COALESCE(SUM(valor_total), 0)
            │           → Retorna: "Você vendeu R$ 5000.00 hoje."
            │
            ├─ tipo_pergunta = classificar_pergunta("Quanto vendi hoje?")
            │           → Detec: "vendi" em patterns['vendas']
            │           → Retorna: "vendas"
            │
            ├─ ChatHistorico.salvar_conversa(user_id, pergunta, resposta, tipo)
            │           → INSERT INTO chat_historico
            │
            ├─ Log.registrar_acao(user_id, 'CHAT_PERGUNTA', ...)
            │           → INSERT INTO logs
            │
            └─ return jsonify({
                 "sucesso": true,
                 "pergunta": "Quanto vendi hoje?",
                 "resposta": "Você vendeu R$ 5000.00 hoje.",
                 "tipo": "vendas",
                 "timestamp": "2024-03-20T10:30:00"
               })

┌────────────────────────────────────────────────────────────────────┐
│ 4. JAVASCRIPT RECEBE E EXIBE RESPOSTA                              │
└────────────────────────────────────────────────────────────────────┘
            │
            ├─ Parse JSON response
            ├─ Cria novo <div class="chat-message assistant">
            ├─ Insere no DOM
            ├─ Faz scroll para o fim
            └─ Re-habilita botão de envio

┌────────────────────────────────────────────────────────────────────┐
│ 5. USUÁRIO VÊ RESPOSTA NA TELA                                     │
└────────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ BANCO DE DADOS

### Tabela: chat_historico
```sql
CREATE TABLE chat_historico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    pergunta TEXT NOT NULL,
    resposta TEXT NOT NULL,
    tipo_pergunta TEXT,           -- 'vendas', 'produtos', 'estoque', etc.
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)
```

### Tabela: analises_ia (Cache)
```sql
CREATE TABLE analises_ia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    tipo TEXT,                     -- 'insights', 'previsoes', etc.
    dados_json TEXT,              -- JSON serializado
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)
```

---

## 📝 EXEMPLOS DE PERGUNTAS E RESPOSTAS

### 1. Vendas
```
P: "Quanto vendi hoje?"
R: "Você vendeu R$ 5000.00 hoje."

P: "Qual é meu faturamento?"
R: "Você vendeu um total de R$ 125000.00."

P: "Quanto vendi nesta semana?"
R: "Você vendeu R$ 35000.00 nesta semana em 12 transações."

P: "Quanto vendi neste mês?"
R: "Seu faturamento do mês é R$ 150000.00."
```

### 2. Produtos
```
P: "Qual meu produto mais vendido?"
R: "Seu produto mais vendido é \"Produto A\" com 150 unidades vendidas."

P: "Qual é o melhor produto?"
R: "🏆 Seu melhor produto é \"Produto A\" com R$ 50000.00 de receita total."

P: "Qual é o pior produto?"
R: "📉 \"Produto X\" nunca foi vendido. Considere revisar seu preço ou remover."

P: "Quantos produtos eu tenho?"
R: "Você tem 25 produtos no catálogo."
```

### 3. Estoque
```
P: "Quanto eu tenho em estoque?"
R: "Você possui 5000 itens em estoque no total."

P: "Qual produto está com estoque baixo?"
R: "Estes produtos têm estoque baixo: \"Produto A\" (5 unidades), \"Produto B\" (3 unidades)"

P: "Quando meu estoque vai acabar?"
R: [Lista de produtos com dias restantes]
```

### 4. Clientes
```
P: "Quantos clientes eu tenho?"
R: "Você tem 45 clientes registrados."
```

### 5. Análises
```
P: "Qual é o meu ticket médio?"
R: "Seu ticket médio é de R$ 523.45."

P: "Qual foi minha venda mínima?"
R: "Sua menor venda foi R$ 50.00."

P: "Qual foi minha venda máxima?"
R: "Sua maior venda foi R$ 8500.00."

P: "Qual é o meu lucro?"
R: "Seu lucro total é aproximadamente R$ 25000.00."
```

### 6. Recomendações
```
P: "Que sugestões você tem para mim?"
R: "💡 Minhas recomendações:
    - Revisão de Produtos: Alguns produtos têm baixa rotação...
    - Oportunidade de Maximização: \"Produto A\" é seu produto mais vendido..."
```

### 7. Padrão Fallback
```
P: "Como você está?"
R: "Desculpe, não consegui entender sua pergunta. Tente perguntar sobre: vendas de hoje, produtos mais vendidos, estoque, clientes, etc."
```

---

## 📈 CATEGORIAS DE PERGUNTAS

Classificação automática por `classificar_pergunta()`:

```
'vendas'        → ['vendi', 'venda', 'faturamento', etc.]
'produtos'      → ['produto', 'melhores', 'destaque', etc.]
'estoque'       → ['estoque', 'quantidade', 'stock', etc.]
'clientes'      → ['cliente', 'clientes', 'quantos clientes', etc.]
'financeiro'    → ['lucro', 'ganho', 'ganhos', 'margem', etc.]
'previsao'      → ['quando', 'vai acabar', 'previsão', etc.]
'comportamento' → ['crescimento', 'tendência', 'padrão', etc.]
'geral'         → ['ajuda', 'sugestão', 'recomendação', etc.]
'outro'         → [padrão final]
```

---

## 🔐 Autenticação e Permissões

```
Decorador: @require_login
├─ Verifica: 'user_id' in session
├─ Se falso: redireciona para login
└─ Se verdadeiro: continua execução

Decorador: @login_required_api
├─ Verifica: 'user_id' in session
├─ Se falso: retorna JSON 401 'Não autorizado'
└─ Se verdadeiro: continua execução

Decorador: @login_required_for_chat (em chat_routes.py)
├─ Verifica: 'user_id' in session
├─ Se falso: retorna JSON 401 'Não autorizado'
└─ Se verdadeiro: continua execução
```

---

## 🎯 Status Final

| Componente | Status | Notas |
|------------|--------|-------|
| Chat Routes (7 endpoints) | ✅ OK | Todos implementados |
| AI Routes (5 endpoints) | ✅ OK | Todos implementados |
| AnalysisEngine | ✅ OK | 11 métodos |
| Templates | ⚠️ PARCIAL | chat.html com erro, index.html OK |
| JavaScript | ✅ OK | AJAX implementado |
| Decoradores | ✅ OK | 3 tipos |
| Banco de dados | ✅ OK | Tabelas criadas |
| Autenticação | ✅ OK | Protegida |

