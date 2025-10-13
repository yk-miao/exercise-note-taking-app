# Lab 2 Writeup: Database Refactoring and Vercel Deployment

## Overview

This document outlines the complete process of refactoring a Flask note-taking application from SQLite to PostgreSQL (Supabase) and deploying it to Vercel. The refactoring was necessary because Vercel's serverless environment cannot reliably write to or read from local database files.

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Solution Architecture](#solution-architecture)
3. [Database Refactoring Steps](#database-refactoring-steps)
4. [Supabase Setup](#supabase-setup)
5. [Local Testing](#local-testing)
6. [Vercel Deployment](#vercel-deployment)
7. [Troubleshooting](#troubleshooting)
8. [Final Verification](#final-verification)

## Problem Statement

The original application used SQLite with a local database file (`database/app.db`), which works fine for local development but fails in serverless environments like Vercel because:

- Serverless functions are stateless and ephemeral
- File system writes are not persistent between function invocations
- Local file paths are not reliable in cloud environments

## Solution Architecture

We refactored the application to use PostgreSQL hosted on Supabase, which provides:

- Persistent cloud-hosted database
- Connection pooling for serverless environments
- SSL encryption for secure connections
- Automatic backups and scaling

## Database Refactoring Steps

### 1. Update Database Configuration (`src/main.py`)

**Before:**
```python
# configure database to use repository-root `database/app.db`
ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(ROOT_DIR, 'database', 'app.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
```

**After:**
```python
# Database configuration
# Prefer DATABASE_URL (e.g., Supabase Postgres) with normalization and sensible engine options.
ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(ROOT_DIR, 'database', 'app.db')

database_url = os.environ.get('DATABASE_URL')

def normalize_database_url(url: str) -> str:
    # Convert postgres:// and postgresql:// to postgresql+psycopg:// for SQLAlchemy 2
    if url.startswith('postgres://'):
        url = 'postgresql+psycopg://' + url[len('postgres://'):]
    elif url.startswith('postgresql://'):
        url = 'postgresql+psycopg://' + url[len('postgresql://'):]
    # Ensure sslmode=require for hosted Postgres if not explicitly set
    if url.startswith('postgresql+psycopg://') and 'sslmode=' not in url:
        separator = '&' if '?' in url else '?'
        url = f"{url}{separator}sslmode=require"
    return url

if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = normalize_database_url(database_url)
else:
    # Local fallback to SQLite in repo database/app.db
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_size': 5,
    'max_overflow': 10,
}
```

### 2. Add PostgreSQL Driver (`requirements.txt`)

Added the PostgreSQL driver:
```
psycopg[binary]==3.2.3
```

### 3. Update Documentation (`README.md`)

Added comprehensive documentation for:
- Database configuration options
- Supabase setup instructions
- Vercel deployment steps
- Environment variable requirements

## Supabase Setup

### 1. Create Supabase Project

1. Go to [Supabase](https://supabase.com)
2. Create a new project
3. Wait for the project to be provisioned

### 2. Get Connection String

1. Navigate to **Project Settings** → **Database**
2. Scroll down to **Connection string**
3. Select **psql** or **pooled** connection string
4. Copy the connection string (format: `postgres://USER:PASSWORD@HOST:PORT/DATABASE`)

### 3. Test Connection

Test the connection using `psql`:
```bash
psql "postgresql://postgres.<project-ref>:<password>@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require" -c "select now();"
```

## Local Testing

### 1. Set Environment Variables

```bash
export DATABASE_URL="postgresql://postgres.<project-ref>:<password>@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require"
export SECRET_KEY="something-random"
```

### 2. Install Dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Application

```bash
python src/main.py
```

### 4. Test API Endpoints

Create a note:
```bash
curl -X POST http://localhost:5001/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Hello","content":"From Supabase"}'
```

List notes:
```bash
curl http://localhost:5001/api/notes
```

### 5. Verify in Supabase

1. Go to Supabase Dashboard
2. Navigate to **Table Editor**
3. Check the `note` table for your test data

## Vercel Deployment

### 1. Prepare for Deployment

Ensure all changes are committed:
```bash
git add .
git commit -m "Refactor database to use PostgreSQL with Supabase"
git push
```

### 2. Configure Vercel Environment Variables

1. Go to Vercel Dashboard
2. Select your project
3. Navigate to **Settings** → **Environment Variables**
4. Add the following variables:

   - **Name**: `DATABASE_URL`
   - **Value**: Your Supabase connection string
   
   - **Name**: `SECRET_KEY`
   - **Value**: A random secret string

### 3. Deploy

1. Push changes to trigger automatic deployment, or
2. Manually trigger deployment from Vercel Dashboard

### 4. Disable Deployment Protection (if needed)

If you encounter authentication errors:
1. Go to **Settings** → **Deployment Protection**
2. Disable protection for Production environment
3. Redeploy

## Troubleshooting

### Common Issues and Solutions

#### 1. DNS Resolution Error
**Error**: `could not translate host name "db.hbktagimjbpobdlhhfkw.supabase.co" to address`

**Solution**:
- Check if you're using VPN/Proxy
- Try different network
- Flush DNS cache: `sudo dscacheutil -flushcache`

#### 2. Module Not Found Error
**Error**: `ModuleNotFoundError: No module named 'psycopg2'`

**Solution**:
- Ensure `psycopg[binary]==3.2.3` is in `requirements.txt`
- Reinstall dependencies: `pip install -r requirements.txt --upgrade`
- Verify URL normalization converts to `postgresql+psycopg://`

#### 3. Authentication Error
**Error**: `FATAL: Tenant or user not found`

**Solution**:
- Verify connection string format
- Ensure username includes project reference: `postgres.<project-ref>`
- Check password for special characters (keep URL quoted)

#### 4. Vercel Function Errors
**Error**: `FUNCTION_INVOCATION_FAILED`

**Solution**:
- Verify environment variables are set in Vercel
- Check function logs in Vercel Dashboard
- Ensure `requirements.txt` includes all dependencies

## Final Verification

### 1. Test Deployed API

Create a note via deployed API:
```bash
curl -X POST https://your-vercel-domain.vercel.app/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Test from Vercel","content":"This note was created via the deployed API"}'
```

List notes:
```bash
curl https://your-vercel-domain.vercel.app/api/notes
```

### 2. Verify Data Persistence

1. Create notes via the deployed API
2. Check Supabase Table Editor to confirm data is stored
3. Restart the application and verify data persists

## Key Benefits Achieved

1. **Cloud-Native**: Application now works in serverless environments
2. **Scalable**: PostgreSQL can handle concurrent users and large datasets
3. **Reliable**: Data persistence with automatic backups
4. **Secure**: SSL encryption for all database connections
5. **Flexible**: Works both locally (SQLite fallback) and in production (PostgreSQL)

## Conclusion

The refactoring successfully transformed the application from a local SQLite-based system to a cloud-native PostgreSQL solution. The application now:

- Works seamlessly on Vercel's serverless platform
- Maintains backward compatibility with local SQLite development
- Provides robust data persistence and scalability
- Includes comprehensive error handling and connection management

The deployment is now production-ready and can handle real-world usage patterns.
