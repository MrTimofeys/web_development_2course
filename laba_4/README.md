# Лабораторная работа 4

Flask-приложение для управления учетными записями пользователей.

## Запуск

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/flask --app app run
```

При первом запуске автоматически создается SQLite-база `instance/laba_4.sqlite`,
две роли и пользователь-администратор.

Данные для входа:

- логин: `admin`
- пароль: `Admin123`
