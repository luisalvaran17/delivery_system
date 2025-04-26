
# Delivery Service API

## Introduction

This is a backend system for a delivery service that allows users to manage addresses, manage drivers, assign services to drivers. The project is built using the following technologies:

- **Python 3.x**: The programming language used for backend development.
- **Django**: The web framework used to build the application.
- **Django Rest Framework (DRF)**: A powerful toolkit for building Web APIs in Django.
- **PostgreSQL**: The relational database used to store data.
- **Docker**: Used for containerizing the application and managing dependencies with `docker-compose.yml`.
- **JWT Authentication**: JSON Web Tokens (JWT) are used to secure API endpoints and provide authentication.

## Technologies Used

- Python 3.x
- Django
- Django Rest Framework (DRF)
- PostgreSQL
- Docker (docker-compose.yml)
- JWT Authentication

## Setup and Installation

### Prerequisites

Before running the project, ensure you have the following installed:

- Docker
- Docker Compose

### Running the Application

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Build and run the containers:
   ```bash
   docker-compose up --build
   ```

3. Access the application in your browser at:
   ```
   http://localhost:8000
   ```

### Environment Variables

The environment variables used in the `.env` file are:

```plaintext
DATABASE_NAME=<your-database-name>
DATABASE_USER=<your-database-username>
DATABASE_PASSWORD=<your-database-password>
DATABASE_HOST=db
DATABASE_PORT=5432
```

### Running Migrations

Once the containers are up and running, you can apply the migrations to create the database tables.

```bash
docker-compose exec web python manage.py migrate
```

## API Endpoints: Addresses CRUD

### 1. **Create Address**
   - **Endpoint**: `POST /api/addresses/`
   - **Description**: Create a new address.
   - **Request Body**:
     ```json
     {
       "street": "Av. Siempre Viva",
       "city": "Bogotá",
       "latitude": 4.60971,
       "longitude": -74.08175
     }
     ```
   - **Response**:
     ```json
     {
       "id": 1,
       "street": "Av. Siempre Viva",
       "city": "Bogotá",
       "latitude": 4.60971,
       "longitude": -74.08175
     }
     ```

### 2. **Get Address List**
   - **Endpoint**: `GET /api/addresses/`
   - **Description**: Get a list of all addresses.
   - **Response**:
     ```json
     [
       {
         "id": 1,
         "street": "Av. Siempre Viva",
         "city": "Bogotá",
         "latitude": 4.60971,
         "longitude": -74.08175
       }
     ]
     ```

### 3. **Get Address Detail**
   - **Endpoint**: `GET /api/addresses/{id}/`
   - **Description**: Get details of a specific address.
   - **Response**:
     ```json
     {
       "id": 1,
       "street": "Av. Siempre Viva",
       "city": "Bogotá",
       "latitude": 4.60971,
       "longitude": -74.08175
     }
     ```

### 4. **Update Address**
   - **Endpoint**: `PUT /api/addresses/{id}/`
   - **Description**: Update a specific address.
   - **Request Body**:
     ```json
     {
       "street": "New Street",
       "city": "New City",
       "latitude": 4.61000,
       "longitude": -74.08000
     }
     ```
   - **Response**:
     ```json
     {
       "id": 1,
       "street": "New Street",
       "city": "New City",
       "latitude": 4.61000,
       "longitude": -74.08000
     }
     ```

### 5. **Delete Address**
   - **Endpoint**: `DELETE /api/addresses/{id}/`
   - **Description**: Delete a specific address.
   - **Response**:
     ```json
     {
       "message": "Address deleted successfully."
     }
     ```

## Authentication

The API uses **JWT authentication** for securing the endpoints.

- **Obtain Token**: `POST /api/token/`
  - **Request Body**:
    ```json
    {
      "username": "user",
      "password": "password"
    }
    ```
  - **Response**:
    ```json
    {
      "access": "your-jwt-access-token",
      "refresh": "your-jwt-refresh-token"
    }
    ```

All other API endpoints require the `Authorization` header with the `Bearer` token:

```plaintext
Authorization: Bearer <your-jwt-access-token>
```
