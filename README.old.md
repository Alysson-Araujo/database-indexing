# Database Indexing Benchmark

A comprehensive benchmark project to demonstrate and measure the performance impact of different database indexing strategies using Spring Boot, PostgreSQL, and k6 load testing.

## 📋 Overview

This project provides a practical demonstration of how different types of database indexes affect query performance:

- **No Index**: Baseline performance with no indexes
- **Simple Index**: Single-column indexes on frequently queried fields
- **Composite Index**: Multi-column indexes for complex queries
- **Covering Index**: Indexes that include all columns needed by a query

## 🏗️ Architecture

```
database-indexing-benchmark/
├── backend/              # Spring Boot application
├── k6/                   # Load testing scripts
├── database/             # Database migrations and seed data
├── docker-compose.yml    # Docker setup
└── README.md
```

## 🛠️ Tech Stack

- **Backend**: Spring Boot 4.0.2, Java 17
- **Database**: PostgreSQL 16
- **ORM**: Spring Data JPA, Hibernate
- **Migration**: Flyway
- **Load Testing**: k6
- **Data Generation**: Python (Faker library)
- **Containerization**: Docker & Docker Compose

## 📦 Prerequisites

- Java 17 or higher
- Maven 3.6+
- Docker & Docker Compose
- k6 (for load testing)
- Python 3.8+ (for data generation)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd "Database Indexing"
```

### 2. Generate Seed Data

First, install Python dependencies:

```bash
pip install faker
```

Generate the seed data SQL file:

```bash
python database/scripts/generate_seed_data.py > database/migrations/V2__seed_data.sql
```

### 3. Start PostgreSQL with Docker

```bash
docker-compose up -d postgres
```

### 4. Run the Application

```bash
./mvnw spring-boot:run
```

Or build and run:

```bash
./mvnw clean package
java -jar target/DatabaseIndexing-0.0.1-SNAPSHOT.jar
```

## 📊 Running Benchmarks

### Install k6

**Windows (using Chocolatey):**
```bash
choco install k6
```

**macOS:**
```bash
brew install k6
```

**Linux:**
```bash
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

### Run Load Tests

```bash
# Test without indexes (baseline)
k6 run k6/scripts/test-no-index.js

# Test with simple indexes
k6 run k6/scripts/test-simple-index.js

# Test with composite indexes
k6 run k6/scripts/test-composite-index.js

# Test with covering indexes
k6 run k6/scripts/test-covering-index.js
```

## 🗄️ Database Migration Strategy

The project uses Flyway for database migrations in a specific order:

1. **V1__create_tables.sql**: Creates the base table structure
2. **V2__seed_data.sql**: Populates tables with test data
3. **V3__create_simple_indexes.sql**: Adds single-column indexes
4. **V4__create_composite_indexes.sql**: Adds multi-column indexes
5. **V5__create_covering_indexes.sql**: Adds covering indexes

You can selectively run migrations by enabling/disabling them in the `database/migrations` folder.

## 📈 Performance Metrics

The benchmarks measure:

- **Response Time**: Average, median, p95, p99
- **Throughput**: Requests per second
- **Error Rate**: Percentage of failed requests
- **Database Query Time**: Execution time for different index strategies

## 🔧 Configuration

### Application Configuration

Edit `src/main/resources/application.yml` to configure:

- Database connection
- JPA/Hibernate settings
- Server port
- Actuator endpoints

### Load Test Configuration

Edit k6 scripts in `k6/scripts/` to adjust:

- Virtual users (VUs)
- Test duration
- Ramp-up/down stages
- Performance thresholds

## 📝 API Endpoints

### Users
- `GET /api/users/search?email={email}` - Search user by email
- `GET /api/users/{id}` - Get user by ID

### Orders
- `GET /api/orders/user/{userId}` - Get orders by user
- `GET /api/orders/status/{status}` - Get orders by status
- `GET /api/orders/user/{userId}/status/{status}` - Get orders by user and status
- `GET /api/orders/user/{userId}/date-range?start={start}&end={end}` - Get orders by user and date range
- `GET /api/orders/user/{userId}/details` - Get order details with covering index

### Products
- `GET /api/products/category/{category}` - Get products by category
- `GET /api/products/category/{category}/price-range?min={min}&max={max}` - Get products by category and price
- `GET /api/products/category/{category}/details` - Get product details with covering index

### Order Items
- `GET /api/order-items/order/{orderId}` - Get items by order
- `GET /api/order-items/order/{orderId}/details` - Get order item details with covering index

## 🧪 Testing Scenarios

1. **Baseline Test (No Indexes)**
   - Run migrations V1 and V2 only
   - Execute `test-no-index.js`

2. **Simple Index Test**
   - Run migrations V1, V2, and V3
   - Execute `test-simple-index.js`

3. **Composite Index Test**
   - Run migrations V1, V2, V3, and V4
   - Execute `test-composite-index.js`

4. **Covering Index Test**
   - Run all migrations (V1-V5)
   - Execute `test-covering-index.js`

## 📊 Expected Results

Performance should improve progressively:

```
No Index < Simple Index < Composite Index < Covering Index
(slowest)                                    (fastest)
```

## 🐛 Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running: `docker-compose ps`
- Check connection settings in `application.yml`

### Migration Errors
- Clear the database: `docker-compose down -v`
- Rebuild: `docker-compose up -d postgres`

### k6 Test Failures
- Ensure the backend is running
- Check the BASE_URL in k6 scripts
- Verify database has seed data

## 📚 Resources

- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [PostgreSQL Index Documentation](https://www.postgresql.org/docs/current/indexes.html)
- [k6 Documentation](https://k6.io/docs/)
- [Flyway Documentation](https://flywaydb.org/documentation/)

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Created as a demonstration of database indexing strategies and performance benchmarking.
