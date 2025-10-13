# API Documentation

## Authentication Endpoints

### POST /api/auth/login
- **Description**: User authentication
- **Body**: `{ "email": "user@example.com", "password": "password" }`
- **Response**: `{ "token": "jwt_token", "user": {...} }`

### POST /api/auth/register
- **Description**: User registration
- **Body**: `{ "name": "User Name", "email": "user@example.com", "password": "password" }`
- **Response**: `{ "message": "User created successfully" }`

## Groups Endpoints

### GET /api/groups
- **Description**: List all study groups
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "groups": [...] }`

### POST /api/groups
- **Description**: Create new study group
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{ "name": "Group Name", "subject": "Subject", "description": "..." }`
- **Response**: `{ "group": {...} }`

### POST /api/groups/{id}/join
- **Description**: Join a study group
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "message": "Joined group successfully" }`

## Materials Endpoints

### GET /api/materials
- **Description**: List study materials
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "materials": [...] }`

### POST /api/materials
- **Description**: Upload study material
- **Headers**: `Authorization: Bearer <token>`
- **Body**: Form data with file upload
- **Response**: `{ "material": {...} }`

## AI Assistant Endpoints

### POST /api/ai/ask
- **Description**: Ask question to AI assistant
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{ "question": "What is...?" }`
- **Response**: `{ "answer": "AI response..." }`