CREATE TABLE users
(
    id         BIGSERIAL PRIMARY KEY,
    email      VARCHAR(255) NOT NULL,
    username   VARCHAR(100) NOT NULL,
    first_name VARCHAR(100),
    last_name  VARCHAR(100),
    created_at TIMESTAMP    NOT NULL DEFAULT NOW(),
    country    VARCHAR(50),
    city       VARCHAR(100),
    status     VARCHAR(20)
);

CREATE TABLE products
(
    id          BIGSERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    description TEXT,
    price       DECIMAL(10, 2),
    category    VARCHAR(100),
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE TABLE orders
(
    id           BIGSERIAL PRIMARY KEY,
    user_id      BIGINT    NOT NULL,
    order_date   TIMESTAMP NOT NULL DEFAULT NOW(),
    status       VARCHAR(20),
    total_amount DECIMAL(10, 2),
    created_at   TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE order_items
(
    id         BIGSERIAL PRIMARY KEY,
    order_id   BIGINT    NOT NULL,
    product_id BIGINT    NOT NULL,
    quantity   INT       NOT NULL,
    price      DECIMAL(10, 2),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);