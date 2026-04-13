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


#### 2 Employee Login
**Inputs:**
- Email(string, required, unique, valid format)
- Password(string, required)


**Output:**
- message
- Access Token
- Tefresh Token
- Email(string)
- Employee Id (string)

#### 2 Employee Logout
**Inputs:**
- access_token (string)

**Output:**
- message



### Dependenciees:

#### External Depedencies
PostgreSQL
Django REST Framework(DRF)
SimpleJWT 
Redis

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

#### 2. Employee Login
##### POST Method
##### URL : http://localhost:8000/api/v1/authcore/loginauth/


### Request Body

```json
{
 
  "email": "sylvesterkouassi@yahoo.com",
  "password": "StrongPassword123!"

}
```
###  Response (200 Ok)

```json
{
    "message": "Login successful",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc2MDg4NzQyLCJpYXQiOjE3NzYwODY5NDIsImp0aSI6Ijk0ODQ0NDc4NjU0YjQ4ODJhNzc4MTM0NmVmNjQ0NDdlIiwidXNlcl9pZCI6ImE5ZTdjMmM3LTQwNTAtNDM5Ni04ZjI0LWQzODJiMjYxZDg4NyJ9.P2pJALG-m254fp_8gf_Bs32NGr308fyqLv_N813yCKI",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3NjE3MzM0MiwiaWF0IjoxNzc2MDg2OTQyLCJqdGkiOiI4NDAwZWYxMWFlY2E0ZjMxYjQwZjg4ZjMyNjZlMDdhMiIsInVzZXJfaWQiOiJhOWU3YzJjNy00MDUwLTQzOTYtOGYyNC1kMzgyYjI2MWQ4ODcifQ.OeLpZzD7rNqt5fTt8CjiVVlaIDYNWcLYqJn4yZNPjgo",
    "email": "sylvesterkouassi@yahoo.com",
    "Emp_id": "EMP-2026-001"
}
```

#### 3. Employee Logout
##### POST Method
##### URL : http://localhost:8000/api/v1/authcore/logout/

#### HEADER
``` bash
Authorization : Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc1OTI1NzQ3LCJpYXQiOjE3NzU5MjM5NDcsImp0aSI6ImMyYjg5N2U3ZmM5MjRjNDQ4NTg4ODJhN2Y4ZjE5Zjc5IiwidXNlcl9pZCI6ImE5ZTdjMmM3LTQwNTAtNDM5Ni04ZjI0LWQzODJiMjYxZDg4NyJ9.t2I6zG98wUMyce6oIx1VNWlZmwQ_Oy62pKK4wR-P7Is
```


### Request Body

```json
{

}
```
###  Response (200 Ok)

```json
{
    "message": "Logout successful"
}
```