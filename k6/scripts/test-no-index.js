// k6/scripts/test-no-index.js
// Teste SEM índices - para comparar performance base
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration - IGUAL aos outros testes para comparação justa
export const options = {
  stages: [
    { duration: '30s', target: 10 },   // Warm up
    { duration: '1m', target: 50 },    // Normal load
    { duration: '2m', target: 100 },   // Peak load (2 minutos como os outros)
    { duration: '30s', target: 0 },    // Cool down
  ],
  thresholds: {
    http_req_duration: ['p(95)<5000'], // 95% das requests < 5s (mais tolerante sem índices)
    errors: ['rate<0.1'],              // Taxa de erro < 10%
  },
};

const BASE_URL = 'http://localhost:8080';

export default function () {
  // Test 1: Get user by email (SEM índice no email)
  let emailRes = http.get(`${BASE_URL}/api/users/by-email?email=user${Math.floor(Math.random() * 100000)}@example.com`);
  check(emailRes, {
    'status is 200 or 404': (r) => r.status === 200 || r.status === 404,
  }) || errorRate.add(1);

  sleep(0.5);

  // Test 2: Get orders by user (SEM índice no user_id)
  let userId = Math.floor(Math.random() * 100000) + 1;
  let ordersRes = http.get(`${BASE_URL}/api/orders/user/${userId}`);
  check(ordersRes, {
    'status is 200 or 404': (r) => r.status === 200 || r.status === 404,
  }) || errorRate.add(1);

  sleep(0.5);

  // Test 3: Get orders by status (SEM índice no status)
  const statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled'];
  let status = statuses[Math.floor(Math.random() * statuses.length)];
  let statusRes = http.get(`${BASE_URL}/api/orders/status/${status}`);
  check(statusRes, {
    'status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);

  sleep(0.5);

  // Test 4: Get products by category (SEM índice na category)
  const categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Home', 'Sports', 'Toys', 'Beauty'];
  let category = categories[Math.floor(Math.random() * categories.length)];
  let productsRes = http.get(`${BASE_URL}/api/products/category/${category}`);
  check(productsRes, {
    'status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);

  sleep(1);
}

export function handleSummary(data) {
  return {
    'results/no-index-summary.json': JSON.stringify(data),
  };
}
