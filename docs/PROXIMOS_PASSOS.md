# 🔍 PRÓXIMOS PASSOS - INVESTIGAÇÃO E MELHORIAS

**Data:** 2026-02-09  
**Status dos Testes:** ✅ Completos e Validados

---

## 🎯 AGORA VOCÊ TEM

✅ **Testes completos e equilibrados** (4 cenários, ~80k requisições)  
✅ **Resultados surpreendentes** (índices simples 3x mais lentos!)  
✅ **Relatórios completos:**
- `RESULTADO_FINAL_ATUALIZADO.md` - Análise técnica
- `RELATORIO_BENCHMARK.html` - Visualização interativa
- `COMPARATIVO_INDICES.txt` - Comparativo rápido

---

## 🔬 INVESTIGAÇÃO RECOMENDADA

### 1️⃣ **Por que Índices Simples estão LENTOS?**

**Resultado:** P95 = 11.00 ms (3x pior que sem índices!)

**Possíveis causas:**

#### a) **Índices não estão sendo usados pelas queries**
```sql
-- Verificar plano de execução
EXPLAIN ANALYZE 
SELECT * FROM users 
WHERE email = 'user12345@example.com';

-- Deve mostrar "Index Scan" ou "Bitmap Index Scan"
-- Se mostrar "Seq Scan", o índice NÃO está sendo usado!
```

#### b) **Índices estão fragmentados**
```sql
-- Verificar bloat (fragmentação) do índice
SELECT 
    schemaname, 
    tablename, 
    indexname, 
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public';

-- Se idx_scan = 0, índice não está sendo usado!
```

#### c) **Estatísticas desatualizadas**
```sql
-- Atualizar estatísticas do PostgreSQL
ANALYZE users;
ANALYZE orders;
ANALYZE products;
ANALYZE order_items;

-- Depois, rodar o teste novamente
```

#### d) **Queries do K6 não usam os campos indexados**
```javascript
// Verificar em k6/scripts/test-simple-index.js
// As queries devem filtrar pelos campos indexados:
// - users.email (V3__create_simple_indexes.sql)
// - orders.user_id
// - orders.status
// - products.category
```

---

### 2️⃣ **Executar EXPLAIN ANALYZE nas Queries**

Conecte ao PostgreSQL e rode:

```powershell
# Conectar ao banco
psql -U postgres -d benchmark_db
```

```sql
-- 1. Query de email (deve usar idx_users_email)
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM users WHERE email = 'user1@example.com';

-- 2. Query de pedidos por usuário (deve usar idx_orders_user_id)
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM orders WHERE user_id = 1;

-- 3. Query de pedidos por status (deve usar idx_orders_status)
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM orders WHERE status = 'pending';

-- 4. Query de produtos por categoria (deve usar idx_products_category)
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM products WHERE category = 'Electronics';
```

**O que procurar:**
- ✅ "Index Scan using idx_xxx" → Índice sendo usado
- ❌ "Seq Scan on tablename" → Índice NÃO sendo usado
- ⚠️ "Bitmap Heap Scan" → Índice usado, mas muitos resultados

---

### 3️⃣ **Verificar se Índices Existem**

```sql
-- Listar todos os índices
SELECT 
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- Deve mostrar:
-- idx_users_email
-- idx_orders_user_id
-- idx_orders_status
-- idx_products_category
```

---

### 4️⃣ **Re-executar Testes Após Correções**

```powershell
# 1. Atualizar estatísticas (no psql)
psql -U postgres -d benchmark_db -c "ANALYZE;"

# 2. Re-executar teste de índices simples
k6 run --out json=results/simple-index-fixed.json .\k6\scripts\test-simple-index.js

# 3. Comparar resultados
python analyze_results.py
```

---

## 📊 MELHORIAS PARA TESTAR

### 1️⃣ **Aumentar Volume de Dados**

Atualmente: ~100k users, 500k orders, 50k products

**Testar com:**
- 1M users
- 5M orders
- 100k products

