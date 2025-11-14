import json
import os
import platform
import sys

from src.client.client import run_client
from colorama import init
from src.server.server import run_server
from src.utils.platform_detector import is_termux, is_windows

init(autoreset=True)  # Inicializa colorama

# Obtém o diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config", "base_config.json")

# Carrega configs principais
with open(config_path, "r") as f:
    base_config = json.load(f)


def main():
    if is_windows():
        print("Detectado: Windows - Iniciando modo Servidor.")
        run_server(base_config)
    elif is_termux():
        print("Detectado: Termux - Iniciando modo Cliente.")
        run_client(base_config)
    else:
        print("Plataforma não suportada. Use Windows ou Termux.")
        sys.exit(1)


if __name__ == "__main__":
    main()
