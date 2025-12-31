# Bookly API

A production-ready FastAPI REST API for managing book data with PostgreSQL database.

## Features

- ✅ Full CRUD operations (Create, Read, Update, Delete) for books
- ✅ PostgreSQL database with async SQLAlchemy/SQLModel
- ✅ Comprehensive input validation using Pydantic
- ✅ Proper error handling and logging
- ✅ Automatic API documentation (Swagger UI and ReDoc)
- ✅ Type-safe code with proper type hints
- ✅ Production-ready architecture with service layer pattern
- ✅ Database connection pooling
- ✅ Comprehensive code documentation

## Project Structure

```
bookly/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── README.md              # This file
└── src/
    ├── __init__.py        # FastAPI app instance and configuration
    ├── config.py          # Application configuration and settings
    └── books/
        ├── __init__.py
        ├── models.py      # SQLModel database models
        ├── schemas.py     # Pydantic request/response schemas
        ├── service.py     # Business logic layer
        └── routes.py      # API route handlers
    └── db/
        ├── __init__.py
        └── main.py        # Database configuration and session management
```

## Architecture

The application follows a clean architecture pattern:

1. **Routes** (`routes.py`): Handle HTTP requests/responses, validate input, call services
2. **Services** (`service.py`): Contain business logic and database operations
3. **Models** (`models.py`): Define database table structure using SQLModel
4. **Schemas** (`schemas.py`): Define request/response data structures using Pydantic
5. **Database** (`db/main.py`): Manages database connections and sessions

## Prerequisites

- Python 3.12+
- PostgreSQL 12+
- pip (Python package manager)

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory

2. **Create a virtual environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**:
   ```bash
   # Create a new database
   createdb bookly_db
   
   # Or using psql:
   psql -U postgres
   CREATE DATABASE bookly_db;
   ```

5. **Configure environment variables**:
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/bookly_db
   APP_NAME=Bookly API
   APP_VERSION=1.0.0
   DB_POOL_SIZE=5
   DB_MAX_OVERFLOW=10
   DB_ECHO=False
   API_V1_PREFIX=/api/v1
   ```

   Replace `postgres`, `password`, `localhost`, `5432`, and `bookly_db` with your actual database credentials.

## Running the Application

### Development Mode

Run the application using the main entry point:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn src:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Production Mode

For production, use a proper ASGI server with multiple workers:

```bash
uvicorn src:app --host 0.0.0.0 --port 8000 --workers 4
```

Or use a process manager like systemd, supervisor, or Docker.

## API Endpoints

### Books

- `GET /api/v1/books` - Get all books (with pagination)
- `GET /api/v1/books/{book_uid}` - Get a specific book by UUID
- `POST /api/v1/books` - Create a new book
- `PUT /api/v1/books/{book_uid}` - Update a book (partial update)
- `DELETE /api/v1/books/{book_uid}` - Delete a book

### Health Check

- `GET /health` - Check API health status

## API Usage Examples

### Create a Book

```bash
curl -X POST "http://localhost:8000/api/v1/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Alchemist",
    "author": "Paulo Coelho",
    "publication": "HarperCollins",
    "price": 399.99
  }'
```

### Get All Books

```bash
curl "http://localhost:8000/api/v1/books?skip=0&limit=10"
```

### Get a Specific Book

```bash
curl "http://localhost:8000/api/v1/books/{book_uid}"
```

### Update a Book

```bash
curl -X PUT "http://localhost:8000/api/v1/books/{book_uid}" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 449.99
  }'
```

### Delete a Book

```bash
curl -X DELETE "http://localhost:8000/api/v1/books/{book_uid}"
```

## Database Schema

The `Book` table has the following structure:

- `uid` (UUID, Primary Key): Unique identifier
- `title` (String, Indexed): Book title
- `author` (String, Indexed): Author name
- `publication` (String): Publication house
- `price` (Float): Book price
- `created_at` (Timestamp): Creation timestamp (auto-generated)
- `updated_at` (Timestamp): Last update timestamp (auto-updated)

## Code Documentation

Every file in this project is thoroughly documented with:
- Module-level docstrings explaining the purpose
- Class-level docstrings describing functionality
- Function-level docstrings with parameters and return values
- Inline comments explaining complex logic

## Best Practices Implemented

1. **Separation of Concerns**: Clear separation between routes, services, and data access
2. **Type Safety**: Comprehensive type hints throughout the codebase
3. **Error Handling**: Proper exception handling with meaningful error messages
4. **Validation**: Input validation using Pydantic schemas
5. **Database**: Connection pooling and proper session management
6. **Logging**: Structured logging for debugging and monitoring
7. **Documentation**: Comprehensive code documentation and API docs
8. **Security**: Parameterized queries to prevent SQL injection
9. **Scalability**: Async/await for better performance
10. **Maintainability**: Clean code structure and naming conventions

## Development

### Adding New Features

1. Create database models in `src/books/models.py`
2. Define schemas in `src/books/schemas.py`
3. Implement business logic in `src/books/service.py`
4. Create routes in `src/books/routes.py`
5. Register routes in `src/__init__.py`

### Running Tests

(Add your test framework setup here)

### Code Style

The code follows PEP 8 style guidelines. Consider using:
- `black` for code formatting
- `flake8` or `pylint` for linting
- `mypy` for type checking

## Troubleshooting

### Database Connection Issues

- Verify PostgreSQL is running: `pg_isready`
- Check database credentials in `.env` file
- Ensure database exists: `psql -l`
- Verify network connectivity to database server

### Import Errors

- Ensure virtual environment is activated
- Verify all dependencies are installed: `pip list`
- Check Python path and module structure

## License

(Add your license here)

## Contributing

(Add contribution guidelines here)

