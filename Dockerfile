# Use an official Python 3.10.5 runtime as a parent image
FROM python:3.10.5

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port the app runs on
EXPOSE $PORT

# Run the command to start the Django development server
CMD python manage.py runserver 0.0.0.0:$PORT
