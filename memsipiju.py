from flask import Flask, request, jsonify
import time
import sys
import json
from datetime import datetime

def log_json(message, level="info", **kwargs):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "message": message,
        **kwargs  # Any additional key-value pairs can be added here
    }
    # Write to stdout for info and above, stderr for error and below
    output_stream = sys.stderr if level in ["error", "critical", "warn"] else sys.stdout
    json.dump(log_entry, output_stream, ensure_ascii=False)
    output_stream.write("\n")

app = Flask(__name__)

@app.route('/job', methods=['POST'])
def run_job():
    if not request.is_json:
        #print(f"Error: Request must be JSON", file=sys.stderr)
        log_json("Request must be JSON", level="error")
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    duration = data.get('duration', None)
    memory_mb = data.get('memory_mb', None)

    if duration is None:
        #print(f"Error: Duration parameter is required", file=sys.stderr)
        log_json("Duration parameter is required", level="error")
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
        #print(f"Error: {str(e)}", file=sys.stderr)
        log_json("{str(e)}", level="error")
        return jsonify({"error": str(e)}), 400
  
    # Allocate memory if requested
    allocated_memory = []
    if memory_mb:
        try:
            memory_to_allocate = int(memory_mb * 1024 * 1024)  # Convert MB to bytes
            for _ in range(memory_to_allocate // 1000):  # Allocate in chunks
                allocated_memory.append(bytearray(1000))  # 1000 bytes per chunk
        except MemoryError:
            #print(f"Error: Unable to allocate requested memory", file=sys.stderr)
            log_json("Unable to allocate requested memory", level="error")
            return jsonify({"error": "Insufficient memory to fulfill request"}), 500
    
    # Simulate CPU usage
    end_time = time.time() + duration
    try:
        while time.time() < end_time:
            # This loop does nothing but consume CPU time and keep memory allocated
            x = 1
            for i in range(1000000):  # Some arbitrary number of iterations
                x += i
    except Exception as e:
        #print(f"Error during CPU job execution: {str(e)}", file=sys.stderr)
        log_json("An unexpected error occurred during CPU job execution", level="error")
        return jsonify({"error": "An unexpected error occurred during CPU job execution"}), 500
    
    # Clear the allocated memory
    allocated_memory = []

    # Print a message to stdout when the job is done
    #print(f"Job completed. Duration: {duration} seconds, Memory: {memory_mb} MB", file=sys.stdout)
    log_json(f"Job completed. Duration: {duration} seconds, Memory: {memory_mb} MB", level="info")
    return jsonify({
        "status": "completed",
        "duration_requested": duration,
        "memory_allocated_mb": memory_mb if memory_mb else 0,
    }), 200

if __name__ == '__main__':
    app.run(debug=True,  # Enable debug mode
            host='0.0.0.0', # Listen on all public IPs
            port=5000)