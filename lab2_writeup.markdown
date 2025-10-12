# Lab 2: Database Migration - SQLite to PostgreSQL

## Overview
Migrated the note-taking application's database from SQLite to PostgreSQL for better scalability and performance.

## Key Changes

### 1. Database Setup
- Installed PostgreSQL via Homebrew
- Created development database: `notetaker_dev`
- Created test database: `notetaker_test`

### 2. Code Updates
- Added PostgreSQL dependencies
- Updated database models with UUIDs
- Implemented user-note relationships
- Added connection pooling
- Set up database migrations

### 3. Model Changes
```python
# Updated User and Note models with:
- UUID primary keys
- Proper relationships
- Timestamp fields
- Better data types
```

### 4. Environment Setup
```bash
# PostgreSQL connection settings
DATABASE_URL=postgresql://localhost/notetaker_dev
FLASK_ENV=development
```

## Migration Steps
```bash
# Initialize and run migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```