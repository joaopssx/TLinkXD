import os
import platform


def is_windows():
    return platform.system() == "Windows"


def is_termux():
    return "TERMUX_VERSION" in os.environ or "/data/data/com.termux" in os.getcwd()
