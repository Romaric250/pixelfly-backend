# Gunicorn configuration file for PixelFly Backend - Render Optimized
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"
backlog = 2048

# Worker processes (optimized for Render's resource limits)
workers = min(multiprocessing.cpu_count(), int(os.getenv('MAX_WORKERS', '2')))
worker_class = "sync"
worker_connections = 1000
timeout = int(os.getenv('WORKER_TIMEOUT', '60'))  # Increased for image processing
keepalive = int(os.getenv('KEEP_ALIVE', '2'))

# Restart workers after this many requests, to help prevent memory leaks
max_requests = int(os.getenv('MAX_REQUESTS', '500'))
max_requests_jitter = int(os.getenv('MAX_REQUESTS_JITTER', '50'))

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = os.getenv('LOG_LEVEL', 'info').lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "pixelfly-backend"

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = "/tmp/uploads"

# Environment variables
raw_env = [
    'PYTHONPATH=.',
    f'FLASK_ENV={os.getenv("FLASK_ENV", "production")}',
]

# Preload application for better performance
preload_app = True

# Memory management (Render optimized)
max_requests = int(os.getenv('MAX_REQUESTS', '300'))  # Lower for memory efficiency
max_requests_jitter = int(os.getenv('MAX_REQUESTS_JITTER', '30'))

# Graceful timeout
graceful_timeout = 30

# Enable threading for better I/O handling
threads = 2

# Callback functions for monitoring
def when_ready(server):
    server.log.info("🚀 PixelFly Backend Server is ready on Render. Listening on %s", server.address)
    server.log.info("🔧 Workers: %d, Timeout: %ds, Environment: %s",
                    workers, timeout, os.getenv('FLASK_ENV', 'production'))

def worker_int(worker):
    worker.log.info("🔄 Worker %s received INT or QUIT signal", worker.pid)

def pre_fork(server, worker):
    server.log.info("👷 Forking worker %s", worker.pid)

def post_fork(server, worker):
    server.log.info("✅ Worker %s spawned successfully", worker.pid)

def post_worker_init(worker):
    worker.log.info("🎯 Worker %s initialized and ready", worker.pid)

def worker_abort(worker):
    worker.log.error("❌ Worker %s received SIGABRT signal", worker.pid)

def on_exit(server):
    server.log.info("🛑 PixelFly Backend Server shutting down")

def on_reload(server):
    server.log.info("🔄 PixelFly Backend Server reloading")
