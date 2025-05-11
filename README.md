# School Management System

This project is a full-stack application for managing school-related operations.

## Project Structure

```
├── backend/                  # FastAPI backend
│   ├── app/                  # Main application
│   │   ├── auth/             # Authentication
│   │   ├── database/         # Database connections
│   │   ├── models/           # SQLModel models
│   │   ├── routers/          # API routes
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── scripts/          # Utility scripts
│   │   ├── services/         # Business logic services
│   │   ├── tests/            # Unit and integration tests
│   │   └── utils/            # Utilities
│   ├── db_init.py            # Database initialization
│   ├── docker-compose.yml    # Docker compose config
│   ├── Dockerfile            # Docker build config
│   └── requirements.txt      # Python dependencies
├── frontend/                 # React frontend
│   ├── public/               # Static files
│   └── src/                  # React source code
│       ├── components/       # Reusable components
│       ├── context/          # React contexts
│       ├── hooks/            # Custom hooks
│       ├── pages/            # Page components
│       ├── services/         # API services
│       ├── types/            # TypeScript definitions
│       └── utils/            # Utility functions
└── docs/                     # Documentation
```

## Technologies Used

### Backend
- FastAPI (Python)
- SQLModel (ORM)
- PostgreSQL (Database)
- JWT Authentication
- Docker & Docker Compose

### Frontend
- React (with TypeScript)
- Material-UI
- React Router
- Axios

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js and npm/yarn

### Backend Setup
1. Navigate to the backend directory
2. Run `docker-compose up -d` to start the backend and database

### Frontend Setup
1. Navigate to the frontend directory
2. Run `npm install` to install dependencies
3. Run `npm start` to start the development server

## Features

- User authentication and role-based access control
- Student management
- Teacher management
- Course management
- Enrollment management
- Grade management
- Report generation

## Demo Accounts

- Admin: admin@school.com / adminpassword
- Teacher: teacher@school.com / teacherpassword
- Student: student@school.com / studentpassword
