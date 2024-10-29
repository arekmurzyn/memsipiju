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
        log_json("Request must be JSON", level="error")
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    duration = data.get('duration', None)
    memory_mb = data.get('memory_mb', None)

    if duration is None:
        log_json("Duration parameter is required", level="error")
        return jsonify({"error": "Duration parameter is required"}), 400
    if memory_mb is None:
        log_json("Memory amount parameter is required", level="error")
        return jsonify({"error": "Memory amount parameter is required"}), 400

    try:
        duration = float(duration)
    except ValueError:
        log_json("Duration must be a positive number", level="error")
        return jsonify({"error":"Duration must be a positive number"}), 400        
        
    try:    
        memory_mb = float(memory_mb)
    except ValueError:
        log_json("Memory amount must be a positive number", level="error")
        return jsonify({"error": "Memory amount must be a positive number"}), 400

    if duration <= 0:
        log_json("Duration must be a positive number", level="error")
        return jsonify({"error": "Duration must be a positive number"}), 400
 
    if memory_mb <= 0:
        log_json("Memory amount must be a positive number", level="error")
        return jsonify({"error": "Memory amount must be a positive number"}), 400

    # Allocate memory if requested
    allocated_memory = []
    if memory_mb:
        try:
            memory_to_allocate = int(memory_mb * 1024 * 1024)  # Convert MB to bytes
            for _ in range(memory_to_allocate // 1000):  # Allocate in chunks
                allocated_memory.append(bytearray(1000))  # 1000 bytes per chunk
        except MemoryError:
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
        log_json("An unexpected error occurred during CPU job execution", level="error")
        return jsonify({"error": "An unexpected error occurred during CPU job execution"}), 500
    
    # Clear the allocated memory
    allocated_memory = []

    # Print a message to stdout when the job is done
    log_json(f"Job completed. Duration: {duration} seconds, Memory: {memory_mb} MB", level="info")
    return jsonify({
        "status": "completed",
        "duration_requested": duration,
        "memory_allocated_mb": memory_mb if memory_mb else 0,
    }), 200

if __name__ == '__main__':
    app.run(debug=False)