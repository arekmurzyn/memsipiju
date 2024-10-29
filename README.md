# Memsipiju 🧠

![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9-blue)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

Welcome to **Memsipiju**, a Flask application for simulating intensive CPU and memory usage. Ideal for testing system performance or learning about Flask and Docker.

## Table of Contents 📖
- [Memsipiju 🧠](#memsipiju-)
  - [Table of Contents 📖](#table-of-contents-)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Docker](#docker)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- Simulate CPU Usage
- Memory Allocation
- Docker Containerization
- Simple REST API

## Installation

Start the Flask application with:

```sh
python memsipiju.py
```

## Usage

**API**

    POST /job
        Parameters: 
            - duration (required): Duration in seconds for CPU usage simulation.
            - memory_mb (optional): MB of memory to allocate.
            
```json
{
  "duration": 10,
  "memory_mb": 100
}
```

## Docker

Build and run with Docker:

```sh
docker build -t memsipiju .
docker run -p 5000:5000 memsipiju
```

## Contributing

Contributions are welcome! Here's how to contribute:

-Fork the repo on GitHub
-Clone the project to your own machine
-Commit changes to your own branch
-Push your work back up to your fork
-Submit a pull request

## License

Licensed under the Apache License 2.0 (LICENSE). 

For any questions or suggestions, please open an issue. Enjoy using Memsipiju!