"""Database migration script

This script handles the migration of data from SQLite to PostgreSQL.
"""
from flask import Flask
from flask_migrate import Migrate
from src.models.user import db
import os

def init_migrations(app):
    """Initialize database migrations"""
    migrate = Migrate(app, db)
    return migrate

def setup_database(app):
    """Set up the database and migrations"""
    # Initialize SQLAlchemy
    db.init_app(app)
    
    # Initialize migrations
    migrate = init_migrations(app)
    
    return db, migrate