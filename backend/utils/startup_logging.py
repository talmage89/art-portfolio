import logging
import time
import os
from django.db import connection
from django.core.management.color import no_style
from django.db.utils import IntegrityError

logger = logging.getLogger("startup")


class StartupTimer:
    """
    Utility class to track and log application startup times.
    Helps identify bottlenecks in container cold starts.
    """

    def __init__(self):
        self.start_time = time.perf_counter()
        self.checkpoints = {}

    def checkpoint(self, name: str, extra_info: str = ""):
        """Record a checkpoint with timing information."""
        current_time = time.perf_counter()
        elapsed = current_time - self.start_time

        # Calculate time since last checkpoint
        last_checkpoint_time = 0
        if self.checkpoints:
            last_checkpoint_time = max(
                cp["elapsed"] for cp in self.checkpoints.values()
            )
        since_last = elapsed - last_checkpoint_time

        self.checkpoints[name] = {
            "elapsed": elapsed,
            "since_last": since_last,
            "extra_info": extra_info,
        }

        logger.info(
            f"STARTUP_CHECKPOINT name={name} elapsed={elapsed:.6f}s "
            f"since_last={since_last:.6f}s {extra_info}"
        )

    def test_database_connection(self):
        """Test database connectivity and log timing."""
        try:
            db_start = time.perf_counter()

            # Test basic connectivity
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()

            db_connect_time = time.perf_counter() - db_start

            # Test a simple query to artwork table (if it exists)
            query_start = time.perf_counter()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM artwork_artwork LIMIT 1")
                    count = cursor.fetchone()[0]
                query_time = time.perf_counter() - query_start

                self.checkpoint(
                    "database_ready",
                    f"connect_time={db_connect_time:.6f}s query_time={query_time:.6f}s artwork_count={count}",
                )
            except Exception as e:
                # Table might not exist yet, just log basic connection
                self.checkpoint(
                    "database_connected",
                    f"connect_time={db_connect_time:.6f}s error={str(e)[:100]}",
                )

        except Exception as e:
            db_error_time = time.perf_counter() - db_start
            self.checkpoint(
                "database_error",
                f"error_time={db_error_time:.6f}s error={str(e)[:100]}",
            )

    def log_environment_info(self):
        """Log relevant environment information for debugging."""
        env_info = {
            "DATABASE_URL": bool(os.getenv("DATABASE_URL")),
            "DJANGO_SETTINGS_MODULE": os.getenv("DJANGO_SETTINGS_MODULE", "not_set"),
            "DEBUG": os.getenv("DEBUG", "not_set"),
            "PORT": os.getenv("PORT", "not_set"),
        }

        env_str = " ".join([f"{k}={v}" for k, v in env_info.items()])
        self.checkpoint("environment_loaded", env_str)

    def final_report(self):
        """Log final startup summary."""
        total_time = time.perf_counter() - self.start_time
        checkpoint_count = len(self.checkpoints)

        logger.info(
            f"STARTUP_COMPLETE total_time={total_time:.6f}s "
            f"checkpoints={checkpoint_count}"
        )

        # Log detailed breakdown
        for name, data in self.checkpoints.items():
            logger.info(
                f"STARTUP_BREAKDOWN name={name} elapsed={data['elapsed']:.6f}s "
                f"since_last={data['since_last']:.6f}s {data['extra_info']}"
            )


# Global startup timer instance
startup_timer = StartupTimer()
