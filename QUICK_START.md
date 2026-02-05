# 🚀 GUIA RÁPIDO DE EXECUÇÃO

## ✅ O que já está pronto

Todos os componentes necessários foram criados:

### Backend (Spring Boot)
- ✅ UserController, OrderController, ProductController, OrderItemController
- ✅ UserService, OrderService, ProductService, OrderItemService
- ✅ UserRepository, OrderRepository, ProductRepository, OrderItemRepository
- ✅ Models: User, Order, Product, OrderItem
- ✅ Configurações (application.yml)

### Database
- ✅ Migrações Flyway (V1 a V5)
- ✅ Script de geração de dados (generate_seed_data.py)
- ✅ Índices simples, compostos e covering

### Infraestrutura
- ✅ Docker Compose (PostgreSQL + Backend)
- ✅ Dockerfile
- ✅ Testes k6

## 📋 PASSO A PASSO PARA EXECUTAR

### 1. Compilar o projeto

```powershell
.\mvnw.cmd clean package -DskipTests
```

### 2. Subir o ambiente Docker

```powershell
docker-compose up -d
```

Aguarde ~30 segundos para o backend inicializar.

### 3. Verificar se está rodando

```powershell
# Ver logs
docker-compose logs -f backend

# Testar API
curl http://localhost:8080/api/users/search?email=user1@example.com
```

Se retornar um usuário, está funcionando! ✅

### 4. Popular o banco com dados (OPCIONAL - se quiser 1M+ registros)

```powershell
# Instalar dependências
pip install psycopg2-binary faker

# Executar script (demora 30-60 minutos)
python database/scripts/generate_seed_data.py
```

**NOTA**: O Flyway já inseriu alguns dados de teste na migração V2. Você pode usar esses dados para testes rápidos.

### 5. Testar os endpoints

```powershell
# Buscar usuário por email
curl http://localhost:8080/api/users/by-email?email=user1@example.com

# Buscar por localização
curl "http://localhost:8080/api/users/by-location?country=Brazil&city=São Paulo"

# Buscar pedidos por usuário
curl http://localhost:8080/api/orders/user/1

# Buscar pedidos por status
curl http://localhost:8080/api/orders/status/pending

# Buscar produtos por categoria
curl http://localhost:8080/api/products/category/Electronics
```

### 6. Executar testes de performance com k6 (OPCIONAL)

```powershell
# Instalar k6 primeiro: https://k6.io/docs/getting-started/installation/

# Executar teste
k6 run k6/scripts/test-simple-index.js
```

## 🔍 Verificar índices no banco

```powershell
# Conectar ao PostgreSQL
docker exec -it benchmark-postgres psql -U postgres -d benchmark_db

# Listar índices
\di

# Ver plano de execução de uma query
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user1@example.com';

# Sair
\q
```

## 🛑 Parar o ambiente

```powershell
docker-compose down
```

## 🗑️ Limpar tudo (incluindo dados)

```powershell
docker-compose down -v
```

## 📊 Comparar performance SEM vs COM índices

### Teste SEM índices (V3, V4, V5)

```sql
-- Conectar ao banco
docker exec -it benchmark-postgres psql -U postgres -d benchmark_db

-- Remover índices
DROP INDEX IF EXISTS idx_users_email;
DROP INDEX IF EXISTS idx_users_status;
DROP INDEX IF EXISTS idx_users_country;
-- ... etc

-- Testar query
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user1@example.com';
-- Resultado: Seq Scan (lento)
```

### Teste COM índices

```sql
-- Recriar índice
CREATE INDEX idx_users_email ON users(email);

-- Testar query
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user1@example.com';
-- Resultado: Index Scan (rápido!)
```

## 📈 Métricas Esperadas

Com os dados de teste (poucos registros):
- Sem índices: ~1-10ms
- Com índices: ~1-5ms

Com 1M+ registros (após rodar o script Python):
- Sem índices: 2-5 segundos ⚠️
- Com índices simples: 200-500ms ✅
- Com índices compostos: 50-200ms ✅✅
- Com covering indexes: 10-50ms 🚀

## 🎯 Próximos Passos

1. ✅ **Compilar e executar** o projeto
2. ✅ **Testar os endpoints** manualmente
3. 📊 **Gerar 1M+ registros** (opcional, demora ~1 hora)
4. 📈 **Executar testes k6** para comparar performance
5. 🔍 **Analisar EXPLAIN ANALYZE** das queries

## 🆘 Problemas Comuns

### Backend não inicia
```powershell
# Ver logs
docker-compose logs backend

# Reiniciar
docker-compose restart backend
```

### Erro de conexão com PostgreSQL
```powershell
# Verificar se está rodando
docker ps

# Ver logs
docker-compose logs postgres
```

### Porta 8080 já em uso
Altere a porta no `docker-compose.yml`:
```yaml
ports:
  - "8081:8080"  # Usar porta 8081 ao invés de 8080
```

## ✅ Checklist Final

- [ ] Projeto compilado (`mvnw.cmd clean package`)
- [ ] Docker Compose rodando (`docker-compose up -d`)
- [ ] Backend acessível (http://localhost:8080)
- [ ] Endpoints testados com sucesso
- [ ] (Opcional) Dados gerados (1M+ registros)
- [ ] (Opcional) Testes k6 executados

**Pronto! Seu sistema de benchmark de índices está funcionando! 🎉**
