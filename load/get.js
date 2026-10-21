// ЛР8: виртуальные пользователи (VUs) отправляют GET-запрос к API калькулятора стенда.
// Запуск: k6 run --vus 10 --duration 30s load/get.js
// Параметры: BASE_URL (адрес стенда), SLEEP (пауза между запросами одного VU, секунды).
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:5000';
const PAUSE = Number(__ENV.SLEEP ?? 1);

// Цели теста, записанные как пороги: при нарушении k6 завершается с ошибкой.
export const options = {
  thresholds: {
    http_req_duration: ['p(95)<300'], // 95% ответов быстрее 300 мс
    http_req_failed: ['rate<0.01'], // меньше 1% ошибок
    checks: ['rate>0.99'], // ответы правильные по содержанию
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/api/calc?a=2&b=3&op=add`);
  check(res, {
    'статус 200': (r) => r.status === 200,
    'результат 5': (r) => r.json('result') === 5,
  });
  sleep(PAUSE);
}
