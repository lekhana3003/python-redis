# Use the official Python image from Docker Hub
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the rest of the application code into the container
COPY . /app/

# Copy the entry point script into the container
COPY spawn_redis_server.sh /app/

# Set the entry point for the container
ENTRYPOINT ["./spawn_redis_server.sh"]
