"""
Fonctions utilitaires de mathématiques
"""
from poetry_example_project.tools.hellotools import print_log

def add(first_term: int, second_term: int)-> int:
    """Additionne deux termes"""
    print_log(f"{first_term} + {second_term}")
    result = first_term+second_term
    print_log(f"Et le résultat est... {result}")

def sub(first_term: int, second_term: int)-> int:
    """Soustrait deux termes"""
    print_log(f"{first_term} - {second_term}")
    result = first_term-second_term
    print_log(f"Et le résultat est... {result}")

def mul(first_term: int, second_term: int)-> int:
    """Multiplie deux termes"""
    print_log(f"{first_term} * {second_term}")
    result = first_term*second_term
    print_log(f"Et le résultat est... {result}")
