-- V5__create_covering_indexes.sql
-- Covering indexes e Partial indexes para otimização avançada

-- Covering index para busca por email retornando dados do usuário
-- INCLUDE adiciona colunas extras ao índice sem fazer parte da chave
CREATE INDEX idx_users_email_covering
    ON users(email)
    INCLUDE (username, first_name, last_name, country, city, status);

-- Partial index: apenas usuários ativos (reduz tamanho do índice)
CREATE INDEX idx_users_active
    ON users(status, created_at)
    WHERE status = 'active';

-- Covering index para orders por user_id com detalhes
CREATE INDEX idx_orders_user_covering
    ON orders(user_id, order_date DESC)
    INCLUDE (order_number, status, total_amount);

-- Partial index: apenas pedidos pendentes ou em processamento
CREATE INDEX idx_orders_pending
    ON orders(status, order_date)
    WHERE status IN ('pending', 'processing');

-- Covering index para products por categoria
CREATE INDEX idx_products_category_covering
    ON products(category, price)
    INCLUDE (name, stock_quantity);

-- Covering index para order_items por order_id
CREATE INDEX idx_order_items_order_covering
    ON order_items(order_id)
    INCLUDE (product_id, quantity, unit_price);

-- Partial index para order_items com quantidade alta
CREATE INDEX idx_order_items_high_quantity
    ON order_items(order_id, quantity)
    WHERE quantity > 1;
