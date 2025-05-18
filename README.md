Library Management API \
This is a REST API for managing a library system built with Django REST Framework (DRF) and SQLite database. It includes user management, book reservations, and rating functionalities.\
Default Users\

The following default users are created during migration:\


Admin: username: rozagul, password: 1234, role: admin.\  

Operator: username: operator, password: operator1, role: operator\

User: username: Nodirbekova, password: Nodirbekova, role: user\


Docker\

Ensure Docker and Docker Compose are installed.\
Run the following command to start the application:docker-compose up --build\


The API will be available at http://127.0.0.1:8080/api/v1/.\


Run Migrations:Migrations are automatically applied via Docker Compose. Default users will be created.\


API Endpoints\

Authentication\

POST /api/v1/token/: \
'{"username": "rozagul", "password": "1234"}'\


POST /api/v1/token/refresh/: Refresh a JWT token.\

User Management\

POST /api/v1/users/signup/: Register a new user (role: user only, open to all).curl -X POST 'http://127.0.0.1:8080/api/v1/users/signup/' \

-H 'Content-Type: application/json' \
-d '{"username": "newuser", "password": "pass123"}'\


POST /api/v1/users/create/: Create a new user (admin only).curl -X POST 'http://127.0.0.1:8080/api/v1/users/create/' \

-H 'Authorization: Bearer <admin_token>' \
-H 'Content-Type: application/json' \
-d '{"username": "newadmin", "password": "adminpass", "role": "admin"}'


GET /api/v1/users//: Retrieve a user (admin only).
PUT /api/v1/users//: Update a user (admin only).
PATCH /api/v1/users//: Partially update a user (admin only).
DELETE /api/v1/users//: Delete a user (admin only).

Books

GET /api/v1/books/: List all books (open to all).curl -X GET 'http://127.0.0.1:8080/api/v1/books/'


POST /api/v1/books/: Create a book (admin only).
GET /api/v1/books//: Retrieve a book (open to all).
PUT /api/v1/books//: Update a book (admin only).
PATCH /api/v1/books//: Partially update a book (admin only).
DELETE /api/v1/books//: Delete a book (admin only).

Orders

POST /api/v1/orders/create/: Reserve a book (user only).curl -X POST 'http://127.0.0.1:8080/api/v1/orders/create/' \
-H 'Authorization: Bearer <user_token>' \
-H 'Content-Type: application/json' \
-d '{"book": 1}'


GET /api/v1/orders/check/: Check and cancel reservations older than 1 day (user only).curl -X GET 'http://127.0.0.1:8080/api/v1/orders/check/' \
-H 'Authorization: Bearer <user_token>'


GET /api/v1/orders//: Retrieve an order (user only).
PUT /api/v1/orders//: Update an order (operator/admin only).
PATCH /api/v1/orders//: Partially update an order (operator/admin only).
DELETE /api/v1/orders//: Delete an order (operator/admin only).
POST /api/v1/orders//take/: Take a reserved book (operator/admin only).curl -X POST 'http://127.0.0.1:8080/api/v1/orders/1/take/' \
-H 'Authorization: Bearer <operator_token>'


POST /api/v1/orders//return/: Return a book and calculate fine (operator/admin only).curl -X POST 'http://127.0.0.1:8080/api/v1/orders/1/return/' \
-H 'Authorization: Bearer <operator_token>'



Ratings

POST /api/v1/ratings/create/: Rate a book (user only, 0-5 stars).curl -X POST 'http://127.0.0.1:8080/api/v1/ratings/create/' \
-H 'Authorization: Bearer <user_token>' \
-H 'Content-Type: application/json' \
-d '{"book": 1, "score": 4}'


GET /api/v1/ratings//: Retrieve a rating (user only).
PUT /api/v1/ratings//: Update a rating (admin only).
PATCH /api/v1/ratings//: Partially update a rating (admin only).
DELETE /api/v1/ratings//: Delete a rating (admin only).

Permissions

Admin (role: admin): Can access all endpoints.
Operator (role: operator): Can access /orders/<pk>/take/, /orders/<pk>/return/, and modify orders (PUT, PATCH, DELETE).
User (role: user): Can access /orders/create/, /orders/check/, /ratings/create/, and view-only endpoints. If a user tries to access restricted endpoints (e.g., DELETE /users/<pk>/), a 403 error with "You do not have permission to perform this action." will be returned.

