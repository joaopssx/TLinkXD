def ascii_bar(value, short=False):
    if short:
        bars = int(value / 20)  # Para horizontal curto
        return "#" * bars
    bars = int(value / 10)
    return "[" + "#" * bars + " " * (10 - bars) + "]"
