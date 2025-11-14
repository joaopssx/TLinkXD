import socket
import json
import threading
import time
import psutil
import os
from src.utils.stats_collector import collect_stats
from src.utils.token_generator import generate_token
from src.utils.logger import setup_logger
from src.features.alerts import check_alerts
from .local_display import display_local_stats

logger = setup_logger()

def run_server(config):
    host = config['network']['host']
    port = config['network']['port']
    token = generate_token()
    print(f"Token gerado: {token}")
    print(f"Servidor ouvindo em {host}:{port}")
    logger.info(f"Servidor iniciado em {host}:{port}")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    interval = config['update_interval']

    local_display_thread = threading.Thread(target=display_local_stats, daemon=True)
    local_display_thread.start()

    def handle_client(conn, addr):
        received_token = conn.recv(1024).decode('utf-8').strip()
        if received_token != token:
            conn.sendall("Token inválido.".encode('utf-8'))
            conn.close()
            return
        conn.sendall(b"Conectado.")
        logger.info(f"Cliente conectado: {addr}")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        filter_path = os.path.join(script_dir, "..", "config", "stats_filter.json")
        with open(filter_path, 'r') as f:
            filter_config = json.load(f)

        prev_net_io = psutil.net_io_counters()
        prev_disk_io = psutil.disk_io_counters()

        while True:
            stats = collect_stats()

            current_net_io = psutil.net_io_counters()
            stats['net_upload_speed'] = round((current_net_io.bytes_sent - prev_net_io.bytes_sent) / interval / 1024, 2)
            stats['net_download_speed'] = round((current_net_io.bytes_recv - prev_net_io.bytes_recv) / interval / 1024, 2)
            prev_net_io = current_net_io

            current_disk_io = psutil.disk_io_counters()
            stats['disk_io_read_speed'] = round((current_disk_io.read_bytes - prev_disk_io.read_bytes) / interval / 1024, 2)
            stats['disk_io_write_speed'] = round((current_disk_io.write_bytes - prev_disk_io.write_bytes) / interval / 1024, 2)
            prev_disk_io = current_disk_io

            alerts = check_alerts(stats)
            if alerts:
                stats['alerts'] = alerts
                logger.warning(f"Alertas: {alerts}")

            filtered_stats = {k: v for k, v in stats.items() if filter_config.get(k)}
            conn.sendall(json.dumps(filtered_stats).encode('utf-8') + b'\n')

            time.sleep(interval)

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
