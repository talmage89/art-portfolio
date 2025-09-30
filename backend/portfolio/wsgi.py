"""
WSGI config for portfolio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
import time

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.core.wsgi import get_wsgi_application

# Initialize startup logging
wsgi_start_time = time.perf_counter()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio.settings.production")

# Import startup timer after Django settings are configured
try:
    from utils.startup_logging import startup_timer

    startup_timer.checkpoint(
        "wsgi_init", f"wsgi_elapsed={time.perf_counter() - wsgi_start_time:.6f}s"
    )
    startup_timer.log_environment_info()

    # Get the Django application
    app_start = time.perf_counter()
    application = get_wsgi_application()
    app_time = time.perf_counter() - app_start

    startup_timer.checkpoint("django_app_ready", f"app_init_time={app_time:.6f}s")
    startup_timer.test_database_connection()
    startup_timer.final_report()

except Exception as e:
    # Fallback if startup logging fails
    print(f"STARTUP_ERROR: Failed to initialize startup logging: {e}")
    application = get_wsgi_application()
