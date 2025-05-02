import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import db instance after loading env vars
from src.models.base import db

# Import blueprints
from src.routes.auth import auth_bp
from src.routes.audience import audience_bp
from src.routes.products import products_bp
from src.routes.reports import reports_bp
from src.routes.insights import insights_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default-fallback-secret-key') # Use env var for secret key

# Enable database functionality
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(audience_bp, url_prefix="/api/audience")
app.register_blueprint(products_bp, url_prefix="/api/products")
app.register_blueprint(reports_bp, url_prefix="/api/reports")
app.register_blueprint(insights_bp, url_prefix="/api/insights")

# Serve static files (React build) - adjust static_folder if needed after frontend build
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # In development, React dev server handles frontend.
    # In production, Flask serves the built React app from 'static' or a configured folder.
    # We will adjust this later to serve the React build output.
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    # Check if the path is an API call first
    if path.startswith('api/'):
        # Let Flask routing handle API calls, return 404 if not found by blueprints
        return "API route not found", 404

    # Serve static files or index.html for frontend routing
    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "Frontend entry point (index.html) not found in static folder.", 404


if __name__ == '__main__':
    # Make sure to run with the virtual environment activated
    # Example: /home/ubuntu/instagram-audience-app/server/venv/bin/python /home/ubuntu/instagram-audience-app/server/src/main.py
    app.run(host='0.0.0.0', port=5000, debug=True)

