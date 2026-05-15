FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Buat user non-root untuk keamanan (opsional tapi disarankan)
RUN useradd -U appuser
USER appuser

EXPOSE 8080

# Jalankan dengan gunicorn sesuai standar deployment
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "service:app"]
