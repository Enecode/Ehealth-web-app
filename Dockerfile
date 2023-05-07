# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Install Nginx and configure it to serve the Django application
RUN apt-get update && \
    apt-get install -y nginx && \
    rm /etc/nginx/sites-enabled/default && \
    cp /app/nginx.conf /etc/nginx/sites-available/ && \
    ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/

# Expose port 80 for the Nginx server
EXPOSE 80

# Start the Nginx server and the Django application
CMD service nginx start && python manage.py runserver 0.0.0.0:8000
