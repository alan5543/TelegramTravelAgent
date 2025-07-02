# Use an official Node.js image as a base (it comes with npm)
# We choose a version like 18-alpine for a balance of features and small image size.
FROM node:18-alpine

# Install Python and its dependencies for uv
# apk is the package manager for Alpine Linux. curl is needed to download uv installer.
RUN apk add --no-cache python3 py3-pip curl

# Install uv (uvx comes with uv)
# This is the recommended standalone installer method for uv.
# It installs uv to /root/.cargo/bin by default.
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv's installation directory to the PATH for the root user.
# This ensures uv and uvx commands are found.
ENV PATH="/root/.cargo/bin:$PATH"

# Set the working directory inside the container
WORKDIR /app

# Copy your requirements.txt file first to leverage Docker's build cache.
# If requirements.txt changes, only this layer and subsequent layers will be rebuilt.
COPY requirements.txt .

# Install Python dependencies using uv.
# `uv pip install -r` is the command to install from requirements.txt.
# We use --no-cache-dir to keep the image smaller by not storing install caches.
RUN uv pip install -r requirements.txt --no-cache-dir

# Copy the rest of your application code into the container
# The '.' copies everything from the current build context (your project directory)
# to the /app directory inside the container.
COPY . .

# Expose the port your FastAPI application will listen on.
# Hugging Face Spaces typically expects your application to listen on port 7860.
EXPOSE 7860

# Define the command to run your FastAPI application with Uvicorn.
# The `uvicorn` server will listen on 0.0.0.0 (all network interfaces) at port 7860.
# The 'main:app' refers to the 'app' object within your 'main.py' file.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]