# Итоговый отчёт ревью Demo27

**Объект:** Demo27 (Flask API + web UI + PostgreSQL)  
**Основание:** статический анализ предоставленного ZIP-архива  
**Статус:** код просмотрен; часть динамических проверок недоступна в среде ревью

## Итог
Обнаружены несколько значимых рисков безопасности. Наиболее критичный — публичная регистрация позволяет выбрать роль администратора. Дополнительно бизнес API CRUD endpoints не защищены авторизацией; пользовательские поля вставляются в DOM через `innerHTML`; CAPTCHA в веб-входе отключена; в конфигурации есть слабые fallback секреты; `run.py` запускает debug и bind на `0.0.0.0`.

## Приоритетные findings
| ID | Приоритет | Проблема | Файл/место |
|---|---|---|---|
| SEC-01 | Critical | Публичная регистрация с ролью администратора | `app/blueprints/auth.py`, register |
| SEC-02 | High | CRUD API без login/role проверки | `app/views/base_view.py`, `app/views/*_view.py` |
| SEC-06 | High | Пользовательские значения вставляются через `innerHTML` (XSS-risk) | `web/notes.html`, `web/clients.html`, другие шаблоны |
| SEC-04 | High | Предсказуемые fallback SECRET_KEY и DB password | `app/config.py` |
| SEC-05 | High (deployment) | Debug=True и bind 0.0.0.0 | `run.py` |
| SEC-03 | Medium/High | CAPTCHA не проверяется при web-login | `app/blueprints/web.py` |
| SEC-08 | Medium | CSRF защита не обнаружена для session-based изменяющих запросов | конфигурация и routes |
| L-04 | Medium | Неоднородная валидация входных данных | API views/services |
| S-01 | Low | Дублирующий `request.get_json()` | `app/blueprints/auth.py` |
| S-03 | Low/Medium | Параллельные API реализации в blueprints и views | `app/blueprints/`, `app/views/` |

## Проверки и ограничения
- Python syntax compilation: **67/67 файлов успешно**.
- pytest: **не запустился**, сборка тестов остановлена из-за отсутствующего Flask в runtime (`ModuleNotFoundError`). Это не результат выполнения тестов.
- flake8/pylint: не установлены, не запускались.
- Скриптовый style scan: 84 trailing-whitespace строки; 112 строк длиной более 88 символов.
- Онлайн проверка CVE зависимостей не выполнялась.
- XSS не подтверждался запуском payload в браузере: статически подтверждены опасные `innerHTML` sinks и пользовательские данные в них.

## План исправлений (не применялись к исходному проекту)
1. Публичный `/api/auth/register`: роль не брать из запроса, всегда назначать обычного пользователя.
2. Закрыть бизнес CRUD API аутентификацией; права на операции проверять отдельно.
3. Заменить динамический `innerHTML` с данными API на безопасное создание DOM и `textContent`.
4. Убрать слабые fallback секреты, проверять наличие env-переменных при production запуске.
5. Разделить dev/prod запуск: `debug=False` и WSGI для production.
6. Подключить реальную CAPTCHA проверку и CSRF protection.
7. Добавить regression tests для прав, регистрации роли, XSS input handling и блокировки.

## Предлагаемые commit messages
- `review(day-1): add repository map and checklist`
- `review(day-2): document style findings`
- `review(day-3): analyze API logic and database`
- `review(day-4): document security and dependencies`
- `review(day-5): finalize review report`
- `fix: prevent public admin role registration`
- `fix: protect CRUD API endpoints`
- `fix: render user content safely`

## Важно
Это отчёты ревью, а не фиксация того, что исправления уже внесены. Рекомендуемые исправления требуют отдельной ветки, изменения кода, тестов и подтверждения результата.
