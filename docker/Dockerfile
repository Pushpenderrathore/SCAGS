FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (layer caching)
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy project
COPY . .

# Seed the database on build
RUN python database/seed.py

EXPOSE 5000

ENV FLASK_DEBUG=false

CMD ["python", "backend/app.py"]
