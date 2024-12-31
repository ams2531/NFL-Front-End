FROM python:3.9-slim

WORKDIR /app

# Install gunicorn explicitly
RUN pip install gunicorn

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all files
COPY . .

# Make sure we expose the port
EXPOSE 10000

# Run gunicorn with explicit path
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
