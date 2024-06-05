# Use the official Python image from the Docker Hub
FROM python:3.11-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the Flask app runs on
EXPOSE 8000

# Set environment variables for Flask
ENV FLASK_APP=app.py

# Command to run the application
CMD ["python", "app.py"]


# docker build -t image_name .
# docker run -p 8000:8000 image_name
# Uvicorn running on http://0.0.0.0:8000, instead, use this http://localhost:8000
# when you run the docker run command, you are launching a new container based on the specified image, and the application runs inside that container.