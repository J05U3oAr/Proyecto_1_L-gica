from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from itertools import permutations
from pathlib import Path
from typing import Callable, Iterable


OperationCounter = Callable[[int], int]
ReferenceFormula = Callable[[int], int]


@dataclass(frozen=True)
class Experiment:
    complexity: str
    name: str
    values: tuple[int, ...]
    algorithm: OperationCounter
    reference: ReferenceFormula


def algorithm_logarithmic(n: int) -> int:
    """O(lg n): divide el problema entre 2 en cada iteracion."""
    operations = 0
    while n > 1:
        n //= 2
        operations += 1
    return operations


def algorithm_linear(n: int) -> int:
    """O(n): recorre n elementos una sola vez."""
    operations = 0
    for _ in range(n):
        operations += 1
    return operations


def algorithm_n_log_n(n: int) -> int:
    """O(n lg n): por cada elemento hace una busqueda binaria simulada."""
    operations = 0
    for _ in range(n):
        size = n
        while size > 1:
            size //= 2
            operations += 1
    return operations


def algorithm_quadratic(n: int) -> int:
    """O(n^2): compara todos los pares ordenados."""
    operations = 0
    for _ in range(n):
        for _ in range(n):
            operations += 1
    return operations


def algorithm_cubic(n: int) -> int:
    """O(n^3): recorre una matriz tridimensional."""
    operations = 0
    for _ in range(n):
        for _ in range(n):
            for _ in range(n):
                operations += 1
    return operations


def algorithm_power_ten(n: int) -> int:
    """O(n^10): genera todas las tuplas de longitud 10 con valores 0..n-1."""
    operations = 0

    def visit(depth: int) -> None:
        nonlocal operations
        if depth == 10:
            operations += 1
            return
        for _ in range(n):
            visit(depth + 1)

    visit(0)
    return operations


def algorithm_factorial(n: int) -> int:
    """O(n!): genera todas las permutaciones de n elementos."""
    operations = 0
    for _ in permutations(range(n)):
        operations += 1
    return operations


def algorithm_exponential(n: int) -> int:
    """O(2^n): genera todos los subconjuntos mediante mascaras de bits."""
    operations = 0
    for _ in range(1 << n):
        operations += 1
    return operations


def lg(n: int) -> int:
    return int(math.log2(n)) if n > 0 else 0


EXPERIMENTS: tuple[Experiment, ...] = (
    Experiment("O(lg n)", "Division sucesiva entre 2", (2, 4, 8, 16, 32, 64, 128), algorithm_logarithmic, lg),
    Experiment("O(n)", "Recorrido simple", (10, 100, 1_000, 5_000, 10_000), algorithm_linear, lambda n: n),
    Experiment("O(n lg n)", "n busquedas binarias simuladas", (8, 16, 32, 64, 128, 256), algorithm_n_log_n, lambda n: n * lg(n)),
    Experiment("O(n^2)", "Pares ordenados", (10, 20, 50, 100, 200), algorithm_quadratic, lambda n: n**2),
    Experiment("O(n^3)", "Matriz tridimensional", (5, 10, 20, 30, 40), algorithm_cubic, lambda n: n**3),
    Experiment("O(n^10)", "Tuplas de longitud 10", (1, 2, 3, 4), algorithm_power_ten, lambda n: n**10),
    Experiment("O(n!)", "Permutaciones", (1, 2, 3, 4, 5, 6, 7, 8), algorithm_factorial, math.factorial),
    Experiment("O(2^n)", "Subconjuntos", (4, 8, 12, 16, 20), algorithm_exponential, lambda n: 2**n),
)


def run_experiments() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for experiment in EXPERIMENTS:
        for n in experiment.values:
            operations = experiment.algorithm(n)
            reference = experiment.reference(n)
            ratio = operations / reference if reference else 0
            rows.append(
                {
                    "Complejidad": experiment.complexity,
                    "Algoritmo": experiment.name,
                    "n": str(n),
                    "Operaciones medidas": str(operations),
                    "Formula esperada": str(reference),
                    "Operacion/formula": f"{ratio:.2f}",
                }
            )
    return rows


def format_table(rows: Iterable[dict[str, str]]) -> str:
    materialized = list(rows)
    headers = ["Complejidad", "Algoritmo", "n", "Operaciones medidas", "Formula esperada", "Operacion/formula"]
    widths = {
        header: max(len(header), *(len(row[header]) for row in materialized))
        for header in headers
    }
    separator = " | "
    lines = [
        separator.join(header.ljust(widths[header]) for header in headers),
        separator.join("-" * widths[header] for header in headers),
    ]
    for row in materialized:
        lines.append(separator.join(row[header].ljust(widths[header]) for header in headers))
    return "\n".join(lines)


def save_csv(rows: Iterable[dict[str, str]], path: Path) -> None:
    materialized = list(rows)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=materialized[0].keys())
        writer.writeheader()
        writer.writerows(materialized)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Proyecto 1: evidencia numerica de complejidades mediante conteo de operaciones."
    )
    parser.add_argument("--csv", type=Path, default=Path("resultados_complejidades.csv"), help="Ruta del CSV generado.")
    parser.add_argument(
        "--txt",
        type=Path,
        default=Path("salida_ejemplo.txt"),
        help="Ruta del archivo de texto con la misma tabla mostrada en pantalla.",
    )
    parser.add_argument("--no-guardar", action="store_true", help="Solo imprime en consola, sin escribir archivos.")
    args = parser.parse_args()

    rows = run_experiments()
    table = format_table(rows)
    print(table)

    if not args.no_guardar:
        save_csv(rows, args.csv)
        args.txt.write_text(table + "\n", encoding="utf-8")
        print()
        print(f"Archivos generados: {args.csv} y {args.txt}")


if __name__ == "__main__":
    main()
