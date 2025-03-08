# Use a stable official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy dependency file first for caching benefits
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application after installing dependencies
COPY . .

# Expose Flask port
EXPOSE 5000

# Set environment variables (better to use .env)
ENV FLASK_APP="leader-follower/org_api.py"
ENV FLASK_RUN_HOST="0.0.0.0"
ENV FLASK_RUN_PORT=5000

# Create a non-root user for security
RUN useradd -m flaskuser
USER flaskuser

# Run the Flask app using Waitress
CMD ["python", "leader-follower/org_api.py"]
