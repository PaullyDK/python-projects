Run Locally (Without Docker)
1. Install Dependencies
	pip install -r requirements.txt
2. Start the server
	python server.py
3. Open your browser
	http://127.0.0.1:5000/metrics

Run With Docker
1. Build the Docker image
	docker build -t logservice .
2. Run the container
	docker run -p 5001:5000 logservice
3. view metrics
	http://localhost:5001/metrics

A lightweight Python microservice that analyzes HTTP server logs and exposes key metrics through a REST API. The service processes log files to compute total requests, success rate, most frequent endpoint, and average response time, and makes these analytics available via a /metrics endpoint. The entire application is containerized using Docker for easy deployment and portability. Made for practice.
