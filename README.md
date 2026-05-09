# 📋 Todo App

Веб-застосунок для управління задачами з можливістю шейрингу по email.

## Стек

- **Backend**: FastAPI + SQLite (SQLAlchemy) + JWT auth
- **Frontend**: Streamlit
- **Тести**: pytest

## Запуск

### 1. Клонуй репозиторій та налаштуй `.env`

```bash
cp .env .env
# Відредагуй .env — вкажи SMTP дані та SECRET_KEY
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API буде доступне на http://localhost:8000  
Swagger UI: http://localhost:8000/docs

### 3. Frontend (в окремому терміналі)

```bash
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Відкриється на http://localhost:8501

### 4. Тести

```bash
cd backend
pytest tests/ -v
```

## Налаштування Email (шейринг)

У `.env` вкажи SMTP дані. Для Gmail:
1. Увімкни двофакторну автентифікацію
2. Створи **App Password**: Google Account → Security → App Passwords
3. Вкажи його як `SMTP_PASSWORD`

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
EMAILS_FROM_EMAIL=your@gmail.com
```

## Структура проєкту

```
todo-app/
├── backend/
│   ├── app/
│   │   ├── api/routes/     # auth, tasks, sharing
│   │   ├── core/           # config, security (JWT)
│   │   ├── db/models/      # User, Task (SQLAlchemy)
│   │   ├── schemas/        # Pydantic моделі
│   │   ├── services/       # email_service
│   │   └── main.py
│   └── tests/
├── frontend/
│   └── streamlit_app.py
└── .env.example
```
