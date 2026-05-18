# Travel Planner API

A lightweight RESTful API built with FastAPI to help travelers plan trips, manage projects, and save places validated by the Art Institute of Chicago API.

## Features
- **Projects CRUD**: Manage travel projects (Name, Description, Start Date).
- **Places Integration**: Add and validate places using external IDs from the Art Institute of Chicago API.
- **Business Logic**: Limits of 10 places per project, duplicate prevention, and automatic project completion status.
- **Docker Support**: Ready for containerized deployment.

## Tech Stack
- FastAPI, SQLAlchemy, SQLite, Pydantic, Requests, Docker & Docker Compose.

## Quick Start

### Option 1: Run via Docker (Recommended)
```bash
docker-compose up --build
```
The API will be available at `http://localhost:8000`.

### Option 2: Run Locally
1. Clone the repository and navigate to the project directory.
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Start the server:
```bash
uvicorn main:app --reload
```

## API Documentation
Once the application is running, open the interactive Swagger UI documentation at:
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

*Note for testing endpoints:* Use valid external IDs like `129884` or `27992` to add places successfully.