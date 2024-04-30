# Use the official Python image as base
FROM python:3.10
# Set the working directory in the container
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . /app
# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Expose port 8000 to the outside world
EXPOSE 8000
# Define environment variable
ENV FLASK_APP=app.py
# Define the mode of deployment
ENV FLASK_ENV=development
# Run app.py when the container launches
CMD ["python3", "main.py"]

# # Copy entrypoint script into the container
# COPY entrypoint.sh /app/entrypoint.sh

# # Give execute permissions to the entrypoint script
# RUN chmod +x /app/entrypoint.sh

# # Run the entrypoint script when the container launches
# CMD ["/bin/bash", "/app/entrypoint.sh"]