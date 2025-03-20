FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=drf_geo.drf_geo.settings

# Set working directory
WORKDIR /app

# Copy requirements.txt first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Create a non-root user and set it as the owner of the working directory
RUN adduser --disabled-password --gecos '' drf_geouser \
    && chown -R drf_geouser:drf_geouser /app \
    && chmod -R 755 /app

# Switch to the non-root user
USER drf_geouser

# Expose port 8000
EXPOSE 8000

# Run migrations, collect static files, and start Gunicorn
CMD ["sh", "-c", "python drf_geo/manage.py migrate && python drf_geo/manage.py collectstatic --noinput && gunicorn drf_geo.drf_geo.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
