# Library Service API

DRF-based API service for managing a library system: books, users, borrowings, returns, permissions, JWT authentication, API documentation, tests, and Docker setup.

## Features

* Books CRUD
* Book inventory management
* Custom user model with email authentication
* JWT authentication
* Admin-only book management
* Borrowing list and detail endpoints
* Borrowing creation with automatic inventory decrease
* Borrowing return endpoint with automatic inventory increase
* Borrowing filtering by active status and user
* Swagger API documentation
* Docker Compose setup with PostgreSQL
* Test coverage: 92%

## Tech Stack

* Python
* Django
* Django REST Framework
* Simple JWT
* PostgreSQL
* Docker / Docker Compose
* drf-spectacular
* pytest
* pytest-django
* pytest-cov

## Selected Coding Tasks

Implemented tasks from the project specification:

1. Implement CRUD functionality for the Books Service
2. Add permissions to the Books Service
3. Implement CRUD for the Users Service
4. Implement the Borrowing List & Detail endpoint
5. Implement the Create Borrowing endpoint
6. Add filtering for the Borrowings List endpoint
7. Implement a return Borrowing functionality
8. Setup docker-compose

## Installation

Clone the repository:

```bash
git clone https://github.com/Aeros72/drf-library-service.git
cd drf-library-service
```

Create and activate virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root using `.env.sample` as an example.

Example:

```env
SECRET_KEY=dev-secret-key
DEBUG=True

POSTGRES_DB=library_db
POSTGRES_USER=library_user
POSTGRES_PASSWORD=library_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

For Docker usage:

```env
POSTGRES_HOST=db
```

## Run Locally

Apply migrations:

```bash
python manage.py migrate
```

Create superuser:

```bash
python manage.py createsuperuser
```

Run server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/api/
```

## Run With Docker

Build and start containers:

```bash
docker compose up --build
```

The app will be available at:

```text
http://127.0.0.1:8000/api/
```

To stop containers:

```bash
docker compose down
```

## API Documentation

Swagger documentation is available at:

```text
http://127.0.0.1:8000/api/doc/
```

Schema endpoint:

```text
http://127.0.0.1:8000/api/schema/
```