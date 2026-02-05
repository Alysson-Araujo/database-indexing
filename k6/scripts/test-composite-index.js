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
    http_req_duration: ['p(95)<250'],
    errors: ['rate<0.1'],
  },
};

const BASE_URL = 'http://localhost:8080';

export default function () {
  // Test 1: Get orders by user and date range (composite index: user_id, order_date)
  let userId = Math.floor(Math.random() * 100000) + 1;
  let startDate = '2024-01-01';
  let endDate = '2024-12-31';
  let userDateRes = http.get(`${BASE_URL}/api/orders/user/${userId}/date-range?start=${startDate}&end=${endDate}`);
  check(userDateRes, {
    'status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);

  sleep(0.5);

  // Test 2: Get orders by user and status (composite index: user_id, status)
  const statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled'];
  let status = statuses[Math.floor(Math.random() * statuses.length)];
  let userStatusRes = http.get(`${BASE_URL}/api/orders/user/${userId}/status/${status}`);
  check(userStatusRes, {
    'status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);

  sleep(0.5);

  // Test 3: Get products by category and price range (composite index: category, price)
  const categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Home', 'Sports', 'Toys', 'Beauty'];
  let category = categories[Math.floor(Math.random() * categories.length)];
  let minPrice = Math.floor(Math.random() * 100);
  let maxPrice = minPrice + 500;
  let categoryPriceRes = http.get(`${BASE_URL}/api/products/category/${category}/price-range?min=${minPrice}&max=${maxPrice}`);
  check(categoryPriceRes, {
    'status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);

  sleep(0.5);

  // Test 4: Get orders by status and date (composite index: status, order_date)
  let statusDateRes = http.get(`${BASE_URL}/api/orders/status/${status}/date-range?start=${startDate}&end=${endDate}`);
  check(statusDateRes, {
    'status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);

  sleep(1);
}

export function handleSummary(data) {
  return {
    'results/composite-index-summary.json': JSON.stringify(data),
  };
}
