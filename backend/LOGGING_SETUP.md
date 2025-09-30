# Database Query Timing Logging Setup

This document explains the logging configuration added to help diagnose cold start performance issues between Google Cloud Run and Neon DB.

## What's Been Added

### 1. Database Query Logging Middleware (`utils/db_logging_middleware.py`)

- Logs every HTTP request start and end times
- Tracks individual SQL query execution times
- Calculates total database time vs. total request time
- Shows percentage of request time spent on database queries

### 2. Container Startup Logging (`utils/startup_logging.py`)

- Times Django application initialization
- Tests database connectivity during startup
- Logs environment configuration
- Provides detailed startup breakdown

### 3. Enhanced WSGI Configuration (`portfolio/wsgi.py`)

- Integrates startup timing into the WSGI application
- Logs container initialization phases
- Tests database connection on startup

### 4. Production-Ready Gunicorn Setup (`Dockerfile`)

- Switched from development server to Gunicorn
- Added container start timestamp
- Optimized worker configuration for Cloud Run

## Log Output Examples

### Container Startup Logs

```
CONTAINER_START: 2025-09-30T10:15:30+00:00
INFO 2025-09-30 10:15:30,123 STARTUP_CHECKPOINT name=wsgi_init elapsed=0.001234s since_last=0.001234s wsgi_elapsed=0.001234s
INFO 2025-09-30 10:15:30,456 STARTUP_CHECKPOINT name=environment_loaded elapsed=0.002456s since_last=0.001222s DATABASE_URL=True DJANGO_SETTINGS_MODULE=portfolio.settings.production
INFO 2025-09-30 10:15:30,789 STARTUP_CHECKPOINT name=django_app_ready elapsed=0.005789s since_last=0.003333s app_init_time=0.003000s
INFO 2025-09-30 10:15:31,234 STARTUP_CHECKPOINT name=database_ready elapsed=0.008234s since_last=0.002445s connect_time=0.120000s query_time=0.045000s artwork_count=25
INFO 2025-09-30 10:15:31,234 STARTUP_COMPLETE total_time=0.008234s checkpoints=4
```

### Request and Query Logs

```
INFO 2025-09-30 10:15:35,123 REQUEST_START path=/api/artworks/ method=GET query_count=0 timestamp=1234567890.123456
INFO 2025-09-30 10:15:35,145 DB_QUERY sql="SELECT * FROM artwork_artwork WHERE status = 'available' ORDER BY sort_order" time=0.012345s
INFO 2025-09-30 10:15:35,156 DB_QUERY sql="SELECT * FROM artwork_image WHERE artwork_id IN (1, 2, 3, 4, 5)" time=0.008765s
INFO 2025-09-30 10:15:35,165 REQUEST_END path=/api/artworks/ method=GET status=200 total_time=0.042000s db_time=0.021110s query_count=2 db_percentage=50.3%
```

## Using the Logs to Diagnose Performance

### Cold Start Analysis

1. **Container Start Time**: Look for `CONTAINER_START` timestamp
2. **Django Initialization**: Check `django_app_ready` checkpoint
3. **Database Connection**: Monitor `database_ready` timing
4. **Total Startup**: Review `STARTUP_COMPLETE` summary

### Request Performance Analysis

1. **Total Request Time**: `REQUEST_END total_time`
2. **Database Time**: `REQUEST_END db_time`
3. **Database Percentage**: `REQUEST_END db_percentage`
4. **Query Count**: `REQUEST_END query_count`
5. **Individual Queries**: Each `DB_QUERY` entry

### Key Metrics to Watch

#### Startup Bottlenecks

- **Database connection > 500ms**: Neon DB cold start issue
- **Django app init > 1000ms**: Container/Python startup issue
- **Total startup > 2000ms**: Overall cold start problem

#### Query Performance

- **db_percentage > 80%**: Database is the bottleneck
- **db_percentage < 20%**: Application logic is the bottleneck
- **Individual queries > 100ms**: Specific query optimization needed

## Environment Variables

### For Development

```bash
DEBUG_SQL=true  # Enable detailed SQL logging
```

### For Production (Cloud Run)

Set these environment variables in your Cloud Run service:

```bash
DEBUG_SQL=false  # Keep false for production
DJANGO_SETTINGS_MODULE=portfolio.settings.production
```

## Testing the Setup

Run the test script to verify logging is working:

```bash
cd backend
python test_logging.py
```

## Monitoring in Cloud Run

1. Go to Google Cloud Console → Cloud Run → Your Service
2. Click on "Logs" tab
3. Filter logs by severity: "INFO" and above
4. Look for log entries with prefixes:
   - `CONTAINER_START`
   - `STARTUP_CHECKPOINT`
   - `REQUEST_START/END`
   - `DB_QUERY`

## Performance Optimization Tips

Based on the logs, you can:

1. **If database is slow**: Consider Neon DB connection pooling or upgrading plan
2. **If container startup is slow**: Optimize Docker image size or use Cloud Run min instances
3. **If specific queries are slow**: Add database indexes or optimize ORM queries
4. **If many queries per request**: Implement query optimization or caching

## Removing the Logging

To remove this logging setup:

1. Remove the middleware from `MIDDLEWARE` in settings
2. Delete the `utils/db_logging_middleware.py` file
3. Revert the `portfolio/wsgi.py` changes
4. Remove the logging configuration from settings
