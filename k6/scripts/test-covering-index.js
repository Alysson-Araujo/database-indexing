import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration
export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m', target: 50 },
    { duration: '2m', target: 100 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'],
    errors: ['rate<0.1'],
  },
};

const BASE_URL = 'http://localhost:8080';

export default function () {
  // Test 1: Get user details by email (covering index includes all needed columns)
  let emailRes = http.get(`${BASE_URL}/api/users/search?email=user${Math.floor(Math.random() * 100000)}@example.com`);
  check(emailRes, {
    'status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);

  sleep(0.5);

  // Test 2: Get order details by user (covering index includes order details)
  let userId = Math.floor(Math.random() * 100000) + 1;
  let ordersRes = http.get(`${BASE_URL}/api/orders/user/${userId}/details`);
  check(ordersRes, {
    'status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);

  sleep(0.5);

  // Test 3: Get products by category with details (covering index)
  const categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Home', 'Sports', 'Toys', 'Beauty'];
  let category = categories[Math.floor(Math.random() * categories.length)];
  let productsRes = http.get(`${BASE_URL}/api/products/category/${category}/details`);
  check(productsRes, {
    'status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);

  sleep(0.5);

  // Test 4: Get order items with details (covering index)
  let orderId = Math.floor(Math.random() * 500000) + 1;
  let orderItemsRes = http.get(`${BASE_URL}/api/order-items/order/${orderId}/details`);
  check(orderItemsRes, {
    'status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);

  sleep(1);
}

export function handleSummary(data) {
  return {
    'results/covering-index-summary.json': JSON.stringify(data),
  };
}
