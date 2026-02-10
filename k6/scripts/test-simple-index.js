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
    { duration: '2m', target: 100 },   // Peak load
    { duration: '30s', target: 0 },    // Cool down
  ],
  thresholds: {
    http_req_duration: ['p(95)<300'],  // 95% das requests < 300ms
    errors: ['rate<0.1'],              // Taxa de erro < 10%
  },
};

const BASE_URL = 'http://localhost:8080';

export default function () {
  // Test 1: Get user by email (with simple index)
  let emailRes = http.get(`${BASE_URL}/api/users/by-email?email=user${Math.floor(Math.random() * 100000)}@example.com`);
  check(emailRes, {
    'status is 200 or 404': (r) => r.status === 200 || r.status === 404,
  }) || errorRate.add(1);

  sleep(0.5);

  // Test 2: Get orders by user (with simple index on user_id)
  let userId = Math.floor(Math.random() * 100000) + 1;
  let ordersRes = http.get(`${BASE_URL}/api/orders/user/${userId}`);
  check(ordersRes, {
    'status is 200 or 404': (r) => r.status === 200 || r.status === 404,
  }) || errorRate.add(1);

  sleep(0.5);

  // Test 3: Get orders by status (with simple index)
  const statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled'];
  let status = statuses[Math.floor(Math.random() * statuses.length)];
  let statusRes = http.get(`${BASE_URL}/api/orders/status/${status}`);
  check(statusRes, {
    'status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);

  sleep(0.5);

  // Test 4: Get products by category (with simple index)
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
    'results/simple-index-summary.json': JSON.stringify(data),
  };
}
