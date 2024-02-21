## Cyberpunk Inventory API

### Overview

Cyberpunk Inventory API is a FastAPI application designed to manage an inventory system, including users, items, and their respective CRUD operations.

### Features

* User Management: Create, read, update, and delete users.
* Item Management: Add, list, update, and delete inventory items.
* Authentication and Authorization: Secure endpoints with JWT tokens.
* Database Integration: PostgreSQL for storing user and inventory data.
* Docker Deployment: Easily set up the environment and deploy using Docker.

### Prerequisites

Before you begin, ensure you have installed the following:

* Python 3.8+
* Docker and Docker Compose
* PostgreSQL (for local development without Docker)

### Installation

Clone the repository to your local machine:

> * git clone https://github.com/OlegAlyeynikov/cyberpunk_inventory_fastapi.git
> * cd cyberpunk-inventory

### Setting Up the Environment

* Initialize environment variables .env as you can see in the .env_example file

#### Using Docker (Recommended)

1. Build and run the Docker containers:

> * docker-compose build
> * docker-compose up

This commands builds the Docker images and runs the containers in the background.

2. Apply database migrations:

> * docker-compose exec web alembic upgrade head

This command runs Alembic migrations to set up your database schema.

3. Create a superuser:

> * docker-compose exec web python inventory_api/create_superuser.py

Create a superuser account.

#### Without Docker

1. Set up a virtual environment:

> * python3 -m venv venv
> * source venv/bin/activate

On Windows use: 

> * venv\Scripts\activate

2. Install dependencies:

> * pip install -r requirements.txt

3. Apply database migrations:

> * alembic upgrade head

4. Run the application:

> * uvicorn inventory_api.main:app --reload

### Testing Endpoints

The API documentation is available at http://localhost:8000/docs once the application is running. Here, you can test all available endpoints directly from your browser.

### Running Tests

To run automated tests, execute:

> * docker-compose exec web pytest

Or, if not using Docker:

> * pytest

### Contributing

Contributions are welcome! Please feel free to submit a pull request.