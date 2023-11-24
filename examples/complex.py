from datetime import datetime

from jsr import invar_poly

mats = [
    [[-3, -2, 1, 2], [-2, 0, -2, 1], [1, 3, -1, -5], [-3, -3, -2, -1]],
    [[1, 0, -3, -1], [-4, -2, -1, -4], [-1, 0, -1, 2], [-1, -2, -1, 2]]
    ]
now = datetime.now()
invar_poly(mats, 10, 10)
print('Time elapsed = ', (datetime.now() - now).total_seconds())