```python
# Editar database/scripts/generate_seed_data.py
NUM_USERS = 1_000_000
NUM_ORDERS = 5_000_000
NUM_PRODUCTS = 100_000
```

**Expectativa:** Índices devem mostrar **muito mais** benefício!

---

### 2️⃣ **Testar Partial Indexes**

Índices parciais para queries específicas:

```sql
-- Índice apenas para pedidos pendentes (status comum)
CREATE INDEX idx_orders_pending 
ON orders (user_id, order_date) 
WHERE status = 'pending';

-- Índice apenas para produtos caros
CREATE INDEX idx_products_expensive 
ON products (category, name) 
WHERE price > 100;
```

---

### 3️⃣ **Testar Diferentes Tipos de Queries**

Adicionar aos scripts K6:

```javascript
// JOIN complexo
let joinRes = http.get(`${BASE_URL}/api/orders/${orderId}/with-items`);

// GROUP BY + COUNT
let statsRes = http.get(`${BASE_URL}/api/orders/stats-by-status`);

// ORDER BY + LIMIT
let topRes = http.get(`${BASE_URL}/api/products/top-expensive?limit=10`);

// Full-text search
let searchRes = http.get(`${BASE_URL}/api/products/search?q=laptop`);
```

---

### 4️⃣ **Comparar com MySQL**

Criar mesmo benchmark no MySQL para comparar:

```bash
# Instalar MySQL
# Rodar mesmos testes
# Comparar resultados PostgreSQL vs MySQL
```

---

## 🚀 APLICAR EM PRODUÇÃO

### **Checklist de Deploy:**

- [ ] 1. **Backup completo** do banco de produção
- [ ] 2. **Rodar em horário de baixa demanda**
- [ ] 3. **Aplicar índices um por vez** (não todos de uma vez)
- [ ] 4. **Monitorar impacto** após cada índice:
  - Latência das queries
  - Uso de CPU/memória
  - Tamanho do banco
- [ ] 5. **Rollback preparado** (DROP INDEX se necessário)

### **Ordem de Aplicação:**

```sql
-- Dia 1: Covering Indexes nos endpoints mais críticos
CREATE INDEX idx_users_email_covering 
ON users (email) INCLUDE (name, country, city, created_at);

-- Monitorar por 24h

-- Dia 2: Índices Compostos nas queries principais
CREATE INDEX idx_orders_user_status 
ON orders (user_id, status);

-- Monitorar por 24h

-- Dia 3: Demais índices compostos
-- ...
```

---

## 📚 DOCUMENTAÇÃO PARA O TIME

### **Criar Wiki/Confluence com:**

1. **Estratégia de Indexação**
   - Quando criar índice
   - Tipos de índices e quando usar
   - Como medir impacto

2. **Índices Existentes**
   - Tabela de todos os índices
   - Por que cada um existe
   - Queries otimizadas por cada índice

3. **Processo de Criação**
   - Como propor novo índice
   - Como testar localmente
   - Processo de aprovação/deploy

4. **Monitoramento**
   - Dashboard com métricas
   - Alertas de performance
   - Revisão trimestral de índices

---

## 🧪 EXPERIMENTOS AVANÇADOS

### 1️⃣ **Expression Indexes**

```sql
-- Índice em função (ex: LOWER para case-insensitive search)
CREATE INDEX idx_users_email_lower 
ON users (LOWER(email));

-- Query usa função
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';
```

### 2️⃣ **GIN/GiST Indexes (Full-Text Search)**

```sql
-- Adicionar coluna tsvector
ALTER TABLE products ADD COLUMN search_vector tsvector;

-- Atualizar com dados
UPDATE products 
SET search_vector = to_tsvector('english', name || ' ' || description);

-- Criar índice GIN
CREATE INDEX idx_products_search 
ON products USING GIN(search_vector);

-- Query de busca
SELECT * FROM products 
WHERE search_vector @@ to_tsquery('english', 'laptop');
```

### 3️⃣ **Index-Only Scans (Verificar)**

