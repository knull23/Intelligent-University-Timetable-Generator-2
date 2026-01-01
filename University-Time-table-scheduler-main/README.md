# University Timetable Scheduler 

**University Timetable Scheduler** is a full‑stack application that automates university timetable creation using a genetic algorithm. It includes a Next.js/React frontend and a Django REST backend with scheduling, management, and visualization tools.

---

## 🔧 Tech Stack

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS
- **Backend:** Django, Django REST Framework, Python
- **DB (dev):** SQLite
- **Testing:** Jest (frontend), Django test runner (backend)

---

## 🚀 Key Features

- Automated timetable generation via a genetic algorithm
- CRUD for Courses, Instructors, Rooms, Sections & Timetables
- JWT-based authentication (DRF SimpleJWT)
- Fitness progression visualization for algorithm convergence
- Management commands for seeding meeting times and debugging the GA

---

## ✅ Quick Start

### Prerequisites

- Node.js (v18+ recommended) and npm
- Python 3.10+ and pip
- Optional: virtualenv

### Backend (Django)

1. Open a terminal and go to the backend folder:

   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:

   Windows:
   ```bash
   python -m venv venv
   .\\venv\\Scripts\\activate
   ```

   macOS / Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. (Important) Apply database migrations:

   ```bash
   python manage.py migrate
   ```

   ⚠️ If you encounter errors about missing columns (e.g., `no such column: scheduler_app_course.semester`), make sure all migrations are applied (`python manage.py showmigrations` then `python manage.py migrate`).

5. (Optional) Create a superuser to access the admin:

   ```bash
   python manage.py createsuperuser
   ```

6. Start the backend server:

   ```bash
   python manage.py runserver
   ```

The API base will be available at: `http://localhost:8000/api/`.

### Frontend (Next.js)

1. From project root:

   ```bash
   npm install
   npm run dev
   ```

2. Open the frontend at `http://localhost:3000`.

---

## 🧪 Tests

- Backend tests:

  ```bash
  # from backend/
  python manage.py test
  ```

- Frontend tests (Jest):

  ```bash
  npm test
  ```

---

## ⚙️ Useful Management Commands

- Seed/generate meeting time slots:
  - `python manage.py add_meeting_times`
  - `python manage.py add_meeting_times_new`
- Add curriculum or assign instructors:
  - `python manage.py add_curriculum`
  - `python manage.py assign_instructors_to_courses`
- Debug genetic algorithm:
  - `python manage.py debug_ga`

---

## 📡 API Overview

Base URL: `http://localhost:8000/api/`

Common endpoints:

- `POST /api/token/` — obtain JWT tokens
- `GET/POST /api/courses/`
- `GET/POST /api/instructors/`
- `GET/POST /api/rooms/`
- `GET/POST /api/timetables/` (also triggers timetable generation in UI)

(See the Django app `scheduler_app` for full serializer/view logic.)

---

## 🐞 Troubleshooting

- Missing DB columns / 500 errors: run `python manage.py showmigrations` and `python manage.py migrate` to ensure all migrations are applied.
- Static files warning in dev: ensure `backend/static` exists or update `STATICFILES_DIRS` in `scheduler/settings.py`.
- If the frontend complains about API URLs, check `lib` utilities for API base settings or ensure backend is running on port 8000.

---

## 🤝 Contributing

Contributions are welcome — please open issues or pull requests. Quick tips:

1. Fork and create a feature branch
2. Run tests and ensure linting
3. Keep changes small and well-documented

---

## 📄 License & Contact

This repository does not declare a license file. If you want to add one, consider `MIT` or another permissive license.

Maintainer: Project owner (use repo issues for contact)

---

If you'd like, I can also:
- Add a concise `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`
- Add a `LICENSE` file (e.g., MIT)

Let me know what you'd like next! ✨
