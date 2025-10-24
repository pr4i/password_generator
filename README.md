# Password Generator — Microservices + Docker + NGINX + Swarm

Демо-проект для Практических работ №3.1 и №3.2.

## Архитектура

- `api` — FastAPI бэкенд для генерации паролей и взаимодействия с микросервисами.
- `policy-service` — микросервис оценки сложности и энтропии пароля.
- `audit-service` — микросервис логирования событий генерации (в памяти) + выдача истории.
- `frontend` — простая страница (React + Vite) для генерации паролей.
- `db` — PostgreSQL для хранения сгенерированных паролей (демо-таблица).
- `nginx` — обратный прокси/балансировщик (для 3.2).
- Docker Compose — локальный запуск (3.1).
- Docker Swarm — развёртывание стэка (3.2).

## Быстрый старт (Compose)

```bash
docker compose up --build
```

Откройте:
- Frontend: http://localhost:5173
- API: http://localhost:8000/docs

## Быстрый старт (Swarm)

```bash
docker swarm init
docker stack deploy -c docker-stack.yml pwgen
```

Проверьте:
- NGINX (проксирует на API/Frontend): http://localhost
- API: http://localhost/api/docs
- Frontend: http://localhost/