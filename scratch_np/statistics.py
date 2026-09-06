"""Os dados da DataSciencester, como arrays.

As listas moram em `scratch/statistics.py` (capítulo 5 do Grus, fora da
ementa): quantos amigos cada usuário tem e quantos minutos por dia passa no
site, com e sem o outlier de 100 amigos. Os capítulos 11 e 12 fazem regressão
em cima delas.

Este módulo só as converte. É a ÚNICA razão para um arquivo de `scratch_np/`
importar `scratch.`: dado, nunca função. Importar `scratch.statistics` desenha
figuras no nível do módulo — o `plt.close('all')` abaixo as descarta antes que
vazem para a saída de uma célula.
"""
import numpy as np
from matplotlib import pyplot as plt

from scratch import statistics as _grus

plt.close("all")

num_friends = np.array(_grus.num_friends, dtype=float)
daily_minutes = np.array(_grus.daily_minutes, dtype=float)
daily_hours = daily_minutes / 60

num_friends_good = np.array(_grus.num_friends_good, dtype=float)
daily_minutes_good = np.array(_grus.daily_minutes_good, dtype=float)
daily_hours_good = daily_minutes_good / 60

assert num_friends.shape == daily_minutes.shape == (204,)
assert num_friends_good.shape == daily_minutes_good.shape == (203,)
assert num_friends.max() == 100 and num_friends_good.max() == 49
