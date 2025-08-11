# TRB Service

A production-ready FastAPI template service.

## Running the service

### With Docker

This service is containerized using Docker.

### Prerequisites

- Docker

### Build the Docker image

```bash
docker build -t trb-service .
```

### Run the Docker container

```bash
docker run -d -p 8000:80 --name trb-service-container trb-service
```

### Accessing the service

Once the container is running, you can access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

The health check endpoint is available at [http://localhost:8000/health](http://localhost:8000/health).

### Generating a PDF

You can generate a PDF by sending a POST request to the `/generate-pdf` endpoint. Here is an example using `curl`:

```bash
curl -X POST "http://localhost:8000/generate-pdf" \
-H "Content-Type: application/json" \
-d '{"html_content": "<html><body><h1>Hello, PDF!</h1><p>This is a test PDF generated from HTML.</p></body></html>"}' \
-o generated_resume.pdf
```

This will create a file named `generated_resume.pdf` in your current directory.

### Running Locally (Without Docker)

To run the service locally without Docker, you can use the `run_local.sh` script. This will create a Python virtual environment, install the necessary dependencies, and start the application.

```bash
./run_local.sh
```

The first time you run this script, `pyppeteer` will download a compatible version of Chromium, which may take a few minutes. The service will be available at [http://localhost:8000](http://localhost:8000).

### Stopping the container

```bash
docker stop trb-service-container
docker rm trb-service-container
```


### Production deployment steps:

1. Install pip - First time only

```bash
sudo apt update
sudo apt install python3-pip
```

2. Install the python3-venv

```bash
sudo apt install python3.11-venv
```

3. Create venv

```bash
python3 -m venv venv
```

4. Install uvicorn

```bash
sudo apt install python3-uvicorn
```
5. run the application

```bash
./run_local.sh
```