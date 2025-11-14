from colorama import Fore


def get_color(key, value):
    if "usage" in key or "used" in key:
        if isinstance(value, (int, float)) and value > 80:
            return Fore.RED
        elif isinstance(value, (int, float)) and value > 50:
            return Fore.YELLOW
        else:
            return Fore.GREEN
    elif "temp" in key:
        if isinstance(value, (int, float)) and value > 70:
            return Fore.RED
        else:
            return Fore.BLUE
    else:
        return Fore.WHITE
