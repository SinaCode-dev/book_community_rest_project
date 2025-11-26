# BookCommunity - Full-Featured Django REST Framework Backend (Educational Project)

A complete Goodreads-like book review and personal library platform built from scratch as an **advanced educational backend project** using Django REST Framework.

The goal of this project is to demonstrate mastery of real-world backend development concepts with Django.

## Features Implemented (100% from scratch)

- User registration & login with **JWT** (access + refresh tokens)
- Submit Comment for books
- Personal library management (Currently Reading, Read, Want to Read)
- Advanced book search & filtering
- Fully protected endpoints (`IsAuthenticated`, custom `IsOwner` permissions)
- Clean project structure (separate apps, serializers, viewsets, routers)
- Ready for PostgreSQL (SQLite used in development for simplicity)

## Tech Stack

- Django + Django REST Framework
- JWT Authentication (`djangorestframework-simplejwt` + `djoser`)
- Django Filter + Search
- RESTful design following industry best practices

## Quick Start

```bash
git clone https://github.com/SinaCode-dev/book_community_rest_project.git
cd book_community_rest_project

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Run migrations & create superuser
python manage.py migrate
python manage.py createsuperuser

# Start server
python manage.py runserver
