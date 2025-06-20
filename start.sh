#!/bin/bash

# PixelFly Backend Startup Script for Render
# This script prepares the environment and starts the Flask application

set -e  # Exit on any error

echo "🚀 Starting PixelFly Backend on Render..."

# Set default environment variables if not provided
export FLASK_ENV=${FLASK_ENV:-production}
export PORT=${PORT:-10000}
export PYTHONPATH=${PYTHONPATH:-"."}

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p /tmp/uploads
mkdir -p /opt/render/project/data

# Set permissions
chmod 755 /tmp/uploads

# Verify Python version
echo "🐍 Python version:"
python --version

# Verify pip and install dependencies if needed
echo "📦 Verifying dependencies..."
pip list | grep -E "(Flask|gunicorn|Pillow)" || echo "⚠️ Some dependencies may be missing"

# Check if critical environment variables are set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️ WARNING: GOOGLE_API_KEY is not set. AI features will be limited."
fi

# Run database migrations if needed (future use)
# echo "🗄️ Running database migrations..."
# python -c "from app import app; print('Database check complete')" || echo "⚠️ Database check failed"

# Start the application with Gunicorn
echo "🚀 Starting Gunicorn server..."
echo "📍 Listening on 0.0.0.0:${PORT}"
echo "🔧 Environment: ${FLASK_ENV}"

exec gunicorn \
    --config gunicorn.conf.py \
    --bind 0.0.0.0:${PORT} \
    --workers ${MAX_WORKERS:-2} \
    --timeout ${WORKER_TIMEOUT:-60} \
    --keep-alive ${KEEP_ALIVE:-2} \
    --max-requests ${MAX_REQUESTS:-500} \
    --max-requests-jitter ${MAX_REQUESTS_JITTER:-50} \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    wsgi:application
