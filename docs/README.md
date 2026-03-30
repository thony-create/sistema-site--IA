# Cognix - Gestão Inteligente com Zyra

Um sistema web completo para gerenciamento de vendas, estoque, clientes e funcionários com inteligência artificial integrada, construído com Flask e SQLite.

## 🎯 Funcionalidades Principais

### Autenticação e Permissões
- ✅ Sistema de login e registro de usuários
- ✅ Três níveis de acesso: Admin, Gerente e Funcionário
- ✅ Controle granular de permissões por funcionalidade
- ✅ Gerenciamento de sessões com logout

### Dashboard Inteligente
- 📊 Indicadores de vendas (dia, semana, mês)
- 📈 Gráficos de vendas em tempo real
- 🔴 Alertas de estoque baixo
- 🏆 Produtos mais vendidos
- 🤖 Insights automáticos gerados por IA

### Gestão de Vendas
- 💳 Registro rápido de vendas
- 📋 Histórico completo com filtros por período
- 🔄 Atualização automática de estoque
- 👥 Associação com clientes

### Controle de Estoque
- 📦 Cadastro de produtos com categorias
- 🎯 Alertas automáticos de baixo estoque
- 📊 Previsão de quando o estoque vai acabar
- 🔔 Notificações de produtos que precisam reposição

### Gestão de Clientes
- 👤 Cadastro de cliente com histórico
- 📞 Informações de contato (email, telefone, CP F)
- 🛒 Histórico completo de compras por cliente
- 📈 Análise de clientes premium

### Gestão de Funcionários
- 👥 Cadastro e perfil de funcionários
- 💰 Controle de salários e comissões
- 🏅 Ranking de vendedores
- 📊 Performance individual
- 🔗 Associação com usuários do sistema

### Relatórios e Analytics
- 📋 Relatórios diários, semanais e mensais
- 💹 Análise de vendas por período
- 🏆 Produtos mais vendidos e com menor saída
- 🔐 Acesso protegido com confirmação de senha
- 💾 Exportação de dados

### Zyra - Consultora Inteligente (Chat)
- 🤖 Perguntas em linguagem natural
- 📊 Análise de vendas: "Quanto eu vendi hoje?"
- 📦 Consultas de estoque: "Qual produto está com estoque baixo?"
- 🏆 Informações de produtos: "Qual meu produto mais vendido?"
- 💡 Sugestões inteligentes context-aware
- 📝 Histórico de conversas
- 💾 Exportação de histórico

### Inteligência Artificial
- 📈 Análise automática de crescimento/queda de vendas
- ⚠️ Alertas de anomalias e padrões
- 🔮 Previsões de falta de estoque
- 💡 Recomendações de precificação
- 🎯 Sugestões de cross-selling
- 📊 Insights sobre comportamento de vendas

### Segurança
- 🔐 Autenticação com hash de senhas (bCrypt)
- 🛡️ Confirmação de senha para dados sensíveis
- 📝 Auditoria completa de ações (logs)
- 🚫 Controle de permissões por função
- 🔒 Sessões seguras com HTTPOnly cookies

### Interface Moderna
- 🎨 Design profissional estilo SaaS
- 📱 Responsivo (funciona em mobile)
- ⚡ Transições suaves e animações
- 🎯 Sidebar intuitiva com navegação por categorias
- 🌈 Paleta de cores moderna (azul, cinza, branco)
- 📐 Tipografia Poppins + Inter

## 🛠️ Tecnologias

- **Backend**: Python 3.8+ com Flask 2.3+
- **Banco de dados**: SQLite (estrutura relacional completa)
- **Frontend**: HTML5, CSS3 (variáveis CSS, grid, flexbox), JavaScript vanilla
- **Autenticação**: Werkzeug security (generate_password_hash)
- **Análise de Dados**: Queries SQL otimizadas
- **IA**: Análise heurística de dados (não requer modelos ML externos)

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- 100MB de espaço em disco

## 🚀 Instalação

### 1. Clone ou baixe o projeto
```bash
cd seu-projeto-gestao
```

### 2. Criar ambiente virtual (recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Executar o servidor
```bash
python app.py
```

O sistema estará disponível em: `http://localhost:5000`

## 📦 Estrutura do Projeto

```
├── app.py                  # Aplicação principal Flask
├── models.py              # Modelos de banco de dados
├── auth.py                # Autenticação e rotas de login
├── admin.py               # Painel administrativo
├── chat_routes.py         # Rotas do assistente de chat
├── ai_module.py           # Motor de IA e analytics
├── security_routes.py     # Rotas de segurança
├── permissions.py         # Sistema de permissões
├── config.py              # Configurações
├── requirements.txt       # Dependências Python
├── static/
│   └── style.css          # CSS moderno SaaS
├── templates/
│   ├── login.html         # Página de login
│   ├── registro.html      # Página de registro
│   ├── dashboard.html     # Dashboard principal
│   ├── perfil.html        # Perfil do usuário
│   ├── components/
│   │   ├── sidebar.html   # Barra lateral
│   │   └── header.html    # Cabeçalho
│   ├── chat/
│   │   └── index.html     # Chat assistente
│   ├── security/
│   │   └── confirm_password.html  # Confirmação de senha
│   └── admin/
│       ├── dashboard.html        # Painel admin
│       ├── usuarios.html         # Gerenciar usuários
│       └── funcionarios.html     # Gerenciar funcionários
└── gestao_empresarial.db  # Banco de dados (criado automaticamente)
```

