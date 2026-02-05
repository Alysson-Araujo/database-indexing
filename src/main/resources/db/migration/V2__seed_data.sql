-- V2__seed_data.sql
-- This migration is a placeholder
-- To seed the database with 1M+ records, run the Python script:
-- python database/scripts/generate_seed_data.py

-- For testing purposes, you can insert a few sample records here:

INSERT INTO users (email, username, first_name, last_name, country, city, status)
VALUES
    ('user1@example.com', 'user1', 'John', 'Doe', 'Brazil', 'São Paulo', 'active'),
    ('user2@example.com', 'user2', 'Jane', 'Smith', 'USA', 'New York', 'active'),
    ('user3@example.com', 'user3', 'Bob', 'Johnson', 'Brazil', 'Rio de Janeiro', 'inactive');

INSERT INTO products (name, category, price, stock_quantity)
VALUES
    ('Laptop Dell', 'Electronics', 3500.00, 50),
    ('T-Shirt Nike', 'Clothing', 89.90, 200),
    ('Organic Coffee', 'Food', 25.00, 1000),
    ('Python Book', 'Books', 59.90, 100);

INSERT INTO orders (user_id, order_number, order_date, status, total_amount)
VALUES
    (1, 'ORD-0000000001', NOW() - INTERVAL '10 days', 'delivered', 3500.00),
    (2, 'ORD-0000000002', NOW() - INTERVAL '5 days', 'processing', 179.80),
    (1, 'ORD-0000000003', NOW() - INTERVAL '2 days', 'pending', 84.90);

INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES
    (1, 1, 1, 3500.00),
    (2, 2, 2, 89.90),
    (3, 3, 3, 25.00),
    (3, 4, 1, 59.90);
