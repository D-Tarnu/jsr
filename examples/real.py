from datetime import datetime

from src import jsr

mats = [
    [[1, 0, 2], [-1, 0, 2], [0, 1, 0]],
    [[0, 1, 0], [0, -1, 0], [1, 0, 0]]
    ]
now = datetime.now()
jsr.invar_poly(mats, 10, 10, False)
print('Time elapsed = ', (datetime.now() - now).total_seconds())
