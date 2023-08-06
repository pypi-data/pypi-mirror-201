from typing import Literal

import numpy as np
import pandas as pd


def new_population(vars: int) -> pd.DataFrame:
    """
    Cria uma nova população vazia. População será abstraída por um DataFrame do pandas em que
    as linhas representam o indivíduos.
    As colunas serão:
     - speed_{n}: velocidade da partícula n
     - position_{n}: posição da partícula n no espaço
     - best_position_n: melhor posição da partícula n
     - objective: valor da função objetivo

    Examples:
        >>> p = new_population(20)
        >>> isinstance(p, pd.DataFrame)
        True
        >>> p.empty
        True
        >>> len(p.columns) == 20 * 3 + 1
        True
    """
    columns = []
    for col_name in "speed", "position", "best_position":
        for i in range(vars):
            columns.append(f"{col_name}_{i}")

    columns.append("objective")

    population = pd.DataFrame(columns=columns, data=[])
    return population


def random_numbers(
    number: int,
    vars: int,
    min: int | None = None,
    max: int | None = None,
    type: Literal["int"] | Literal["float"] | None = None,
) -> np.ndarray:
    """
    Gera números aleatórios dependendo da entrada.

    Examples:
        >>> numbers = random_numbers(200, 3, 2, 20)
        >>> len(numbers) == 200
        True

    """
    max = max or 1
    min = min or 0
    assert min < max, "'min' deve ser menor do que 'max'"

    assert isinstance(vars, int), "'vars' deve ser inteiro"

    size = (number, vars)
    numbers = np.random.uniform(min, max, size=size)

    match type:
        case "int":
            numbers = np.int64(numbers)
    return numbers
