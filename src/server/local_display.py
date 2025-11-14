import os
import time

from colorama import Fore
from src.ui.color_utils import get_color
from src.ui.graph_utils import ascii_bar
from src.utils.stats_collector import collect_stats


def display_local_stats():
    while True:
        stats = collect_stats()  # Coleta stats para display local
        os.system("cls" if os.name == "nt" else "clear")
        print(Fore.CYAN + "Status Local do Servidor (Windows):")
        for key, value in stats.items():
            if value is not None:
                color = get_color(key, value)
                if (
                    isinstance(value, (int, float))
                    and "percent" in key
                    or "usage" in key
                ):
                    bar = ascii_bar(value)
                    print(f"{color}{key.capitalize()}: {value} {bar}{Fore.RESET}")
                elif isinstance(value, list):
                    print(f"{color}{key.capitalize()}: {Fore.RESET}")
                    for item in value:
                        print(f" - {item}")
                else:
                    print(f"{color}{key.capitalize()}: {value}{Fore.RESET}")
        time.sleep(5)  # Atualiza a cada 5s
