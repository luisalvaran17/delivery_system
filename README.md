
# Delivery Service API

## Introduction

This is a backend system for a delivery service that allows users to manage addresses, manage drivers, assign services to drivers. The project is built using the following technologies:

- **Python 3.x**: The programming language used for backend development.
- **Django**: The web framework used to build the application.
- **Django Rest Framework (DRF)**: A powerful toolkit for building Web APIs in Django.
- **PostgreSQL**: The relational database used to store data.
- **Docker**: Used for containerizing the application and managing dependencies with `docker-compose.yml`.
- **JWT Authentication**: JSON Web Tokens (JWT) are used to secure API endpoints and provide authentication.

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
OPENROUTE_SERVICE_KEY=<your-openrouteservice-apikey>
```

### Running Migrations

Once the containers are up and running, you can apply the migrations to create the database tables.

```bash
docker-compose exec web python manage.py migrate
```

### Faker

You can populate the database with fake addresses and drivers for testing purposes using the seed command.

```bash
docker-compose exec web python manage.py seed_data
```

This will create:
- 20 random addresses.
- 20 random drivers with associated users and addresses.

## API Endpoints: Service Requests

### 1. **Request Service**
   - **Endpoint**: `POST /api/services/`
   - **Description**: Create a new service request.
   - **Request Body**:
      ```json
       {   
         "pickup_address": {
             "street": "Cl. 68a #90a – 31",
             "city": "Bogotá",
             "latitude": 4.693408,
             "longitude": -74.112279
         } 
       }
      ```
   - **Response**:
     ```json
        {
           "id": 9,
           "client": "client1",
           "pickup_address": {
               ...
           },
           "assigned_driver": {
               "id": 116,
               "user": "esteban74",
               "current_address": {
                   "id": 181,
                   "street": "Avenida Caracas 58",
                   "city": "Bogotá",
                   "latitude": 4.655587,
                   "longitude": -74.103641
               },
               "is_available": false
           },
           "estimated_time_minutes": 15,
           "created_at": "2025-04-28T01:38:32.382421Z",
           "status": "in progress"
       }
     ```

### 2. **Get Address List**
   - **Endpoint**: `GET /api/services/`
   - **Description**: Get a list of all services.

### 3. **Get Service Detail**
   - **Endpoint**: `GET /api/services/{id}/`
   - **Description**: Get details of a specific service.

### 4. **Update Service**
   - **Endpoint**: `PUT /api/services/{id}/`
   - **Description**: Update a specific service.

### 5. **Delete Service**
   - **Endpoint**: `DELETE /api/services/{id}/`
   - **Description**: Delete a specific service.

### 6. **Complete Service Request**
   - **Endpoint**: `DELETE /api/services/{id}/complete/`
   - **Description**: Complete a specific service by driver.
   - **Request Body**:
     ```json
      {
      "status": "completed"
      }
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


## API Endpoints: Drivers CRUD

### 1. **Create Driver**
   - **Endpoint**: `POST /api/drivers/`
   - **Description**: Create a new driver.
   - **Request Body**:
     ```json
     {
       "current_address": {
         "street": "Av. Siempre Viva",
         "city": "Bogotá",
         "latitude": 4.60971,
         "longitude": -74.08175
       },
       "is_available": true
     }
     ```

### 2. **Get Driver List**
   - **Endpoint**: `GET /api/drivers/`
   - **Description**: Get a list of all drivers.
   - **Response**:
     ```json
     [
       {
         "id": 1,
         "user": "yarrieta",
         "current_address": {
           "id": 1,
           "street": "Av. Siempre Viva",
           "city": "Bogotá",
           "latitude": 4.60971,
           "longitude": -74.08175
         },
         "is_available": true
       }
     ]
     ```

### 3. **Get Driver Detail**
   - **Endpoint**: `GET /api/drivers/{id}/`
   - **Description**: Get details of a specific driver.

### 4. **Update Driver**
   - **Endpoint**: `PUT /api/drivers/{id}/`
   - **Description**: Update a specific driver's information.
   - **Request Body**:
     ```json
     {
       "current_address": {
         "street": "New Street",
         "city": "New City",
         "latitude": 4.61000,
         "longitude": -74.08000
       },
       "is_available": false
     }
     ```

### 5. **Delete Driver**
   - **Endpoint**: `DELETE /api/drivers/{id}/`
   - **Description**: Delete a specific driver.


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
