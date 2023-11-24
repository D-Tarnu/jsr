from datetime import datetime

from jsr import invar_poly

mats = [
    [[1, 0, 2], [-1, 0, 2], [0, 1, 0]],
    [[0, 1, 0], [0, -1, 0], [1, 0, 0]]
    ]
now = datetime.now()
invar_poly(mats, 10, 10)
print('Time elapsed = ', (datetime.now() - now).total_seconds())

# These matrices are tied to the sequence autocorrelations of Rudin-Shapiro sequences (see "On maximal autocorrelations of Rudin-Shapiro sequences" by T.).
# Note how quickly the JSR is found compared to the complex.py example. This is due to only working with a real leading eigenvector.
