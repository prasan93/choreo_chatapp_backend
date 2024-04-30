# Stage 1: Build Flask application
FROM python:3.10 AS flask_app

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Switch to the non-root user
USER 10015

# Expose port 8000 to the outside world
EXPOSE 8000

# Define environment variable
ENV FLASK_APP=app.py

# Define the mode of deployment
ENV FLASK_ENV=development

# Run app.py when the container launches
CMD ["python3", "main.py"]

# Stage 2: Build NGINX
FROM nginx:latest AS nginx_server

# Copy NGINX configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Stage 3: PostgreSQL Setup
FROM postgres:latest AS postgres_setup

# Environment variables for PostgreSQL
ENV POSTGRES_DB=idea
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=Prasan123#
ENV DB_NAME=idea
ENV DB_USERNAME=postgres
ENV DB_PASSWORD=Prasan123#
ENV DB_HOST=init-db
ENV DB_PORT=5432

# Expose PostgreSQL port
EXPOSE 5432

# Stage 4: Final stage combining Flask app, NGINX, and PostgreSQL
FROM flask_app AS final

# Expose port 80 to the outside world
EXPOSE 80

# Copy NGINX configuration from nginx_server stage
COPY --from=nginx_server /etc/nginx/nginx.conf /etc/nginx/nginx.conf