## 🎓 Primeiros Passos

### 1. Criar primeira conta (Admin)
- Vá para `http://localhost:5000/registro`
- Preencha nome, email e senha
- A primeira conta criada automaticamente se torna Admin

### 2. Adicionar Produtos
- Navegue para "Estoque" → "Adicionar Produto"
- Preencha nome, quantidade, preço e categoria
- Defina estoque mínimo para alertas

### 3. Registrar Vendas
- Vá para "Vendas" → "Nova Venda"
- Selecione produtos e quantidade
- O estoque é atualizado automaticamente

### 4. Visualizar Dashboard
- Veja indicadores em tempo real
- Leia insights automáticos da IA
- Monitore estoque baixo

### 5. Usar IA Chat
- Clique em "Zyra" na sidebar
- Faça perguntas como:
  - "Quanto eu vendi hoje?"
  - "Qual produto está com estoque baixo?"
  - "Qual meu produto mais vendido?"

## 👥 Perfis de Acesso

### Admin (Acesso Total)
- Gerenciar usuários e permissões
- Acessar relatórios financeiros
- Gerenciar funcionários
- Visualizar logs de auditoria
- Configurar sistema

### Gerente (Acesso Amplo)
- Visualizar relatórios e analytics
- Registrar vendas
- Gerenciar estoque
- Gerenciar clientes
- ❌ NÃO pode gerenciar usuarios

### Funcionário (Acesso Básico)
- Registrar vendas
- Visualizar estoque
- Usar assistente IA
- ❌ NÃO pode ver dados financeiros
- ❌ NÃO pode gerenciar inventário

## 🔐 Segurança

### Boas Práticas Implementadas
- ✅ Senhas hasheadas com Werkzeug security
- ✅ Confirmação de senha para dados sensíveis
- ✅ Auditoria completa em logs_acao
- ✅ Isolamento de dados por usuário
- ✅ Controle de permissões granular
- ✅ Sessões seguras

### Para Produção (Importante!)
Antes de colocar em produção:

1. Mude a SECRET_KEY no `config.py`:
```python
SECRET_KEY = 'sua-chave-segura-muito-longa-aleatoria'
```

2. Ative HTTPS:
```python
SESSION_COOKIE_SECURE = True
```

3. Configure banco de dados robusto (PostgreSQL)

4. Use um web server (Gunicorn) em vez do Flask dev server

5. Configure variáveis de ambiente para credenciais

## 🤖 Como a IA Funciona

O sistema inclui análises inteligentes que:

1. **Detecta Tendências**: Compara vendas de períodos diferentes
2. **Alerta sobre Anomalias**: Identifica quedas ou picos anormais
3. **Prevê Falta de Estoque**: Usa histórico de venda para prever quando vai acabar
4. **Recomenda Ações**: Sugere aumentos de preço em produtos mais vendidos
5. **Responde em Linguagem Natural**: Processa perguntas e retorna respostas contextuais

Não usa APIs externas - tudo funciona localmente!

## 📊 Exemplos de Queries

O sistema otimiza queries para performance:

```sql
-- Produtos mais vendidos
SELECT p.nome, SUM(iv.quantidade)
FROM itens_venda iv
JOIN produtos p ON iv.produto_id = p.id
GROUP BY p.id
ORDER BY SUM(iv.quantidade) DESC

-- Revenue em período
SELECT SUM(valor_total)
FROM vendas
WHERE DATE(data_venda) BETWEEN '2024-01-01' AND '2024-01-31'

-- Vendedores top
SELECT f.nome, COUNT(v.id), SUM(v.valor_total)
FROM funcionarios f
LEFT JOIN vendas v ON f.id = v.funcionario_id
GROUP BY f.id
ORDER BY SUM(v.valor_total) DESC
```

## 🐛 Troubleshooting

### Erro: "database is locked"
- Feche outras conexões ao banco
- Reinicie o servidor

### Erro: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Erro: "ModuleNotFoundError: No module named 'models'"
- Certifique-se de estar no diretório correto (root do projeto)
- Verifique se models.py existe

### Dashboard não aparece dados
- Certifique-se de ter registrado vendas
- Verifique se os produtos estão cadastrados
- Veja o console para erros SQL

## 📈 Próximas Melhorias

- [ ] Integração com APIs de pagamento (Stripe, PagSeguro)
- [ ] WhatsApp notifications
- [ ] Mobile app nativa
- [ ] Backup automático em nuvem
- [ ] Integração com contabilidade
- [ ] Previsões com Machine Learning
- [ ] Integração com Marketplace (AliExpress, Amazon)
- [ ] Sistema de nota fiscal eletrônica

## 📞 Suporte

Para bugs ou sugestões, abra uma issue ou entre em contato.

## 📄 Licença

MIT License - Este projeto é open-source e pode ser usado livremente.

---

**Versão**: 1.0.0  
**Último update**: Março 2026  
**Status**: ✅ Produção
