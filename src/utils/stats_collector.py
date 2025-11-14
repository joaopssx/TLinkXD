import getpass
import platform
import socket
import time

import psutil


def get_cpu_temp():
    if platform.system() != "Windows":
        return None
    try:
        import wmi
        w = wmi.WMI(namespace="root\\wmi")
        temp_info = w.MSAcpi_ThermalZoneTemperature()[0]
        return (temp_info.CurrentTemperature / 10.0) - 273.15
    except Exception:
        return None


def get_system_temps():
    return psutil.sensors_temperatures() or None


def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return None


def get_net_connections():
    connections = []
    for conn in psutil.net_connections(kind="inet"):
        if conn.status == "ESTABLISHED":
            conn_dict = {
                "local_addr": f"{conn.laddr.ip}:{conn.laddr.port}",
                "remote_addr": f"{conn.raddr.ip}:{conn.raddr.port}"
                if conn.raddr
                else None,
                "status": conn.status,
            }
            connections.append(conn_dict)
    return connections


def get_top_processes():
    processes = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            processes.append(
                {
                    "pid": proc.info["pid"],
                    "name": proc.info["name"],
                    "cpu_percent": proc.info["cpu_percent"],
                    "memory_percent": proc.info["memory_percent"],
                }
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    processes.sort(key=lambda p: p["cpu_percent"], reverse=True)
    return processes[:5]


def get_disk_partitions():
    return [p.device for p in psutil.disk_partitions()]


def collect_stats():
    battery = psutil.sensors_battery()
    stats = {
        "user": getpass.getuser(),
        "xd": None,
        "os": platform.system() + " " + platform.release(),
        "processor": platform.processor(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "cpu_freq": psutil.cpu_freq().current if psutil.cpu_freq() else None,
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "cpu_temp": get_cpu_temp(),
        "system_temps": get_system_temps(),
        "ram_total": round(psutil.virtual_memory().total / (1024**3), 2),
        "ram_used": round(psutil.virtual_memory().used / (1024**3), 2),
        "ram_free": round(psutil.virtual_memory().available / (1024**3), 2),
        "swap_total": round(psutil.swap_memory().total / (1024**3), 2),
        "swap_used": round(psutil.swap_memory().used / (1024**3), 2),
        "disk_total": round(psutil.disk_usage("/").total / (1024**3), 2),
        "disk_used": round(psutil.disk_usage("/").used / (1024**3), 2),
        "disk_partitions": get_disk_partitions(),
        "disk_io_read_speed": 0.0,  # Calculado no loop
        "disk_io_write_speed": 0.0,  # Calculado no loop
        "uptime": round((time.time() - psutil.boot_time()) / 3600, 2),
        "battery_percent": battery.percent if battery else None,
        "battery_time_left": (battery.secsleft / 60)
        if battery and battery.secsleft != psutil.POWER_TIME_UNLIMITED
        else None,
        "battery_plugged": battery.power_plugged if battery else None,
        "net_interfaces": list(psutil.net_if_addrs().keys()),
        "local_ip": get_local_ip(),
        "net_upload_speed": 0.0,
        "net_download_speed": 0.0,
        "net_sent_cumulative": psutil.net_io_counters().bytes_sent / (1024**2),
        "net_recv_cumulative": psutil.net_io_counters().bytes_recv / (1024**2),
        "net_connections": get_net_connections(),
        "processes": get_top_processes(),
    }
    return stats
