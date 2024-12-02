# Use the official Python image
FROM python:3.10-slim

# Install system dependencies required by reportlab
RUN apt-get update && apt-get install -y \
    build-essential \
    libc-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files into the container
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "ConverterAPI:app", "--host", "0.0.0.0", "--port", "8000"]
