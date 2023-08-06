"""
Outils utilisés dans le projet poetry_example_project. 
"""

from datetime import datetime

def print_log(message: str) -> None:
    """Prints a message to the console."""
    print(f"{datetime.now()} : {message}")
