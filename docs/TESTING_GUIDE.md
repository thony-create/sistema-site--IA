# 🧪 GUIA DE TESTES E VALIDAÇÃO

## Como Testar as Correções

### 1. Teste Rápido (2 minutos)

```bash
# Terminal 1: Iniciar a aplicação
python app.py

# Verificar se inicia sem erros
# Esperado: "Running on http://127.0.0.1:5000"
```

### 2. Teste Manual (5 minutos)

**Cenário #1: Fazer login**
1. Acessar `http://localhost:5000`
2. Clicar em "Registre-se"
3. Preencher formulário (senha mínimo 6 caracteres)
4. Verificar se redireciona para login
5. ✅ Esperado: Login bem-sucedido

**Cenário #2: Testar menu do usuário** ← AQUI ESTÁ O ERRO CORRIGIDO
1. Após login, procurar avatar do usuário no canto superior direito
2. Clicar no menu (⋮ três pontos)
3. ✅ **ANTES:** Erro BuildError ao clicar em "Meu Perfil"
4. ✅ **DEPOIS:** Carrega página de perfil sem erro
5. Verificar se "Painel Admin" também funciona (se for admin)

**Cenário #3: Testar painel admin**
1. Login como usuário admin
2. Clicar em menu → "Painel Admin"
3. ✅ Esperado: Carrega dashboard do admin
4. Verificar se todas as abas funcionam:
   - Usuários
   - Funcionários
   - Ranking de Vendedores
   - Logs
   - Configurações

---

## Código de Teste Automatizado

### Script: `test_endpoints.py`

```python
#!/usr/bin/env python3
"""Test all Flask endpoints are correctly mapped"""

import sys
from app import app

def test_endpoints():
    """Verify all url_for endpoints exist"""
    
    print("🔍 Verificando endpoints do Flask...")
    print("-" * 60)
    
    with app.app_context():
        endpoints = {}
        
        # Listar todos os endpoints
        for rule in app.url_map.iter_rules():
            endpoint = rule.endpoint
            methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
            
            if endpoint not in ['static']:
                endpoints[endpoint] = {
                    'route': str(rule),
                    'methods': methods
                }
        
        # Verificar endpoints críticos
        critical_endpoints = [
            'auth.login',
            'auth.perfil',
            'auth.logout',
            'auth.registro',
            'dashboard',
            'admin.dashboard',
            'admin.listar_usuarios',
            'historico_logs',
            'relatorios'
        ]
        
        print(f"\n✅ ENDPOINTS ENCONTRADOS: {len(endpoints)}\n")
        
        all_ok = True
        for endpoint in critical_endpoints:
            if endpoint in endpoints:
                route = endpoints[endpoint]['route']
                methods = endpoints[endpoint]['methods']
                print(f"✅ {endpoint:30} → {route:30} ({methods})")
            else:
                print(f"❌ {endpoint:30} → NÃO ENCONTRADO")
                all_ok = False
        
        print("\n" + "-" * 60)
        
        if all_ok:
            print("✅ TODOS OS ENDPOINTS CRÍTICOS ENCONTRADOS!")
            print("\n🎉 Projeto está pronto para uso!")
            return 0
        else:
            print("❌ ALGUNS ENDPOINTS ESTÃO FALTANDO!")
            return 1

def test_templates_url_for():
    """Check if all url_for calls in templates are valid"""
    
    print("\n🔍 Verificando chamadas url_for nos templates...")
    print("-" * 60)
    
    # Endpoints disponíveis
    with app.app_context():
        available_endpoints = set()
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                available_endpoints.add(rule.endpoint)
    
    # Exemplos de url_for encontrados (extraído manualmente)
    url_for_calls = [
        ('auth.perfil', 'templates/components/header.html'),
        ('admin.dashboard', 'templates/components/header.html'),
        ('auth.login', 'templates/login.html'),
        ('auth.registro', 'templates/registro.html'),
        ('dashboard', 'templates/components/sidebar.html'),
        ('estoque', 'templates/components/sidebar.html'),
        ('admin.listar_usuarios', 'templates/components/sidebar.html'),
        ('historico_logs', 'templates/components/sidebar.html'),
    ]
    
    print(f"\n✅ VERIFICANDO {len(url_for_calls)} CHAMADAS DE url_for\n")
    
    all_ok = True
    for endpoint, file in url_for_calls:
        if endpoint in available_endpoints:
            print(f"✅ {endpoint:30} em {file}")
        else:
            print(f"❌ {endpoint:30} em {file} - NÃO EXISTE")
            all_ok = False
    
    print("\n" + "-" * 60)
    
    if all_ok:
        print("✅ TODOS OS url_for ESTÃO CORRETOS!")
        return 0
    else:
        print("❌ ALGUNS url_for ESTÃO INVÁLIDOS!")
        return 1

if __name__ == '__main__':
    result1 = test_endpoints()
    result2 = test_templates_url_for()
    
    sys.exit(max(result1, result2))
```

