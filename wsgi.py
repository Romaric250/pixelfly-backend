#!/usr/bin/env python3
"""
WSGI entry point for PixelFly Backend
Production-ready Flask application for Render deployment
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger(__name__)

# Import the Flask application with fallback strategy
app = None
try:
    # Try to import the main app first
    from app import app
    logger.info("✅ Successfully imported Flask app from app.py")
except ImportError as e:
    logger.warning(f"⚠️ Failed to import from app.py: {e}")
    try:
        # Fallback to simple_server
        from simple_server import app
        logger.info("✅ Successfully imported Flask app from simple_server")
    except ImportError as e2:
        logger.warning(f"⚠️ Failed to import from simple_server: {e2}")
        try:
            # Final fallback to API index
            from api.index import app
            logger.info("✅ Successfully imported Flask app from api.index")
        except ImportError as e3:
            logger.error(f"❌ Failed to import from api.index: {e3}")
            raise ImportError("Could not import Flask app from any module")

# Configure for production
if __name__ != "__main__":
    # Running under WSGI server (Gunicorn/Render)
    logger.info("🚀 Running under WSGI server (production mode)")
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
    app.config['ENV'] = 'production'

    # Render-specific configurations
    app.config['SERVER_NAME'] = None  # Let Render handle this
    app.config['PREFERRED_URL_SCHEME'] = 'https'
else:
    # Running directly (development mode)
    logger.info("🔧 Running in development mode")
    app.config['DEBUG'] = True
    app.config['ENV'] = 'development'

# WSGI application object (required by Render)
application = app

if __name__ == "__main__":
    # This allows running the file directly for testing
    logger.info("🧪 Running Flask app directly (development mode)")
    port = int(os.getenv('PORT', 5001))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
