# Use a small Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /main

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Run your app
CMD ["python", "-m", "main.app"]

EXPOSE 8080