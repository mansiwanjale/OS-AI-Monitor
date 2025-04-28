import psutil
import json
import os
import datetime

# Function to get the real-time CPU usage percentage (more responsive)
def get_cpu_usage():
    # Getting CPU usage over a shorter interval (0.1s) for real-time responsiveness
    return psutil.cpu_percent(interval=0.1)

# Function to get the real-time memory usage percentage
def get_memory_usage():
    # Fetch the virtual memory usage in real-time
    memory = psutil.virtual_memory()
    return memory.percent

# Function to get the real-time disk usage percentage
def get_disk_usage():
    # Fetch the disk usage for the root directory in real-time
    disk = psutil.disk_usage('/')
    return disk.percent

# Function to calculate health score based on system usage metrics (without network usage)
def calculate_health_score(cpu, memory, disk):
    # Ensure each metric is within the 0-100 range
    cpu = max(0, min(cpu, 100))
    memory = max(0, min(memory, 100))
    disk = max(0, min(disk, 100))

    # Calculate the health score based on the remaining metrics (cpu, memory, disk)
    score = (100 - cpu) * 0.4 + (100 - memory) * 0.3 + (100 - disk) * 0.3
    
    # Ensure score is positive and within the range 0 to 100
    score = max(0, min(score, 100))

    return round(score)

# Function to save the daily health score to a file (e.g., for the calendar)
def save_daily_score(score):
    daily_scores_file = 'daily_scores.json'
    if os.path.exists(daily_scores_file):
        with open(daily_scores_file, 'r') as f:
            daily_scores = json.load(f)
    else:
        daily_scores = {}

    today = datetime.date.today().isoformat()  # Get today's date in ISO format (YYYY-MM-DD)
    daily_scores[today] = score

    with open(daily_scores_file, 'w') as f:
        json.dump(daily_scores, f, indent=4)

# Function to get the health data for the frontend (JSON format)
def get_health_data():
    # Fetch real-time data for CPU, Memory, and Disk
    cpu = get_cpu_usage()
    memory = get_memory_usage()
    disk = get_disk_usage()
    
    # Calculate health score based on system data
    health_score = calculate_health_score(cpu, memory, disk)
    
    # Save the health score to the daily scores file
    save_daily_score(health_score)
    
    # Prepare the response data
    health_data = {
        'score': health_score,
        'cpuUsage': cpu,
        'memoryUsage': memory,
        'diskUsage': disk,
    }
    
    return health_data

# Endpoint for the System Health API (for example, using Flask)
if __name__ == '__main__':
    # Get real-time system health data
    system_health = get_health_data()

    # Print out the system health data as a JSON object
    print(json.dumps(system_health, indent=4))
