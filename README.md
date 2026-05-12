# ✦ Taskflow — Todo App

Повнофункціональний веб-застосунок для управління задачами з підзадачами, пріоритетами, дедлайнами, повторюваними задачами та шерингом по email.

**[Посилання на застосунок](https://to-do-list-d.streamlit.app/)**
---

## 🛠 Стек технологій

### Backend
| Технологія | Призначення |
|---|---|
| **FastAPI** | REST API фреймворк |
| **SQLAlchemy** | ORM для роботи з БД |
| **SQLite** | База даних (файл `data/todo.db`) |
| **Pydantic v2** | Валідація даних / схеми |
| **JWT (python-jose)** | Авторизація через токени |
| **passlib + bcrypt** | Хешування паролів |
| **smtplib** | Відправка email (шеринг задач) |
| **pytest** | Тестування |

### Frontend
| Технологія | Призначення |
|---|---|
| **Streamlit** | Веб-інтерфейс |
| **requests** | HTTP-запити до API |

### Інфраструктура
| Технологія | Призначення |
|---|---|
| **Docker + Docker Compose** | Контейнеризація |
| **uvicorn** | ASGI-сервер для FastAPI |

---

## 🚀 Запуск

### Варіант 1 — Docker Compose (рекомендовано)

```bash
# Клонуй репозиторій
git clone <repo-url>
cd To-Do-List/todo-app

# Налаштуй змінні середовища
cp .env.example .env
# Відредагуй .env — вкажи SECRET_KEY та SMTP дані

# Запусти
docker-compose up --build
```

- API: http://localhost:8081
- Frontend: http://localhost:8502
- Swagger UI: http://localhost:8081/docs

---

### Варіант 2 — Локально

#### 1. Налаштуй `.env`

```bash
cd todo-app/backend
cp .env.example .env
# Відредагуй .env
```

#### 2. Backend

```bash
cd todo-app/backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Якщо вже є існуюча БД — запусти міграцію
python migrate_db.py

uvicorn app.main:app --reload --port 8081
```

API: http://localhost:8081 · Swagger: http://localhost:8081/docs

#### 3. Frontend (окремий термінал)

```bash
cd todo-app/frontend
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port 8502
```

Frontend: http://localhost:8502

#### 4. Тести

```bash
cd todo-app/backend
pytest tests/ -v
```

---

## ⚙️ Змінні середовища (`.env`)

```env
# Безпека
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# База даних
DATABASE_URL=sqlite:///./data/todo.db

# SMTP (для шерингу задач по email)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
EMAILS_FROM_EMAIL=your@gmail.com
```

> **Gmail:** увімкни двофакторну автентифікацію → Google Account → Security → App Passwords → згенеруй пароль і вкажи як `SMTP_PASSWORD`.

---

## 📁 Структура проєкту

```
To-Do-List/
└── todo-app/
    ├── backend/
    │   ├── app/
    │   │   ├── api/
    │   │   │   ├── routes/
    │   │   │   │   ├── auth.py          # Реєстрація, логін, зміна пароля
    │   │   │   │   ├── tasks.py         # CRUD задач, фільтри, статистика
    │   │   │   │   └── sharing.py       # Шеринг задач по email
    │   │   │   ├── __init__.py
    │   │   │   └── deps.py              # Залежності (get_current_user)
    │   │   ├── core/
    │   │   │   ├── config.py            # Налаштування (Pydantic Settings)
    │   │   │   └── security.py          # JWT, хешування паролів
    │   │   ├── db/
    │   │   │   ├── models/
    │   │   │   │   ├── task.py          # Модель Task (SQLAlchemy)
    │   │   │   │   └── user.py          # Модель User (SQLAlchemy)
    │   │   │   ├── data/
    │   │   │   │   └── todo.db          # SQLite БД (gitignore)
    │   │   │   └── session.py           # Engine, SessionLocal, Base
    │   │   ├── schemas/
    │   │   │   ├── task.py              # TaskCreate, TaskUpdate, TaskRead
    │   │   │   └── user.py              # UserCreate, UserRead, Token
    │   │   ├── services/
    │   │   │   └── email_service.py     # Відправка email через SMTP
    │   │   └── main.py                  # FastAPI app, middleware, роути
    │   ├── tests/
    │   │   ├── conftest.py              # Фікстури pytest
    │   │   ├── test_auth.py             # Тести авторизації
    │   │   └── test_tasks.py            # Тести задач
    │   ├── migrate_db.py                # Скрипт міграції SQLite БД
    │   ├── .env                         # Змінні середовища (не комітити!)
    │   ├── dockerfile
    │   └── requirements.txt
    ├── frontend/
    │   ├── streamlit_app.py             # Streamlit UI
    │   ├── dockerfile
    │   └── requirements.txt
    ├── .env                             # Спільні змінні для Docker Compose
    ├── .gitignore
    ├── docker-compose.yml
    └── README.md
```

---

## 🗄️ Модель даних

### Task
| Поле | Тип | Опис |
|---|---|---|
| `id` | int | Первинний ключ |
| `title` | string | Назва задачі |
| `description` | text | Опис (необов'язково) |
| `notes` | text | Нотатки/коментарі |
| `status` | enum | `todo` / `in_progress` / `done` |
| `priority` | enum | `low` / `medium` / `high` |
| `due_date` | date | Дедлайн |
| `tags` | JSON | Масив тегів |
| `recurrence` | enum | `none` / `daily` / `weekly` / `monthly` |
| `parent_id` | int FK | ID батьківської задачі (для підзадач) |
| `owner_id` | int FK | ID власника |
| `created_at` | datetime | Дата створення |
| `updated_at` | datetime | Дата оновлення |
| `completed_at` | datetime | Дата завершення |

---

## 📡 API ендпоінти

### Auth — `/auth`
| Метод | URL | Опис |
|---|---|---|
| `POST` | `/auth/register` | Реєстрація |
| `POST` | `/auth/login` | Логін (JWT токен) |
| `POST` | `/auth/change-password` | Зміна пароля |

### Tasks — `/tasks`
| Метод | URL | Опис |
|---|---|---|
| `GET` | `/tasks/` | Список задач (фільтри: status, priority, q, overdue, parent_id) |
| `POST` | `/tasks/` | Створити задачу |
| `GET` | `/tasks/{id}` | Отримати задачу |
| `PATCH` | `/tasks/{id}` | Оновити задачу |
| `DELETE` | `/tasks/{id}` | Видалити задачу |
| `DELETE` | `/tasks/` | Видалити всі задачі |
| `GET` | `/tasks/stats/summary` | Статистика задач |
| `POST` | `/tasks/share` | Надіслати задачі на email |

---

## ✨ Функціонал

- 🔐 **Авторизація** — реєстрація, JWT-логін, зміна пароля
- ✅ **Задачі** — створення, редагування, видалення, зміна статусу та пріоритету
- 📎 **Підзадачі** — ієрархія задач (розкриваються по кліку `▸`)
- 🔁 **Повторювані задачі** — щоденно/щотижня/щомісяця; при завершенні автоматично створюється наступна
- 📅 **Дедлайни** — індикатори "Overdue", "Due today", "3d left"
- 🏷 **Теги** — довільні мітки через кому
- 📝 **Нотатки** — приватні коментарі до задачі
- 🔍 **Пошук і фільтрація** — по назві, статусу, пріоритету, тегам, прострочені
- 📊 **Аналітика** — completion rate, breakdown по статусах і пріоритетах, список прострочених
- 📨 **Шеринг** — відправка списку задач на email
- 🗑 **Масове видалення** — очистити всі задачі
