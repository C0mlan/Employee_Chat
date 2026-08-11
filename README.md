#   EMPLOYEE CHAT SYSTEM – Backend

## Project overview
A backend system that provides a secure and private messaging solution for employees and administrators. It enables each employee to exchange messages and communicate directly with admins in real time. It allows employee to share information online, while ensuring:

* "Privacy: Chats are private between employee and admin"

* "Authentication & Roles: Employees and admins have controlled access"

* "Persistence: Messages are saved in the database"



---
## Technology Stack:
| Category | Technology                      |
|----------|---------------------------------|
| Language |Python 3           |
| Framework | Django 5 + Django REST Framework            |
| Security | JWT            |
| Database | PostgreSQL 15(Docker container)                      |
| Cache / Message Broker: | Redis 7 (Docker container)                         |
| Testing | Pytest |
| Containerization | Docker, Docker Compose          |
| CI/CD | GitHub Actions                  |
| API Documentation | OpenAPI, Swagger UI   |

## 🛠 Getting Started

### Prerequisites

Before running the project, make sure you have the following installed:

* Python 3
* Docker
* Git

### Clone the Repository

```bash
git clone https://github.com/C0mlan/Employee_Chat.git
cd Employee_Chat
```

### Configure Environment Variables

Create a .env file in the project root.

Copy the variables from `.env.example` into `.env` and update the values according to your local environment.

### Start the Application

The project runs all required services inside Docker containers, including:

* Django
* PostgreSQL
* Redis
* Celery

Build and start the containers with:

```bash
docker compose up --build
```

Once the containers are running, the Django application will be available at:

```text
http://localhost:8000
```

### Apply Database Migrations

Run the Django migrations inside the web container:

```bash
docker exec -it employee_chat-web-1 python manage.py migrate
```

### Create a Superuser

To create a Django admin account:

```bash
docker exec -it employee_chat-web-1 python manage.py createsuperuser
```

Follow the prompts to enter the superuser credentials.

### Verify Running Services

To check that all Docker services are running:

```bash
docker compose ps
```

You should see the project's containers for Django, PostgreSQL, Redis, and Celery.

### Run the Application

Start the Django application using:

```bash
doker compose up
```

### Run Tests

Run the complete test suite inside the Django container:

```bash
docker compose exec web pytest -v
```

## Features

### Authentication & Authorization

* Employee registration. 
* JWT-based access and refresh token authentication.
* Role-based access control for managers, team leads, and employees.


### Direct Messaging

* One-to-one messaging between employees.
* Real-time message delivery through WebSockets.


## Architecture


## API Documentation

The API follows RESTful design principles and uses JWT-based authentication.

Interactive API documentation is available through Swagger/OpenAPI.

For detailed endpoint specifications, request/response schemas,
authentication requirements, and error responses, see:



[- API Reference](docs/api_documentation.md)


