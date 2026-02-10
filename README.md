# 🗄️ Database Indexing Benchmark

Benchmark profissional para comparar o impacto de diferentes estratégias de indexação no PostgreSQL.

## 📊 Resultados do Benchmark

| Posição | Estratégia | P95 | vs Sem Índices |
|---------|------------|-----|----------------|
| 🥇 | **Covering Indexes** | **3.44 ms** | **9.7% mais rápido** |
| 🥈 | **Índices Compostos** | **3.60 ms** | **5.3% mais rápido** |
| 🥉 | **Sem Índices** | **3.80 ms** | Baseline |
| 4º | **Índices Simples** | **11.00 ms** | 189% mais lento ⚠️ |

**📈 Ver relatório completo:** [docs/RELATORIO_BENCHMARK.html](docs/RELATORIO_BENCHMARK.html)

---

## 🚀 Quick Start

### Pré-requisitos

- Java 21+
- PostgreSQL 15+
- Maven 3.9+
- K6 (para testes de carga)
- Python 3.10+ (para análise)

### 1. Configurar Banco de Dados

```bash
# Criar banco
psql -U postgres -c "CREATE DATABASE benchmark_db;"

# Aplicar migrations (ou deixe o Flyway fazer automaticamente)
```

### 2. Executar Aplicação

```powershell
# Sem Docker
.\start-local.ps1

# Com Docker
docker-compose up -d
```

### 3. Executar Testes K6

```powershell
# Teste sem índices
k6 run --out json=results/no-index.json k6/scripts/test-no-index.js

# Teste com índices simples
k6 run --out json=results/simple-index.json k6/scripts/test-simple-index.js

# Teste com índices compostos
k6 run --out json=results/composite-index.json k6/scripts/test-composite-index.js

# Teste com covering indexes
k6 run --out json=results/covering-index.json k6/scripts/test-covering-index.js
```

### 4. Analisar Resultados

```powershell
# Análise comparativa
python scripts/compare_all_tests.py

# Gerar relatório HTML
python scripts/generate_html_report.py

# Abrir relatório
start docs/RELATORIO_BENCHMARK.html
```

---

## 📁 Estrutura do Projeto

```
Database Indexing/
├── src/                          # Código fonte Spring Boot
│   └── main/
│       ├── java/                 # Controllers, Services, Repositories
│       └── resources/
│           ├── application.yml   # Configuração
│           └── db/migration/     # Flyway migrations
├── k6/
│   └── scripts/                  # Scripts de teste K6
│       ├── test-no-index.js
│       ├── test-simple-index.js
│       ├── test-composite-index.js
│       └── test-covering-index.js
├── database/
│   ├── migrations/               # Migrations SQL
│   └── scripts/                  # Scripts de seed
├── scripts/                      # Scripts de análise Python
│   ├── analyze_results.py
│   ├── compare_all_tests.py
│   └── generate_html_report.py
├── results/                      # Dados brutos dos testes K6
├── docs/                         # Documentação e relatórios
│   ├── RELATORIO_BENCHMARK.html  # Relatório visual interativo
│   ├── RESULTADO_FINAL_ATUALIZADO.md
│   ├── RESUMO_EXECUTIVO.md
│   └── PROXIMOS_PASSOS.md
├── start-local.ps1               # Script de execução local
├── docker-compose.yml            # Docker Compose
├── pom.xml                       # Maven config
└── README.md                     # Este arquivo
```

---

## 🧪 Cenários de Teste

### 1. Sem Índices
- Queries básicas sem otimização
- Baseline para comparação

### 2. Índices Simples
- `idx_users_email` - Índice no email
- `idx_orders_user_id` - Índice no user_id
- `idx_orders_status` - Índice no status
- `idx_products_category` - Índice na categoria

### 3. Índices Compostos
- `idx_orders_user_status` - Composto (user_id, status)
- `idx_orders_user_date` - Composto (user_id, order_date)
- `idx_products_category_price` - Composto (category, price)

### 4. Covering Indexes
- Índices que incluem todas as colunas necessárias
- Evitam acesso à tabela (index-only scan)

---

## 📊 Métricas Coletadas

- **Latência:** P50, P90, P95, P99, Máxima
- **Throughput:** Requisições/segundo
- **Taxa de Sucesso:** HTTP 200/404/500
- **Iterações:** Total de testes executados

---

## 🛠️ Tecnologias

- **Backend:** Spring Boot 4.0, Java 21
- **Banco:** PostgreSQL 15
- **Migrations:** Flyway
- **Load Testing:** K6 (Grafana)
- **Análise:** Python 3 (json, statistics)
- **Containers:** Docker, Docker Compose

---

## 📚 Documentação Adicional

- [docs/RELATORIO_BENCHMARK.html](docs/RELATORIO_BENCHMARK.html) - Relatório visual interativo 🌟
- [docs/RESULTADO_FINAL_ATUALIZADO.md](docs/RESULTADO_FINAL_ATUALIZADO.md) - Análise técnica completa
- [docs/RESUMO_EXECUTIVO.md](docs/RESUMO_EXECUTIVO.md) - Resumo para stakeholders
- [docs/PROXIMOS_PASSOS.md](docs/PROXIMOS_PASSOS.md) - Guia de investigação

---

## 📈 Principais Descobertas

1. ✅ **Covering Indexes** oferecem a melhor performance (3.44 ms P95)
2. ✅ **Índices Compostos** são ótimo custo-benefício (3.60 ms P95)
3. ⚠️ **Índices Simples** podem PIORAR performance se mal projetados
4. 💡 Sempre validar índices com `EXPLAIN ANALYZE`

---

## 📝 Licença

MIT License

---

**Criado em:** 2026-02-09  
**Status:** ✅ Completo e Validado
