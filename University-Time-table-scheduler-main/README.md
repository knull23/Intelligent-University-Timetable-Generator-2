# University Timetable Scheduler

This is a full-stack application designed to automate the creation of university timetables. It uses a genetic algorithm to find optimal schedules based on a set of constraints. The frontend is a modern web interface built with Next.js, and the backend is a powerful REST API powered by Django.

## Tech Stack

- **Frontend:**
  - Next.js
  - React
  - TypeScript
  - Tailwind CSS
  - Axios

- **Backend:**
  - Django
  - Django Rest Framework
  - Python
  - SQLite (default)

## Features

- **Automated Timetable Generation:** The core feature of the application. It uses a genetic algorithm to generate conflict-free timetables.
- **CRUD Operations:** Manage essential data like courses, instructors, rooms, and departments through a user-friendly interface.
- **Authentication:** Secure user authentication using JWT.
- **Dashboard:** A central dashboard to view statistics and manage the scheduling process.
- **Fitness Progression:** Visualize the improvement of the genetic algorithm's solution over generations.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Node.js and npm
- Python and pip

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Start the backend server:**
    ```bash
    python manage.py runserver
    ```
    The backend API will be available at `http://localhost:8000`.

### Frontend Setup

1.  **Navigate to the project root directory:**
    ```bash
    cd .. 
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Start the development server:**
    ```bash
    npm run dev
    ```
    The frontend will be accessible at `http://localhost:3000`.

## Project Structure

- **`/app`**: Contains the Next.js pages and layouts for the frontend application.
- **`/backend`**: The Django project that houses the backend REST API and the genetic algorithm logic.
  - **`/backend/scheduler_app`**: The main Django app containing models, views, and the core scheduling algorithm.
- **`/components`**: Reusable React components used throughout the frontend.
- **`/lib`**: Utility functions and API connection logic for the frontend.

## API Endpoints

The backend exposes a REST API built with Django Rest Framework. The base URL for the API is `/api/`.

Some of the key endpoints include:

- `/api/token/`: User authentication.
- `/api/timetables/`: CRUD for timetables and triggering generation.
- `/api/courses/`: CRUD for courses.
- `/api/instructors/`: CRUD for instructors.
- `/api/rooms/`: CRUD for rooms.

## Testing

The frontend uses Jest for component testing. You can run the tests with:

```bash
npm test
```
