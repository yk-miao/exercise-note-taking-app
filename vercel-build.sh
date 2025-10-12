#!/bin/bash
python -m pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
python << END
from src.main import app, db
with app.app_context():
    db.create_all()
END