# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
# - ffmpeg for audio processing by Whisper
# - git for any potential SCM operations by huggingface_hub or similar (good to have)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install PyTorch with CPU support first (important for smaller install size)
# Using the same --extra-index-url as we configured for Render
RUN pip install --no-cache-dir torch torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Expose the port the app runs on (Hugging Face Spaces typically use 7860)
EXPOSE 7860

# Define the command to run your app using Gunicorn
# We'll use Gunicorn, similar to your Procfile, and bind to port 7860.
# Using --workers 1 as we did before for memory constraints.
# Using --timeout 120 as we found necessary.
CMD ["gunicorn", "--workers", "1", "--timeout", "120", "--bind", "0.0.0.0:7860", "app:app"]
