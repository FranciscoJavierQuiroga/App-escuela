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
- Vercel CLI (para despliegue)

### Desarrollo Local

#### Backend Setup
1. Navigate to the backend directory
2. Run `docker-compose up -d` to start the backend and database

#### Frontend Setup
1. Navigate to the frontend directory
2. Run `npm install` to install dependencies
3. Run `npm start` to start the development server

### Despliegue en Vercel

#### Requisitos Previos
- Cuenta en [Vercel](https://vercel.com)
- [Vercel CLI](https://vercel.com/cli) instalado
- [GitHub](https://github.com) o [GitLab](https://gitlab.com) para alojar el código

#### Pasos para el Despliegue

1. **Preparación del Repositorio**
   - Sube tu código a un repositorio Git (GitHub, GitLab, etc.)

2. **Despliegue del Frontend**
   - Accede a tu cuenta de Vercel
   - Selecciona "Import Project" y elige tu repositorio
   - Configura el proyecto:
     - Framework Preset: React
     - Root Directory: `/frontend`
     - Build Command: `npm run build`
     - Output Directory: `build`
   - En la sección de Variables de Entorno, configura:
     - `REACT_APP_API_URL`: URL de tu backend (por ej. https://tu-app-backend.vercel.app/api)

3. **Despliegue del Backend**
   - Desde la interfaz de Vercel:
     - Importa nuevamente el mismo repositorio
     - Configura como:
       - Framework Preset: Other
       - Root Directory: `/`
       - Build Command: (dejar vacío)
       - Output Directory: (dejar vacío)
   - En la sección de Variables de Entorno, configura todas las variables mencionadas en el archivo `.env.example`
   - Para la base de datos, es recomendable utilizar un servicio gestionado como:
     - [Supabase](https://supabase.com)
     - [Neon](https://neon.tech)
     - [Railway](https://railway.app)
     - [ElephantSQL](https://www.elephantsql.com)

4. **Configuración de Dominios Personalizados (Opcional)**
   - En la configuración del proyecto en Vercel, puedes añadir dominios personalizados tanto para el frontend como para el backend.

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
