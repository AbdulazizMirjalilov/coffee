# Knowledge Management Platform

## Overview

## Features

- Integration with Redis for caching and Celery for asynchronous task processing
- Automatic database migrations with Alembic
- Pre-commit hooks to ensure code quality and consistency

## Installation

### Step 1: Clone the Repository

```bash
git clone https://gitlab.com/knowledge-management-platform1/backend/be-template.git
cd be-template
```

### Step 2: Install Dependencies

```bash
poetry install
```

### Step 3: Set Up Environment Variables

Create a `.env` file in the src folder of the project and set the environment variables:

```bash
mv .env.example .env
```

### Step 4: Run Migrations

Make sure you have Alembic configured, then run:

```bash
poetry run alembic upgrade head
```

### Step 5: Start the Services

You can run the application using Docker Compose:

```bash
docker-compose up -d --build
```

Alternatively, if you're not using Docker, start the services manually:

```bash
poetry run uvicorn app.main:app --reload
```

## Running Tests

To run the tests:

```bash
poetry run pytest
```

## Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. Install the pre-commit hooks by running:

```bash
poetry run pre-commit install
```

Then, before committing changes, the pre-commit hooks will automatically run.

## Useful commands

Create a new migration (when you modify the models):

```bash
poetry run alembic revision --autogenerate -m "description of the changes"
```

Apply migrations (update the database schema):

```bash
poetry run alembic upgrade head
```

Downgrade the database (if you need to revert changes):

```bash
poetry run alembic downgrade -1
```

Show current migration status:

```bash
poetry run alembic current
```

Show the migration history:

```bash
poetry run alembic history
```
