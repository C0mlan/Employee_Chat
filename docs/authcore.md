##  Module Name: Auth Core

### Purpose
This module is responsible for all aspects of user authentication and access control in the Employee Chat System. It provides a secure, reliable, and centralized authentication system that enables controlled access to the chat system and protects user data.

### Operations

####  1. Registration
**Inputs:**
- First name(string, required)
- last name(string, required)
- email(string, required, unique, valid format)
- password(string, required)
- confirm password(string, required)

**Output:**
- User Id(uuid)
- Employe Id (string)
- First name(string)
- last name(string)
- email(string)
- is Verified(boolean)
- role(string)

### Dependenciees:

#### External Depedencies
PostgreSQL
Django REST Framework(DRF)

#### Internal Depedencies








## API DESIGN
### Endpoints
#### 1. Employee Registration
##### POST Method
##### URL : http://localhost:8000/api/v1/authcore/register/



### Request Body

```json
{
  "first_name": "sylvester",
  "last_name": "Kouassi",
  "email": "sylvesterkouassi@yahoo.com",
  "password": "StrongPassword123!",
  "confirm_password": "StrongPassword123!"
}
```
Response (201 Created)

```json
{
    "message": "User created successfully",
    "id": "561b408b-9601-44ac-a409-a71455b167cc",
    "emp_id": "EMP-2026-001",
    "first_name": "sylvester",
    "last_name": "Kouassi",
    "email": "sylvesterkouassi@yahoo.com",
    "is_verified": false,
    "role": "employee"
}
```