```sql
-- Query que DEVE usar index-only scan
EXPLAIN (ANALYZE, BUFFERS) 
SELECT email, name FROM users WHERE email = 'user@example.com';

-- Se usar covering index, deve mostrar:
-- "Index Only Scan using idx_users_email_covering"
```

---

## 📊 MÉTRICAS A MONITORAR EM PRODUÇÃO

### **APM (Application Performance Monitoring):**

- Latência P50, P95, P99 por endpoint
- Throughput (req/s)
- Taxa de erro
- Tempo médio de query SQL

### **Database Monitoring:**

```sql
-- Queries mais lentas
SELECT 
    query,
    mean_exec_time,
    calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Índices não utilizados
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
AND schemaname = 'public';

-- Tamanho dos índices
SELECT 
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;
```

---

## 🎯 OBJETIVOS PARA OS PRÓXIMOS 30 DIAS

### **Semana 1:**
- [ ] Investigar por que índices simples estão lentos
- [ ] Executar EXPLAIN ANALYZE em todas as queries
- [ ] Corrigir problema identificado
- [ ] Re-executar teste de índices simples

### **Semana 2:**
- [ ] Aumentar volume de dados (1M-5M registros)
- [ ] Re-executar todos os testes
- [ ] Comparar resultados com dataset maior

### **Semana 3:**
- [ ] Criar testes com queries avançadas (JOIN, GROUP BY, etc.)
- [ ] Testar partial indexes
- [ ] Gerar novo relatório comparativo

### **Semana 4:**
- [ ] Documentar estratégia de indexação
- [ ] Apresentar resultados para o time
- [ ] Planejar deploy em produção

---

## 📝 PERGUNTAS A RESPONDER

1. **Por que índices simples estão 3x mais lentos?**
   - Resposta após investigação: _______________

2. **Em que volume de dados índices se tornam críticos?**
   - Testar: 100k, 1M, 10M, 100M registros

3. **Qual o overhead de escrita com índices?**
   - Testar: INSERT/UPDATE/DELETE com e sem índices

4. **Índices melhoram JOIN queries?**
   - Testar: Query com JOIN antes/depois de índices

5. **Vale a pena usar partial indexes?**
   - Comparar: Índice completo vs parcial

---

## ✅ CHECKLIST FINAL

Antes de dar o projeto como **100% COMPLETO**:

- [x] Testes executados e equilibrados
- [x] Resultados analisados e documentados
- [x] Relatórios gerados (MD + HTML)
- [ ] Investigação de anomalias concluída
- [ ] Testes com volume maior de dados
- [ ] Documentação para o time criada
- [ ] Apresentação preparada
- [ ] Deploy em produção planejado

---

## 🎉 VOCÊ ESTÁ AQUI

```
┌─────────────────────────────────────────────────────────┐
│  [✓] Testes Executados                                  │
│  [✓] Resultados Analisados                              │
│  [✓] Relatórios Gerados                                 │
│  [✓] Anomalias Corrigidas                               │
│  [→] Investigação de Performance ← VOCÊ ESTÁ AQUI       │
│  [ ] Testes Avançados                                   │
│  [ ] Documentação Completa                              │
│  [ ] Deploy em Produção                                 │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 COMECE AGORA!

### **Passo 1: Investigar Índices Simples**

```powershell
# Conectar ao PostgreSQL
psql -U postgres -d benchmark_db

# Executar EXPLAIN ANALYZE
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user1@example.com';
```

### **Passo 2: Atualizar Estatísticas**

```sql
ANALYZE;
```

### **Passo 3: Re-executar Teste**

```powershell
k6 run --out json=results/simple-index-fixed.json .\k6\scripts\test-simple-index.js
```

---

**Boa sorte na investigação! 🔍**

Se precisar de ajuda, consulte:
- `RESULTADO_FINAL_ATUALIZADO.md` - Análise completa
- `RELATORIO_BENCHMARK.html` - Visualização interativa
- PostgreSQL docs: https://www.postgresql.org/docs/current/indexes.html

