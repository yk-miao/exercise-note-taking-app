import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.note import note_bp
from src.models.note import Note
from src.config import config
from src.migrations import setup_database

def create_app(config_name='default'):
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Load configuration
    app.config.from_object(config[config_name])
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')
    
    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e),
            'environment': os.getenv('VERCEL_ENV', 'development')
        }), 500
    
    # Enable CORS
    CORS(app)
    
    # Set up database and migrations
    db, migrate = setup_database(app)
    
    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(note_bp, url_prefix='/api')
    
    return app

app = create_app('production' if os.getenv('VERCEL_ENV') == 'production' else 'development')

# Error handling for Vercel
@app.errorhandler(500)
def handle_500(e):
    return jsonify({
        'error': 'Internal Server Error',
        'message': str(e),
        'details': getattr(e, 'original_exception', str(e))
    }), 500

try:
    # Initialize database tables
    with app.app_context():
        db.create_all()
except Exception as e:
    print(f"Database initialization error: {str(e)}")

# Health check endpoint for Vercel
@app.route('/api/healthcheck')
def healthcheck():
    try:
        # Test database connection
        with app.app_context():
            db.engine.connect()
            db.create_all()
        return jsonify({
            "status": "healthy",
            "environment": os.getenv('VERCEL_ENV', 'development'),
            "database": "connected"
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "environment": os.getenv('VERCEL_ENV', 'development')
        }), 500
@app.route('/api/healthcheck')
def healthcheck():
    return jsonify({"status": "healthy", "environment": os.getenv('VERCEL_ENV', 'development')})

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve(path):
    if path.startswith('api/'):
        return {"error": "Not Found"}, 404
        
    if path in ['favicon.ico', 'favicon.png']:
        return '', 204  # Return empty response for favicon requests
        
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    try:
        if os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            return send_from_directory(static_folder_path, 'index.html')
    except Exception as e:
        print(f"Error serving static file: {str(e)}")
        return "Error serving file", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
