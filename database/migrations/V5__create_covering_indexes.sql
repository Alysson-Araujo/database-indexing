-- V5__create_covering_indexes.sql

-- Index que cobre toda a query (evita ir na tabela)
CREATE INDEX idx_users_email_covering
    ON users(email)
    INCLUDE (username, first_name, last_name);

-- Partial index (apenas registros ativos)
CREATE INDEX idx_users_active
    ON users(status, created_at)
    WHERE status = 'active';