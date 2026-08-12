# Proyecto 1: análisis de complejidades algorítmicas

Este proyecto demuestra de forma numérica cómo crece el número de operaciones de distintos algoritmos según el tamaño de la entrada, `n`. Para cada complejidad se ejecuta un algoritmo representativo, se cuentan sus operaciones y se compara el resultado con su fórmula teórica.

## Complejidades analizadas

| Complejidad | Algoritmo representativo | Fórmula de referencia |
| --- | --- | ---: |
| `O(lg n)` | División sucesiva entre 2 | `lg(n)` |
| `O(n)` | Recorrido simple | `n` |
| `O(n lg n)` | Una búsqueda binaria simulada por elemento | `n * lg(n)` |
| `O(n^2)` | Recorrido de todos los pares ordenados | `n^2` |
| `O(n^3)` | Recorrido de una matriz tridimensional | `n^3` |
| `O(n^10)` | Generación de tuplas de longitud 10 | `n^10` |
| `O(n!)` | Generación de todas las permutaciones | `n!` |
| `O(2^n)` | Generación de todos los subconjuntos | `2^n` |

> `lg(n)` representa el logaritmo en base 2. Los valores de entrada son potencias de 2 en los experimentos que usan esta función.

## Metodología

El programa usa contadores explícitos en lugar de medir el tiempo de ejecución. Así evita que los resultados dependan del procesador, la carga del sistema o la implementación del intérprete.

Para cada experimento:

1. Ejecuta el algoritmo con varios valores de `n`.
2. Cuenta las operaciones realizadas.
3. Calcula el valor de la fórmula teórica.
4. Obtiene la razón `operaciones / fórmula`.
5. Muestra una tabla y, por defecto, guarda los resultados en formatos CSV y TXT.

Una razón de `1.00` indica que el contador implementado coincide exactamente con la fórmula de referencia para ese caso. El objetivo es visualizar el patrón de crecimiento; no se trata de un benchmark de rendimiento.

## Requisitos

- Python 3.9 o posterior.
- No se necesitan paquetes externos: el proyecto utiliza únicamente la biblioteca estándar de Python.

## Ejecución

Desde la raíz del repositorio:

```bash
python3 proyecto1_complejidades.py
```

El comando imprime la tabla en la terminal y genera:

- `resultados_complejidades.csv`: resultados estructurados para una hoja de cálculo o un análisis posterior.
- `salida_ejemplo.txt`: copia de la tabla mostrada en la terminal.

### Opciones disponibles

```bash
python3 proyecto1_complejidades.py --help
```

| Opción | Descripción |
| --- | --- |
| `--csv RUTA` | Cambia la ruta del archivo CSV generado. |
| `--txt RUTA` | Cambia la ruta del archivo de texto generado. |
| `--no-guardar` | Muestra los resultados sin escribir archivos. |

Ejemplos:

```bash
# Mostrar la tabla sin modificar archivos
python3 proyecto1_complejidades.py --no-guardar

# Guardar los resultados en rutas personalizadas
python3 proyecto1_complejidades.py \
  --csv datos/resultado.csv \
  --txt datos/resultado.txt
```

Las carpetas indicadas en rutas personalizadas deben existir antes de ejecutar el programa.

## Formato de los resultados

Cada fila contiene los siguientes campos:

| Campo | Significado |
| --- | --- |
| `Complejidad` | Orden de crecimiento estudiado. |
| `Algoritmo` | Nombre del procedimiento representativo. |
| `n` | Tamaño de la entrada. |
| `Operaciones medidas` | Operaciones contadas por el algoritmo. |
| `Formula esperada` | Resultado de la fórmula teórica. |
| `Operacion/formula` | Razón entre el conteo y la referencia. |

Ejemplo abreviado:

```text
Complejidad | Algoritmo                 | n  | Operaciones medidas | Formula esperada | Operacion/formula
O(lg n)     | Division sucesiva entre 2 | 16 | 4                   | 4                | 1.00
O(n^2)      | Pares ordenados           | 20 | 400                 | 400              | 1.00
O(2^n)      | Subconjuntos              | 12 | 4096                | 4096             | 1.00
```

## Estructura del repositorio

```text
.
├── proyecto1_complejidades.py   # Implementación y ejecución de los experimentos
├── resultados_complejidades.csv # Resultados en formato tabular
├── salida_ejemplo.txt            # Salida completa de ejemplo
└── README.md                     # Documentación del proyecto
```

## Interpretación

Los resultados permiten comparar la rapidez con la que crecen las funciones:

- `O(lg n)`, `O(n)` y `O(n lg n)` mantienen un crecimiento moderado y aceptan valores de entrada relativamente grandes.
- `O(n^2)` y `O(n^3)` aumentan con rapidez debido a sus ciclos anidados.
- `O(n^10)`, `O(n!)` y `O(2^n)` se vuelven costosos incluso para entradas pequeñas, por lo que el programa utiliza valores de `n` limitados.

La notación Big O describe una cota asintótica y normalmente omite constantes y términos de menor orden. En este proyecto, cada algoritmo fue construido para que su conteo coincida con una fórmula concreta; por eso la columna `Operacion/formula` vale `1.00` en los datos incluidos.

## Consideraciones

- Los experimentos cuentan iteraciones específicas, no todas las instrucciones ejecutadas por Python.
- Los tamaños de entrada se eligieron para que los algoritmos de crecimiento rápido terminen en un tiempo razonable.
- Cambiar los valores de `EXPERIMENTS` puede aumentar considerablemente el tiempo de ejecución y el uso de recursos, especialmente en `O(n^10)`, `O(n!)` y `O(2^n)`.
