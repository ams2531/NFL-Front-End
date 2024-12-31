FROM python:3.9.7-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y <br>    gcc <br>    python3-dev <br>    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Make sure we expose the port
EXPOSE 10000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
