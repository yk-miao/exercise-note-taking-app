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
- Updated route parameters to use UUID type

### 3. Route Updates
```python
# Updated all note routes to use UUID parameters:
@note_bp.route('/notes/<uuid:note_id>', methods=['GET'])
@note_bp.route('/notes/<uuid:note_id>', methods=['PUT'])
@note_bp.route('/notes/<uuid:note_id>', methods=['DELETE'])
@note_bp.route('/notes/<uuid:note_id>/translate', methods=['POST'])
```

### 4. Model Changes
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

## Vercel Deployment Configuration

### 1. Environment Setup
The following environment variables need to be configured in Vercel:
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: API key for OpenAI services
- `VERCEL_ENV`: Set to 'production' for production environment

### 2. Project Structure Updates
- Added `vercel.json` for deployment configuration
- Updated app structure for serverless deployment
- Added health check endpoint at `/api/healthcheck`
- Modified database configuration for Vercel's environment

### 3. Key Files
```json
// vercel.json
{
    "version": 2,
    "builds": [
        {
            "src": "src/main.py",
            "use": "@vercel/python"
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "src/main.py"
        }
    ],
    "env": {
        "PYTHONPATH": "src"
    }
}
```

### 4. Deployment Steps
1. Install Vercel CLI: `npm install -g vercel`
2. Link project: `vercel link`
3. Set up environment variables in Vercel dashboard
4. Deploy: `vercel --prod`

### 5. Database Configuration
- Updated to handle Vercel's PostgreSQL connection string format
- Implemented connection pooling for better performance
- Added automatic database reconnection handling