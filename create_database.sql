-- ====================================
-- CRIAR BANCO DE DADOS NO POSTGRESQL
-- ====================================

-- 1. Conecte-se ao PostgreSQL como superusuário
-- psql -U postgres

-- 2. Crie o banco de dados
CREATE DATABASE benchmark_db;

-- 3. Verifique se foi criado
\l

-- 4. Conecte ao banco recém-criado
\c benchmark_db

-- 5. Pronto! O Flyway irá criar as tabelas automaticamente quando o backend iniciar

-- ====================================
-- COMANDOS ÚTEIS
-- ====================================

-- Ver tabelas criadas
\dt

-- Ver dados nas tabelas
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM orders;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM order_items;

-- Ver alguns registros
SELECT * FROM users LIMIT 5;
SELECT * FROM products LIMIT 5;

-- Ver índices criados
\di

-- Analisar uma query
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user1@example.com';

-- Sair do psql
\q
