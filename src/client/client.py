import json
import os
import socket
import sys

from colorama import Fore
from src.client.display import display_horizontal, display_stats


def run_client(config):
    host = input("Digite o IP do servidor: ")
    port = config["network"]["port"]
    token = input("Digite o token: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except Exception as e:
        print(f"Erro de conexão: {e}")
        sys.exit(1)

    client_socket.sendall(token.encode("utf-8"))
    response = client_socket.recv(1024).decode("utf-8")
    if response != "Conectado.":
        print(response)
        sys.exit(1)

    # Corrige o caminho da configuração de display
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "..", "config", "display_config.json")
    with open(config_path, "r") as f:
        display_config = json.load(f)
    horizontal = display_config["horizontal_mode"]

    print(Fore.GREEN + "Conectado! Recebendo stats...")
    buffer = ""
    while True:
        try:
            data = client_socket.recv(4096).decode("utf-8")
            if not data:
                break
            buffer += data
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                stats = json.loads(line)
                os.system("clear")
                if horizontal:
                    display_horizontal(stats)
                else:
                    display_stats(stats)
        except json.JSONDecodeError:
            print(Fore.RED + "Erro ao decodificar os dados do servidor. Tentando novamente...")
            # Limpa o buffer para evitar loops de erro com dados corrompidos
            buffer = ""
            continue
        except KeyboardInterrupt:
            print("\nDesconectando...")
            break
        except Exception as e:
            print(f"\nErro inesperado: {e}")
            break

    client_socket.close()
