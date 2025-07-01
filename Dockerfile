# Dockerfile
# Use a Python base image with Node.js pre-installed (for npx)
FROM python:3.10-slim-buster

# Install Node.js if your base image doesn't have it (some python images include it)
# If using python:3.10-slim-buster, you'll likely need to install node/npm
RUN apt-get update && \
    apt-get install -y --no-install-recommends nodejs npm && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port that your FastAPI application will listen on
# Hugging Face Spaces default to 7860 for web apps.
ENV PORT=7860
EXPOSE $PORT

# Command to run your FastAPI application with Uvicorn
# This will execute when your Space starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]