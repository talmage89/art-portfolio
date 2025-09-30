import logging
import time
from django.db import connection
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("db_queries")


class DatabaseQueryLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log database query timing for performance analysis.
    Logs each query with start time, execution time, and SQL statement.
    """

    def process_request(self, request):
        # Reset query count for this request
        self.start_time = time.perf_counter()
        self.initial_queries = len(connection.queries)
        logger.info(
            f"REQUEST_START path={request.path} method={request.method} "
            f"query_count={self.initial_queries} timestamp={self.start_time:.6f}"
        )

    def process_response(self, request, response):
        # Log final query statistics
        end_time = time.perf_counter()
        total_time = end_time - self.start_time
        final_queries = len(connection.queries)
        query_count = final_queries - self.initial_queries

        # Calculate total database time
        db_time = 0
        if hasattr(connection, "queries") and connection.queries:
            # Get queries from this request only
            request_queries = connection.queries[self.initial_queries :]
            for query in request_queries:
                query_time = float(query.get("time", 0))
                db_time += query_time

                # Log individual query details
                logger.info(
                    f"DB_QUERY sql=\"{query['sql'][:200]}{'...' if len(query['sql']) > 200 else ''}\" "
                    f"time={query_time:.6f}s"
                )

        logger.info(
            f"REQUEST_END path={request.path} method={request.method} "
            f"status={response.status_code} total_time={total_time:.6f}s "
            f"db_time={db_time:.6f}s query_count={query_count} "
            f"db_percentage={((db_time/total_time)*100) if total_time > 0 else 0:.1f}%"
        )

        return response

    def process_exception(self, request, exception):
        # Log exceptions with timing data
        if hasattr(self, "start_time"):
            end_time = time.perf_counter()
            total_time = end_time - self.start_time
            logger.error(
                f"REQUEST_EXCEPTION path={request.path} method={request.method} "
                f"exception={exception.__class__.__name__} total_time={total_time:.6f}s"
            )
