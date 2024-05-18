# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install curl and ping
RUN apt-get update && apt-get install -y curl

# Make port 8888 available to the world outside this container
EXPOSE 8888

# Run the app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8888", "server:app"]