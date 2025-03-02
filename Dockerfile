# Use the official Python image
FROM python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app will run on (adjust as needed)
EXPOSE 8000

# Use Uvicorn to serve the app in production mode
CMD ["uvicorn", "app.asgi:application", "--host", "0.0.0.0", "--port", "8000"]