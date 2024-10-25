from flask import Flask, request, jsonify
import time
import random
import sys

app = Flask(__name__)

@app.route('/job', methods=['POST'])
def run_job():
    if not request.is_json:
        print(f"Error: Request must be JSON", file=sys.stderr)
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    duration = data.get('duration', None)
    memory_mb = data.get('memory_mb', None)

    if duration is None:
        print(f"Error: Duration parameter is required", file=sys.stderr)
        return jsonify({"error": "Duration parameter is required"}), 400
    
    try:
        duration = float(duration)
        if duration <= 0:
            raise ValueError("Duration must be a positive number")
        
        if memory_mb is not None:
            memory_mb = float(memory_mb)
            if memory_mb < 0:
                raise ValueError("Memory amount must be non-negative")
    except ValueError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return jsonify({"error": str(e)}), 400
    
    # Simulate CPU usage
    start_time = time.time()
    end_time = start_time + duration
    
    # Allocate memory if requested
    allocated_memory = []
    if memory_mb:
        try:
            memory_to_allocate = int(memory_mb * 1024 * 1024)  # Convert MB to bytes
            for _ in range(memory_to_allocate // 1000):  # Allocate in chunks
                allocated_memory.append(bytearray(1000))  # 1000 bytes per chunk
        except MemoryError:
            print(f"Error: Unable to allocate requested memory", file=sys.stderr)
            return jsonify({"error": "Insufficient memory to fulfill request"}), 500
    
    try:
        while time.time() < end_time:
            # This loop does nothing but consume CPU time and keep memory allocated
            x = 1
            for i in range(1000000):  # Some arbitrary number of iterations
                x += i
    except Exception as e:
        print(f"Error during job execution: {str(e)}", file=sys.stderr)
        return jsonify({"error": "An unexpected error occurred during job execution"}), 500
    
    # Clear the allocated memory
    allocated_memory = []

    # Print a message to stdout when the job is done
    print(f"Job completed. Duration: {duration} seconds, Memory: {memory_mb} MB", file=sys.stdout)

    return jsonify({
        "status": "completed",
        "duration_requested": duration,
        "memory_allocated_mb": memory_mb if memory_mb else 0,
        "actual_duration": time.time() - start_time
    }), 200

if __name__ == '__main__':
    app.run(debug=True)