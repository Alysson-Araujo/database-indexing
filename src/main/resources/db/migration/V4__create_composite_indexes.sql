-- V4__create_composite_indexes.sql
-- Índices compostos para queries com múltiplas colunas

-- Para queries: WHERE country = ? AND city = ?
CREATE INDEX idx_users_country_city ON users(country, city);

-- Para queries: WHERE status = ? AND created_at >= ?
CREATE INDEX idx_users_status_created ON users(status, created_at);

-- Para queries: WHERE user_id = ? AND order_date >= ?
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);

-- Para queries: WHERE status = ? AND order_date >= ?
CREATE INDEX idx_orders_status_date ON orders(status, order_date);

-- Para queries: WHERE user_id = ? AND status = ?
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Para queries: WHERE category = ? AND price BETWEEN ? AND ?
CREATE INDEX idx_products_category_price ON products(category, price);

-- Para queries com order_id e product_id juntos
CREATE INDEX idx_order_items_order_product ON order_items(order_id, product_id);
