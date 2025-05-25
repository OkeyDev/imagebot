# Проект для конвертации изображений

Небольшой проект для конвертации изображений из одного формата в другой используя ImageMagick с реализованной регистрацией и аутентификацией пользователей.

### Стэк

- [FastAPI](https://fastapi.tiangolo.com)
  - [SQLModel](https://sqlmodel.tiangolo.com) для работы с SQL базой данных (ORM на основе SQLAlchemy)
  - [Pydantic](https://docs.pydantic.dev/) - для работы с JSON
  - [PostgreSQL](https://www.postgresql.org/) - база данных
  - [Celery](https://docs.celeryq.dev) - очередь задач. Для масштабирования вширь
  - [Redis](https://redis.io/) для ограничения количества запросов.
- [Docker](https://docs.docker.com/) + [Docker compose](https://docs.docker.com/compose/)  для сборки проекта
- Хэширование паролей с использованием passlib
- JWT для входа в аккаунт

### В планах добавить

- [ ] Healthckeck для API
- [ ] Docker compose watch для удобной разработки
- [ ] Telegram bot для работы с API
- [ ] Документация для API + Docstring
- [ ] Тесты с pytest
- [ ] JWT blacklist с использованием Redis
- [ ] Мониторинг с использованием Prometheus + Grafana
- [ ] CI/CD Pipeline

## Загрузка и запуск проекта

Для этого у вас должен быть Docker + Docker compose или Docker Desktop.

**Загрузка проекта:**

```sh
cd ~
git clone https://github.com/OkeyDev/imagebot
cd imagebot
```

**Запуск:**

```sh
cp .env.default .env
docker compose up -d 
```

API будет доступен по ссылке <http://localhost:8000> (если на этом порту не запущены другие приложения).
Документация достуна по ссылке: <http://localhost:8000/docs>

## Использование

1. Зарегестрируйте пользователя вызвав /register. Валидации данных нет, так что можно оставить значения по умолчанию.
2. Войдите в свой аккаунт использую кнопку Authorize вверху страницы слева. Введите логин и пароль, которые вы вводили в /register.
  Если вы ничего не меняли используйте логин string и пароль string.
3. Отправьте запрос /string с необходимым форматом и изображением.
