# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (like mysql client if needed, though pymysql is used)
# RUN apt-get update && apt-get install -y --no-install-recommends default-mysql-client && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir reduces image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables (can be overridden at runtime)
# These should be set during deployment (e.g., via Docker run -e or docker-compose.yml)
# ENV FLASK_APP=src/main.py
# ENV FLASK_RUN_HOST=0.0.0.0
# ENV DB_HOST=db # Example if using docker-compose with a service named 'db'
# ENV DB_USERNAME=root
# ENV DB_PASSWORD=password
# ENV DB_NAME=mydb
# ENV INSTAGRAM_APP_ID=...
# ENV INSTAGRAM_APP_SECRET=...
# ENV INSTAGRAM_REDIRECT_URI=...
# ENV JWT_SECRET_KEY=...

# Run main.py when the container launches using gunicorn (recommended for production)
# Install gunicorn first
RUN pip install gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.main:app"]

# Alternatively, for development/testing:
# CMD ["python", "src/main.py"]

