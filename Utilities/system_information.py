import os
import json
import psutil
import platform
import GPUtil
import ctypes
from ctypes import wintypes
import subprocess
from datetime import datetime

SPEC_FILE = "system_specs.json"

# System Queries Functions
def check_power_status():
    battery = psutil.sensors_battery()
    if battery is None:
        return "Unable to determine power status."
    return "The laptop is currently on AC power." if battery.power_plugged else "The laptop is currently running on battery."

def get_wifi_info():
    wifi_info = "Unable to retrieve Wi-Fi information."
    if platform.system() == "Windows":
        try:
            result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], stderr=subprocess.DEVNULL)
            result = result.decode('utf-8').split("\n")
            for line in result:
                if "SSID" in line:
                    wifi_info = line.split(":")[1].strip()
                    break
        except Exception as e:
            wifi_info = f"Error retrieving Wi-Fi info: {e}"
    return wifi_info

def get_battery_percentage():
    battery = psutil.sensors_battery()
    if battery is None:
        return "Unable to determine battery percentage."
    return f"Battery percentage: {battery.percent}%"

def get_cpu_usage():
    return f"CPU Usage: {psutil.cpu_percent()}%"

def get_ram_usage():
    memory = psutil.virtual_memory()
    return f"RAM Usage: {memory.percent}% ({round(memory.used / (1024 ** 3), 2)} GB used)"

def get_gpu_usage():
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            return f"GPU Usage: {gpus[0].load * 100:.2f}%"
    except Exception as e:
        return f"GPU Usage: Error retrieving GPU usage: {e}"
    return "GPU Usage: No GPU detected."

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return f"Disk Usage: {disk.percent}% used ({round(disk.used / (1024 ** 3), 2)} GB used of {round(disk.total / (1024 ** 3), 2)} GB)"

def get_system_uptime():
    uptime_seconds = psutil.boot_time()
    uptime = round((psutil.time.time() - uptime_seconds) / 3600, 2)
    return f"System Uptime: {uptime} hours"

def get_process_count():
    return f"Number of running processes: {len(psutil.pids())}"

def check_network_status():
    try:
        subprocess.check_output(["ping", "-n", "1", "8.8.8.8"], stderr=subprocess.STDOUT)
        return "Network Status: Connected to the internet"
    except subprocess.CalledProcessError:
        return "Network Status: Not connected to the internet"

def get_active_connections():
    try:
        connections = psutil.net_connections()
        return f"Active Connections: {len(connections)}"
    except Exception as e:
        return f"Error retrieving active connections: {e}"

def get_swap_memory_usage():
    swap = psutil.swap_memory()
    return f"Swap Memory Usage: {swap.percent}% ({round(swap.used / (1024 ** 3), 2)} GB used)"

def get_available_partitions():
    partitions = psutil.disk_partitions()
    return [partition.device for partition in partitions]

def get_temperature_sensors():
    try:
        sensors = psutil.sensors_temperatures()
        return sensors if sensors else "No temperature sensors found."
    except Exception as e:
        return f"Error retrieving temperature sensors: {e}"

def get_battery_time_remaining():
    battery = psutil.sensors_battery()
    if battery is None:
        return "Unable to determine battery time remaining."
    return f"Time Remaining: {round(battery.secsleft / 60)} minutes" if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Time Remaining: Unlimited"

def is_system_virtualized():
    return "System is virtualized" if "VIRTUAL" in platform.platform().upper() else "System is not virtualized"

def get_boot_time():
    boot_time = psutil.boot_time()
    return f"Boot Time: {datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')}"

def get_user_login_info():
    users = psutil.users()
    return [f"{user.name} logged in since {datetime.fromtimestamp(user.started).strftime('%Y-%m-%d %H:%M:%S')}" for user in users]

def get_top_memory_processes():
    processes = sorted(psutil.process_iter(['pid', 'name', 'memory_percent']), key=lambda p: p.info['memory_percent'], reverse=True)[:5]
    return [(proc.info['name'], proc.info['memory_percent']) for proc in processes]

def get_top_cpu_processes():
    processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), key=lambda p: p.info['cpu_percent'], reverse=True)[:5]
    return [(proc.info['name'], proc.info['cpu_percent']) for proc in processes]

# Save and Load System Specs
def save_specs_to_file():
    specs = {
        "Processor": platform.processor(),
        "RAM": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
        "Storage": f"{round(psutil.disk_usage('/').total / (1024 ** 3), 2)} GB",
        "OS": platform.system(),
        "Graphics": "No GPU detected.",
    }
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            specs["Graphics"] = gpus[0].name
    except Exception as e:
        specs["Graphics"] = f"Error retrieving GPU info: {e}"

    with open(SPEC_FILE, "w") as file:
        json.dump(specs, file, indent=4)
    return "System specs saved successfully."

def load_specs_from_file():
    if os.path.exists(SPEC_FILE):
        with open(SPEC_FILE, "r") as file:
            return json.load(file)
    return "No saved specifications found."

# Main Program
def main():
    queries = {
        "power status": check_power_status,
        "battery percentage": get_battery_percentage,
        "disk usage": get_disk_usage,
        "system uptime": get_system_uptime,
        "process count": get_process_count,
        "network status": check_network_status,
        "active connections": get_active_connections,
        "available partitions": get_available_partitions,
        "battery time remaining": get_battery_time_remaining,
        "user login info": get_user_login_info,
        "save specs": save_specs_to_file,
        "load specs": load_specs_from_file,
        "top memory processes": get_top_memory_processes,
    }

    while True:
        user_input = input("\nAsk for system info (or type 'exit' to quit): ").lower()
        if user_input == "exit":
            print("Exiting...")
            break
        elif user_input in queries:
            result = queries[user_input]()
            if isinstance(result, list):
                for item in result:
                    print(item)
            else:
                print(result)
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
