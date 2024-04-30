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

# Stage 3: Final stage combining Flask app and NGINX
FROM flask_app AS final

# Expose port 80 to the outside world
EXPOSE 80

# Copy NGINX configuration from nginx_server stage
COPY --from=nginx_server /etc/nginx/nginx.conf /etc/nginx/nginx.conf

# Install PostgreSQL client
USER root
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get clean
USER 10015

# Database initialization
# You may need to replace these variables with actual values
# Depending on your application's requirements
RUN pg_ctl initdb -D /var/lib/postgresql/data && \
    pg_ctl start -D /var/lib/postgresql/data && \
    psql -U ${DB_USERNAME} -d ${DB_NAME} -c "CREATE TABLE IF NOT EXISTS your_table_name (column1 type1, column2 type2);" && \
    pg_ctl stop -D /var/lib/postgresql/data