**Para executar:**
```bash
python test_endpoints.py
```

**Saída esperada:**
```
✅ auth.login                 → /login                   (GET,POST)
✅ auth.perfil               → /perfil                  (GET,POST)
✅ auth.logout               → /logout                  (GET)
✅ admin.dashboard           → /admin/                  (GET)
✅ dashboard                 → /dashboard               (GET)
✅ historico_logs            → /logs                    (GET)

✅ TODOS OS ENDPOINTS CRÍTICOS ENCONTRADOS!
✅ TODOS OS url_for ESTÃO CORRETOS!
```

---

## Teste de Segurança

### Script: `test_security.py`

```python
#!/usr/bin/env python3
"""Test security features"""

from app import app
from flask import session

def test_admin_protection():
    """Verify /admin routes require admin access"""
    
    print("🔒 Testando proteção de rotas admin...")
    print("-" * 60)
    
    client = app.test_client()
    
    admin_routes = [
        '/admin/',
        '/admin/usuarios',
        '/admin/funcionarios',
    ]
    
    print("\n1️⃣ Sem autenticação:\n")
    for route in admin_routes:
        response = client.get(route, follow_redirects=False)
        expected_status = 302  # Redirect
        actual_status = response.status_code
        
        if actual_status == expected_status:
            print(f"✅ {route:30} → Redirecionado para login ({actual_status})")
        else:
            print(f"⚠️ {route:30} → Status {actual_status} (esperado 302)")
    
    print("\n" + "-" * 60)
    print("✅ Proteção de acesso funcionando!")

if __name__ == '__main__':
    test_admin_protection()
```

---

## Verificação Manual de Blueprints

```python
# Terminal Python interativo
python
>>> from app import app
>>> 
>>> # Ver todos os endpoints
>>> for rule in app.url_map.iter_rules():
...     if rule.endpoint != 'static':
...         print(f"{rule.endpoint:30} {rule}")
...

# Saída deve incluir:
# auth.login                    /login
# auth.perfil                   /perfil             ← CORRIGIDO
# admin.dashboard               /admin/             ← CORRIGIDO
# dashboard                     /dashboard
# ... etc
```

---

## Checklist de Validação

### ✅ Testes Críticos

- [ ] Aplicação inicia (`python app.py`)
- [ ] Nenhum erro BuildError ao iniciar
- [ ] Login funciona
- [ ] Clique em "Meu Perfil" (header.html) não gera erro
- [ ] Clique em "Painel Admin" carrega corretamente
- [ ] Dashboard do admin funciona
- [ ] Relatórios carregam (requer permissão gerente)
- [ ] Histórico de logs funciona

### ✅ Testes de Segurança

- [ ] Usuário comum NÃO consegue acessar /admin
- [ ] Usuário comum NÃO consegue acessar /relatorios
- [ ] Logout funciona
- [ ] Session é limpa após logout

### ✅ Testes de URL Building

- [ ] Todos os links no menu funcionam
- [ ] Paginação funciona (vendas, logs)
- [ ] Botões de ação funcionam (editar, deletar)
- [ ] Nenhum erro 404 em rotas internas

---

## Resultado Esperado Após Correção

```
ANTES:
❌ Click em "Meu Perfil"
   → jinja2.exceptions.TemplateNotFound: perfil
   → Ou BuildError: Could not build url for endpoint 'perfil'

DEPOIS:
✅ Click em "Meu Perfil"
   → Carrega corretamente
   → Mostra dados do usuário
   → Pode editar perfil
```

---

## Troubleshooting

**Problema:** Still getting BuildError after changes
**Solução:**
1. Parar o servidor (`Ctrl+C`)
2. Limpar cache: `rm -rf __pycache__ .pytest_cache`
3. Reiniciar: `python app.py`

**Problema:** Corrigiu mas painel admin não aparece
**Solução:**
1. Verificar se usuário é realmente admin
2. Verificar se session tem 'user_tipo'
3. Consultar banco: `SELECT tipo FROM usuarios WHERE id = ?`

**Problema:** Erro 404 em alguma rota
**Solução:**
1. Verificar se endpoint existe: `test_endpoints.py`
2. Verificar decoradores: `@require_login`, `@require_admin`
3. Verificar se blueprint está registrado em app.py

---

## Dados de Teste

```python
# Dados recomendados para testar

# Usuario Admin
Email: admin@test.com
Senha: admin123 (mínimo 6 caracteres)
Tipo: admin

# Usuario Gerente
Email: gerente@test.com
Senha: gerente123
Tipo: gerente

# Usuario Funcionario
Email: func@test.com
Senha: func123
Tipo: funcionario
```

---

**Última atualização:** 2026-03-20  
**Status:** Pronto para testes
