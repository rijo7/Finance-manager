# Use official slim image with Python 3.11
FROM python:3.11-slim

# Install system dependencies for WeasyPrint and wkhtmltopdf
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libglib2.0-0 \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Run database migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose the port
EXPOSE 8000

# Start server with Gunicorn
CMD ["gunicorn", "finance_manager.wsgi:application", "--bind", "0.0.0.0:8000"]
