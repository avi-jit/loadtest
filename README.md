# Load Tester

A general-purpose HTTP load-testing and benchmarking library written in Python. This tool allows you to test the performance of your HTTP endpoints by generating requests at a given fixed QPS (queries per second) and reporting latencies and error rates.

## Features

- Takes an HTTP address as input.
- Supports a `--qps` flag to generate requests at a given fixed QPS.
- Reports latencies and error rates.
- Supports concurrency with multiple threads.
- Docker image for easy deployment.

## Prerequisites

- Python 3.9+
- Docker (for building and running the Docker image)

## Installation

### Clone the Repository

```sh
git clone https://github.com/avi-jit/load-tester.git
cd load-tester
```

### Install Dependencies

```sh
pip install -r requirements.txt
```

## Usage

### Running the Load Tester

```sh
python load_tester.py http://httpbin.org/get --qps 2 --duration 2 --concurrency 2
```

### Command-Line Arguments

- `url`: The URL to test.
- `qps`: Queries per second (default: 1).
- `duration`: Duration of the test in seconds (default: 10).
- `concurrency`: Number of concurrent threads (default: 1).

## Running Tests

### Install Test Dependencies
```sh
pip install unittest
```

### Run Tests

```sh
python -m unittest discover -s tests
```

## Docker

### Building the Docker Image

```sh
docker build -t load-tester .
```

### Running the Docker Container

```sh
docker run --rm load-tester http://httpbin.org/get --qps 2 --duration 2 --concurrency 2
```

## Example

### Running the Load Tester with Docker
```sh
docker run --rm load-tester http://httpbin.org/get --qps 10 --duration 30 --concurrency 5
```

This command will:

- Hit the URL `http://httpbin.org/get`
- Generate 10 queries per second
- Run the test for 30 seconds
- Use 5 concurrent threads

## License
This project is licensed under the MIT License - see the LICENSE file for details.
