"""Gunicorn configuration file for CycleInvoice.

This configuration file is used to configure gunicorn for production deployment.
It addresses the worker timeout issue by setting appropriate timeout values and
worker configurations.
"""

import os

# Server socket
bind = "0.0.0.0:8000"

# Worker processes
# Use 2-4 workers per core as a general rule
# For a typical container with 1-2 cores, 2-4 workers is reasonable
workers = int(os.getenv("GUNICORN_WORKERS", "2"))

# Worker class
worker_class = "sync"

# Timeout configuration
# Increased from default 30s to 120s to handle slow startup and requests
# This is especially important during initial app loading with Django
timeout = int(os.getenv("GUNICORN_TIMEOUT", "120"))

# Graceful timeout for worker shutdown
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", "30"))

# Keep-alive connections
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", "5"))

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")

# Process naming
proc_name = "cycleinvoice"

# Preload app for better memory efficiency
# This loads the application code before worker processes are forked
preload_app = True

# Worker restart configuration
# Restart workers after this many requests to prevent memory leaks
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", "1000"))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", "50"))
