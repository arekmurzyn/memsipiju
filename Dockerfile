# docker build --progress=plain --no-cache -t arbajt/memsipiju:0.0.1 .
# Build stage
FROM python:3.9-slim as builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libc6-dev \
    libpcre3 \
    libpcre3-dev \
    && rm -rf /var/lib/apt/lists/* 

# Create a virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the dependencies file to the working directory
COPY requirements-build.txt .

# Upgrade PIP
RUN pip install --timeout=100 --upgrade pip
# Install any dependencies
RUN pip install --timeout=100 --no-cache-dir -r requirements.txt

#runtime stage
FROM python:3.9-slim as runtime

# Creating user for uwsgi
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy pcre library from build time
COPY --from=builder /usr/lib/x86_64-linux-gnu/libpcre.so.3 usr/lib/x86_64-linux-gnu

# Set PATH to use the copied virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy the script from src directory to the working directory
COPY memsipiju.py .

# Specify the port number the container should expose
EXPOSE 5000

# Run the application
USER uwsgi
CMD ["uwsgi", "--master", "--socket", "0.0.0.0:5000", "--protocol=http", "--module", "memsipiju:app", "--enable-threads"]