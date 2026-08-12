from __future__ import annotations

"""Proyecto 1: conteo de operaciones para comparar complejidades.

Este programa ejecuta varios algoritmos pequenos, cada uno disenado para
representar una complejidad distinta. En vez de medir tiempo de ejecucion,
cuenta cuantas operaciones realiza cada algoritmo y compara ese conteo con
una formula matematica esperada.

Salidas principales al ejecutar el archivo:
- Imprime una tabla en consola.
- Genera un CSV con los resultados, si no se usa --no-guardar.
- Genera un TXT con la misma tabla de consola, si no se usa --no-guardar.
"""

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
    """Representa un experimento de complejidad.

    Attributes:
        complexity: Texto de la complejidad analizada, por ejemplo "O(n^2)".
        name: Nombre del algoritmo representativo.
        values: Valores de entrada n que se probaran.
        algorithm: Funcion que recibe n y devuelve operaciones medidas.
        reference: Formula que recibe n y devuelve el valor teorico esperado.
    """

    complexity: str
    name: str
    values: tuple[int, ...]
    algorithm: OperationCounter
    reference: ReferenceFormula


def algorithm_logarithmic(n: int) -> int:
    """Cuenta operaciones de un algoritmo O(lg n).

    El valor n se divide entre 2 en cada iteracion hasta llegar a 1.

    Args:
        n: Tamano de la entrada.

    Returns:
        Cantidad de divisiones realizadas. Para potencias de 2, devuelve lg(n).
    """

    operations = 0
    while n > 1:
        n //= 2
        operations += 1
    return operations


def algorithm_linear(n: int) -> int:
    """Cuenta operaciones de un algoritmo O(n).

    Simula un recorrido simple donde se visita cada elemento una vez.

    Args:
        n: Tamano de la entrada.

    Returns:
        Cantidad de iteraciones realizadas, que corresponde a n.
    """

    operations = 0
    for _ in range(n):
        operations += 1
    return operations


def algorithm_n_log_n(n: int) -> int:
    """Cuenta operaciones de un algoritmo O(n lg n).

    Por cada uno de los n elementos, simula una busqueda binaria que divide
    el tamano del problema entre 2.

    Args:
        n: Tamano de la entrada.

    Returns:
        Cantidad total de divisiones simuladas, igual a n * lg(n) para las
        potencias de 2 usadas en los experimentos.
    """

    operations = 0
    for _ in range(n):
        size = n
        while size > 1:
            size //= 2
            operations += 1
    return operations


def algorithm_quadratic(n: int) -> int:
    """Cuenta operaciones de un algoritmo O(n^2).

    Usa dos ciclos anidados para representar la revision de todos los pares
    ordenados posibles.

    Args:
        n: Tamano de la entrada.

    Returns:
        Cantidad de pares visitados, igual a n^2.
    """

    operations = 0
    for _ in range(n):
        for _ in range(n):
            operations += 1
    return operations


def algorithm_cubic(n: int) -> int:
    """Cuenta operaciones de un algoritmo O(n^3).

    Usa tres ciclos anidados para simular el recorrido de una estructura
    tridimensional.

    Args:
        n: Tamano de la entrada.

    Returns:
        Cantidad de posiciones visitadas, igual a n^3.
    """

    operations = 0
    for _ in range(n):
        for _ in range(n):
            for _ in range(n):
                operations += 1
    return operations


def algorithm_power_ten(n: int) -> int:
    """Cuenta operaciones de un algoritmo O(n^10).

    Genera conceptualmente todas las tuplas de longitud 10. Cada posicion de
    la tupla puede tomar n valores diferentes.

    Args:
        n: Cantidad de valores posibles para cada posicion de la tupla.

    Returns:
        Cantidad de tuplas generadas, igual a n^10.
    """

    operations = 0

    def visit(depth: int) -> None:
        """Avanza recursivamente hasta completar una tupla de longitud 10."""

        nonlocal operations
        if depth == 10:
            operations += 1
            return
        for _ in range(n):
            visit(depth + 1)

    visit(0)
    return operations


def algorithm_factorial(n: int) -> int:
    """Cuenta operaciones de un algoritmo O(n!).

    Recorre todas las permutaciones posibles de los elementos 0..n-1.

    Args:
        n: Cantidad de elementos a permutar.

    Returns:
        Cantidad de permutaciones generadas, igual a n!.
    """

    operations = 0
    for _ in permutations(range(n)):
        operations += 1
    return operations


def algorithm_exponential(n: int) -> int:
    """Cuenta operaciones de un algoritmo O(2^n).

    Simula la generacion de todos los subconjuntos posibles. Cada subconjunto
    se representa con una mascara de bits.

    Args:
        n: Cantidad de elementos del conjunto original.

    Returns:
        Cantidad de subconjuntos posibles, igual a 2^n.
    """

    operations = 0
    for _ in range(1 << n):
        operations += 1
    return operations


def lg(n: int) -> int:
    """Calcula el logaritmo base 2 entero usado como formula de referencia.

    Args:
        n: Valor de entrada.

    Returns:
        Parte entera de log2(n). Si n no es positivo, devuelve 0.
    """

    return int(math.log2(n)) if n > 0 else 0


# Lista central de experimentos. Cada entrada conecta:
# complejidad, nombre del algoritmo, valores de n, funcion medida y formula.
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
    """Ejecuta todos los experimentos definidos en EXPERIMENTS.

    Returns:
        Lista de diccionarios. Cada diccionario representa una fila de la
        tabla final con complejidad, algoritmo, n, operaciones medidas,
        formula esperada y razon operacion/formula.
    """

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
    """Convierte los resultados en una tabla de texto alineada.

    Args:
        rows: Filas generadas por run_experiments().

    Returns:
        Cadena de texto con encabezados, separador y filas alineadas.
    """

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
    """Guarda los resultados en un archivo CSV.

    Args:
        rows: Filas generadas por run_experiments().
        path: Ruta donde se escribira el archivo CSV.

    Returns:
        None. La funcion no devuelve datos; su efecto es crear o sobrescribir
        el archivo indicado.
    """

    materialized = list(rows)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=materialized[0].keys())
        writer.writeheader()
        writer.writerows(materialized)


def main() -> None:
    """Punto de entrada del programa.

    Lee argumentos de consola, ejecuta los experimentos, imprime la tabla y,
    si corresponde, guarda los resultados en CSV y TXT.

    Returns:
        None. La salida visible del programa es la impresion en consola y los
        archivos generados.
    """

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
        # Guarda los mismos datos en dos formatos: CSV estructurado y TXT legible.
        save_csv(rows, args.csv)
        args.txt.write_text(table + "\n", encoding="utf-8")
        print()
        print(f"Archivos generados: {args.csv} y {args.txt}")


if __name__ == "__main__":
    main()
