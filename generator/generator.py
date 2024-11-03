import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration for the requests
URL = "http://127.0.0.1:5000/job"  # Adjust this to match your Flask app's endpoint
NUM_REQUESTS = 100  # Total number of requests to send
DURATION_MIN = 0.01  # Minimum duration in seconds for simulation
DURATION_MAX = 1.0  # Maximum duration in seconds for simulation
MEMORY_MIN = 0.1  # Minimum memory in MB to allocate
MEMORY_MAX = 50  # Maximum memory in MB to allocate
TEST_DURATION = 120  # Duration in seconds for the entire test

def generate_request():
    """Generate a single request with random parameters."""
    payload = {
        'duration': random.uniform(DURATION_MIN, DURATION_MAX),
        'memory_mb': random.uniform(MEMORY_MIN, MEMORY_MAX)
    }
    return payload

def send_request(payload):
    """Send a POST request to the server with the given payload."""
    try:
        response = requests.post(URL, json=payload, timeout=10)
        if response.status_code == 200:
            return True
        else:
            print(f"Request failed with status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False

def main():
    start_time = time.time()
    end_time = start_time + TEST_DURATION
    requests_sent = 0
    successes = 0

    # Use a thread pool to make concurrent requests
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers for concurrency
        futures = []
        while time.time() < end_time and requests_sent < NUM_REQUESTS:
            payload = generate_request()
            future = executor.submit(send_request, payload)
            futures.append(future)
            requests_sent += 1

        for future in as_completed(futures):
            if future.result():
                successes += 1

    duration = time.time() - start_time
    print(f"Test completed in {duration:.2f} seconds.")
    print(f"Total requests sent: {requests_sent}")
    print(f"Successful requests: {successes}")
    if requests_sent > 0:
        print(f"Success rate: {100 * successes / requests_sent:.2f}%")

if __name__ == "__main__":
    main()