# tasks.py

import psutil

from flask import Flask, jsonify
import psutil

app = Flask(__name__)

def get_process_data():
    process_list = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'io_counters']):
        try:
            process_info = proc.info
            memory_usage = process_info['memory_info'].rss / (1024 * 1024)  # Memory in MB
            disk_usage = process_info['io_counters'].read_bytes / (1024 * 1024)  # Disk in MB
            cpu_usage = process_info['cpu_percent']  # CPU percentage
            process_list.append({
                'pid': process_info['pid'],
                'name': process_info['name'],
                'cpu': cpu_usage,
                'memory': memory_usage,
                'disk': disk_usage
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue  # Skip processes we don't have access to

    # Sort the processes based on CPU usage in descending order
    process_list.sort(key=lambda x: x['cpu'], reverse=True)

    return process_list
