FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -d /app appuser

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=appuser:appgroup app/ app/
COPY --chown=appuser:appgroup wsgi.py .

# Switch to non-root user
USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "wsgi:app"]