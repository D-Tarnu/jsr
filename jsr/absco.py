import numpy as np
import cvxpy as cp
from scipy.spatial import ConvexHull

def in_complex_absco(z, cloud, acc):
    m = int(len(z)/2)
    n = int(len(cloud)/(2*m))
    x = cp.Variable(3*n + 1)

    A = np.eye(2*n)
    A = np.pad(A, ((2, 0), (n + 1, 0)), mode='constant')
    A = [A[2*i:2*(i+1)] for i in range(n+1)]

    b = [np.array([1,0])]
    for i in range(n):
        b.append(np.zeros(2))

    c = [np.append(np.full(n + 1, -1), np.zeros(2*n))]
    c[0][0] = 0
    for i in range(1, n+1):
        c.append(np.array([1 if i == j else 0 for j in range(3*n + 1)]))

    d = np.append([2], np.zeros(n)).tolist()

    f = np.append([1], np.zeros(3*n))

    F = np.append(np.zeros(n + 1), (np.insert(cloud[::2*m], np.arange(1, n + 1), 0) - np.insert(cloud[1::2*m], np.arange(0, n), 0)))
    F[0] = -z[0]
    for i in range(1, m):
        row = np.append(np.zeros(n + 1), (np.insert(cloud[2*i::2*m], np.arange(1, n + 1), 0) - np.insert(cloud[2*i + 1::2*m], np.arange(0, n), 0)))
        row[0] = -z[2*i]
        F = np.vstack((F, row))
    for i in range(m):
        row = np.append(np.zeros(n + 1), (np.insert(cloud[2*i + 1::2*m], np.arange(1, n + 1), 0) + np.insert(cloud[2*i::2*m], np.arange(0, n), 0)))
        row[0] = -z[2*i + 1]
        F = np.vstack((F, row))

    g = np.zeros(2*m)

    soc_constraints = [
        cp.SOC(c[i].T @ x + d[i], A[i] @ x + b[i]) for i in range(n + 1)
    ]
    prob = cp.Problem(cp.Maximize(f.T@x),
                      soc_constraints + [F @ x == g])
    prob.solve(solver=cp.CLARABEL)

    if prob.value + acc > 1:
        return True

    return False

def in_absco(point, cloud, complex, acc):
    if complex:
        return in_complex_absco(point, cloud, acc)
    else:
        absco = ConvexHull(cloud + [[-x for x in y] for y in cloud])
        return all(
            (np.dot(eq[:-1], point) + eq[-1] <= acc)
            for eq in absco.equations)

