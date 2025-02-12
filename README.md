# FastAPI Project

This is a FastAPI project that demonstrates how to build a RESTful API using FastAPI. The project includes a basic structure for organizing your code, along with instructions for running the application locally or in a Docker container.

## Project Structure

```bash
fastapi-project/
├── app/
│   ├── __init__.py
│   ├── main.py              # Main FastAPI application
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   └── v1/              # Versioned API endpoints
│   │       ├── __init__.py
│   │       ├── endpoints/   # Endpoint definitions
│   │       └── models.py    # Pydantic models
│   ├── core/                # Core application logic
│   │   ├── __init__.py
│   │   └── config.py        # Configuration settings
│   └── db/                  # Database-related files
│       ├── __init__.py
│       └── session.py       # Database session management
├── tests/                   # Unit and integration tests
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yaml       # Docker Compose configuration
├── .env                     # Environment variables
└── README.md                # Project documentation
```

## Features

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **SQLAlchemy**: ORM for database interactions.
- **Docker**: Containerization for easy deployment and development.
- **Testing**: Includes unit and integration tests.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.7+
- Docker (optional, for containerized deployment)
- Docker Compose (optional, for multi-container setup)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/fastapi-project.git
cd fastapi-project
```

### 2. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory and add the following variables:

```bash
DATABASE_URL=sqlite:///./test.db
DEBUG=True
```

### 4. Run the Application

Start the FastAPI app using `uvicorn`:

```bash
uvicorn app.main:app --reload
```

The app will be available at <http://localhost:8000>.

## Running with Docker

### 1. Build the Docker Image

```bash
docker build -t fastapi-app .
```

### 2. Run the Docker Container

```bash
docker run -d -p 8000:8000 --name my-fastapi-app fastapi-app
```

### 3. Using Docker Compose

Run the app and database (if applicable) using Docker Compose:

```bash
docker-compose up
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

## Testing

Run the tests using `pytest`:

```bash
# Install dev dependencies in virtual environment
pip install -r requirements-dev.txt

pytest tests/
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/YourFeatureName).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/latest/)
