-- V4__create_composite_indexes.sql

-- Para query: WHERE country = ? AND city = ?
CREATE INDEX idx_users_country_city ON users(country, city);

-- Para query: WHERE status = ? AND created_at >= ?
CREATE INDEX idx_users_status_created ON users(status, created_at);

-- Para joins
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);