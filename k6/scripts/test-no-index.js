// k6/scripts/test-no-index.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const queryTime = new Trend('query_time');

export const options = {
  stages: [
    { duration: '30s', target: 10 },  // Warm up
    { duration: '1m', target: 50 },   // Normal load
    { duration: '30s', target: 100 }, // Peak load
    { duration: '30s', target: 0 },   // Cool down
  ],
  thresholds: {
    'http_req_duration': ['p(95)<5000'], // 95% das requests < 5s
    'errors': ['rate<0.1'],              // Taxa de erro < 10%
  },
};

const BASE_URL = 'http://localhost:8080/api';

const testEmails = [
  'user1@example.com',
  'user2@example.com',
  // ... lista de emails para testar
];

export default function () {
  // Test 1: Find by email
  const email = testEmails[Math.floor(Math.random() * testEmails.length)];
  const res1 = http.get(`${BASE_URL}/users/by-email?email=${email}`);
  
  check(res1, {
    'status is 200': (r) => r.status === 200,
  });
  
  errorRate.add(res1.status !== 200);
  
  const queryTimeHeader = res1.headers['X-Query-Time'];
  if (queryTimeHeader) {
    queryTime.add(parseInt(queryTimeHeader));
  }
  
  sleep(1);
  
  // Test 2: Find by location
  const res2 = http.get(`${BASE_URL}/users/by-location?country=Brazil&city=São Paulo`);
  
  check(res2, {
    'status is 200': (r) => r.status === 200,
  });
  
  sleep(1);
}