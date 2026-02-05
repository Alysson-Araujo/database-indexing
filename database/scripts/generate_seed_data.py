import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# Conectar ao banco de dados PostgreSQL
conn = psycopg2.connect(
    dbname="benchmark_db",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

print("Starting data generation...")

# 1. Inserir 1M users
print("\n=== Inserting 1,000,000 users ===")
users_batch = []
batch_size = 5000

for i in range(1_000_000):
    users_batch.append((
        fake.email(),
        fake.user_name() + str(i),  # Garantir unicidade
        fake.first_name(),
        fake.last_name(),
        fake.country(),
        fake.city(),
        random.choice(['active', 'inactive', 'suspended'])
    ))

    if len(users_batch) >= batch_size:
        cur.executemany("""
            INSERT INTO users (email, username, first_name, last_name, country, city, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, users_batch)
        conn.commit()
        users_batch = []
        print(f"Inserted {i+1:,} users")

# Inserir registros restantes
if users_batch:
    cur.executemany("""
        INSERT INTO users (email, username, first_name, last_name, country, city, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, users_batch)
    conn.commit()

print("✓ Users insertion completed!")

# 2. Inserir produtos (100k produtos)
print("\n=== Inserting 100,000 products ===")
categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Home', 'Sports', 'Toys', 'Beauty']
products_batch = []

for i in range(100_000):
    products_batch.append((
        fake.catch_phrase(),
        random.choice(categories),
        round(random.uniform(10.0, 1000.0), 2),
        random.randint(0, 1000)
    ))

    if len(products_batch) >= batch_size:
        cur.executemany("""
            INSERT INTO products (name, category, price, stock_quantity)
            VALUES (%s, %s, %s, %s)
        """, products_batch)
        conn.commit()
        products_batch = []
        print(f"Inserted {i+1:,} products")

if products_batch:
    cur.executemany("""
        INSERT INTO products (name, category, price, stock_quantity)
        VALUES (%s, %s, %s, %s)
    """, products_batch)
    conn.commit()

print("✓ Products insertion completed!")

# 3. Inserir 5M orders
print("\n=== Inserting 5,000,000 orders ===")
orders_batch = []
statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']

for i in range(5_000_000):
    order_date = fake.date_time_between(start_date='-2y', end_date='now')
    orders_batch.append((
        random.randint(1, 1_000_000),  # user_id
        f"ORD-{i+1:010d}",  # order_number
        order_date,
        random.choice(statuses),
        round(random.uniform(10.0, 5000.0), 2)
    ))

    if len(orders_batch) >= batch_size:
        cur.executemany("""
            INSERT INTO orders (user_id, order_number, order_date, status, total_amount)
            VALUES (%s, %s, %s, %s, %s)
        """, orders_batch)
        conn.commit()
        orders_batch = []
        if (i + 1) % 100000 == 0:
            print(f"Inserted {i+1:,} orders")

if orders_batch:
    cur.executemany("""
        INSERT INTO orders (user_id, order_number, order_date, status, total_amount)
        VALUES (%s, %s, %s, %s, %s)
    """, orders_batch)
    conn.commit()

print("✓ Orders insertion completed!")

# 4. Inserir order_items (10M - média de 2 itens por pedido)
print("\n=== Inserting 10,000,000 order items ===")
order_items_batch = []

for i in range(10_000_000):
    order_items_batch.append((
        random.randint(1, 5_000_000),  # order_id
        random.randint(1, 100_000),    # product_id
        random.randint(1, 5),           # quantity
        round(random.uniform(10.0, 1000.0), 2)  # unit_price
    ))

    if len(order_items_batch) >= batch_size:
        cur.executemany("""
            INSERT INTO order_items (order_id, product_id, quantity, unit_price)
            VALUES (%s, %s, %s, %s)
        """, order_items_batch)
        conn.commit()
        order_items_batch = []
        if (i + 1) % 500000 == 0:
            print(f"Inserted {i+1:,} order items")

if order_items_batch:
    cur.executemany("""
        INSERT INTO order_items (order_id, product_id, quantity, unit_price)
        VALUES (%s, %s, %s, %s)
    """, order_items_batch)
    conn.commit()

print("✓ Order items insertion completed!")

# Fechar conexão
cur.close()
conn.close()

print("\n" + "="*50)
print("DATA GENERATION COMPLETED!")
print("="*50)
print(f"Users:       1,000,000")
print(f"Products:      100,000")
print(f"Orders:      5,000,000")
print(f"Order Items: 10,000,000")
print("="*50)

