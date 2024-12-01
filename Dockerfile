# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /Converter

# Copy the Converter folder into the container
COPY Converter/ /Converter/

# Copy the requirements file into the container
COPY requirements.txt .

# Install required system packages
RUN apt-get update && apt-get install -y \
    libmagic1 && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "ConverterAPI:app", "--host", "0.0.0.0", "--port", "8000"]
