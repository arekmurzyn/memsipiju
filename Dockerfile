# Use an official Python runtime as the base image
FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install wheel
# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Upgrade PIP
RUN pip install --timeout=1000 --upgrade pip
# Install any dependencies
RUN pip install --timeout=1000 --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Specify the port number the container should expose
EXPOSE 5000

# Run the application
CMD ["uwsgi", "--socket", "0.0.0.0:5000", "--protocol=http", "--module", "memsipiju:app"]