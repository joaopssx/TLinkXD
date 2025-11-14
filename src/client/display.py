from colorama import Fore
from src.ui.color_utils import get_color
from src.ui.graph_utils import ascii_bar


def display_stats(stats):
    for key, value in stats.items():
        if value is not None:
            color = get_color(key, value)
            if isinstance(value, (int, float)) and ("percent" in key or "usage" in key):
                bar = ascii_bar(value)
                print(f"{color}{key.capitalize()}: {value} {bar}{Fore.RESET}")
            elif isinstance(value, list):
                print(f"{color}{key.capitalize()}: {Fore.RESET}")
                for item in value:
                    print(f" - {item}")
            elif isinstance(value, dict):
                print(f"{color}{key.capitalize()}: {value}{Fore.RESET}")
            else:
                print(f"{color}{key.capitalize()}: {value}{Fore.RESET}")


def display_horizontal(stats):
    parts = []
    for key, value in stats.items():
        if value is not None:
            if isinstance(value, (int, float)) and ("percent" in key or "usage" in key):
                bar = ascii_bar(value, short=True)
                parts.append(f"{key}:{value} {bar}")
            else:
                val_str = (
                    str(value)[:20] + "..." if len(str(value)) > 20 else str(value)
                )
                parts.append(f"{key}:{val_str}")
    line = " | ".join(parts)
    print(line)
