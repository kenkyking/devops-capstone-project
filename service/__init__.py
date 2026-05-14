from flask import Flask
from flask_cors import CORS


def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__)

    CORS(app)

    @app.after_request
    def set_security_headers(response):
        """Set security headers"""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response

    return app
