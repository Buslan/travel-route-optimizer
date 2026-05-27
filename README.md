# Travel Route Optimizer

Веб-приложение для подбора маршрута путешествия через несколько точек с оптимизацией по времени, стоимости и пользовательским предпочтениям.

Проект разработан как учебная работа по направлению «Прикладная математика и информатика». Основной акцент сделан не только на визуальном интерфейсе, но и на математической модели маршрута, графовой структуре данных, целевой функции и алгоритме многокритериальной оптимизации.

---

## Цель проекта

Разработать веб-приложение, которое позволяет пользователю построить оптимальный маршрут путешествия через несколько промежуточных точек с учётом:

- общего времени маршрута;
- общей стоимости маршрута;
- пользовательских предпочтений;
- рейтинга посещаемых точек;
- ограничений по бюджету и времени.

---

## Используемые технологии

### Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn
- Pydantic

### Frontend

- HTML
- CSS
- JavaScript

### База данных

- SQLite

---

## Структура проекта

```text
travel_route_app/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── data/
│   │   └── seed_data.py
│   │
│   ├── routes/
│   │   ├── places.py
│   │   ├── routes.py
│   │   └── optimizer.py
│   │
│   └── services/
│       ├── route_optimizer.py
│       ├── route_storage.py
│       ├── cost_calculator.py
│       └── preference_service.py
│
├── frontend/
│   ├── index.html
│   ├── planner.html
│   ├── result.html
│   ├── about.html
│   │
│   ├── css/
│   │   ├── style.css
│   │   ├── landing.css
│   │   ├── planner.css
│   │   ├── result.css
│   │   ├── about.css
│   │   ├── liquid-upgrade.css
│   │   └── graph-align.css
│   │
│   ├── js/
│   │   ├── app.js
│   │   ├── planner.js
│   │   ├── result.js
│   │   └── about.js
│   │
│   └── assets/
│       └── images/
│
├── requirements.txt
├── travel_routes.db
└── README.md