from flask import Flask
from config import PORT
from database import init_db
from routes_api import api_bp
from routes_ui import ui_bp

app = Flask(__name__)

# Initialize Database
init_db(app)

# Register Blueprints
app.register_blueprint(ui_bp)
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    print(f"Starting Web App on http://localhost:{PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True)
