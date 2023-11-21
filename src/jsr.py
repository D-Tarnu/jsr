import numpy as np
import numpy.linalg as linalg

from .absco import in_absco

def flatten_complex_vec(v):
    res = np.array([])

    for entry in v:
        res = np.append(res, entry.real)
        res = np.append(res, entry.imag)

    return res

def essential_vertices(cloud, vertices, complex, dim, num_pts, acc):
    index = 0

    for i in range(num_pts):
        if complex:
            if in_absco(cloud[index*(2*dim) : (index + 1)*(2*dim)], np.concatenate((cloud[:index*(2*dim)], cloud[(index + 1)*(2*dim):])), complex, acc):
                cloud = np.delete(cloud, np.s_[index*(2*dim) : (index+1)*(2*dim)])
                vertices.pop(index)
                index += 1
        else:
            if in_absco(cloud[index], cloud[:index] + cloud[index + 1:], complex, acc):
                cloud.pop(index)
                index += 1
    
    return cloud

def invar_poly(mats, num_smps, num_iter, prune=None, acc=0.000001):
    mats = [np.array(M) for M in mats]
    cands = [np.eye(mats[0].shape[0])]

    for smp_index in range(1, num_smps + 1):
        print('SMP Length: ', smp_index, '...........', flush = True)
        max_eval = 0
        leading_evec = []
        cands = [M @ C for M in mats for C in cands]

        for C in cands:
            evals, evecs = linalg.eig(C)
            abs_evals = np.absolute(evals)
            M_max_eval, max_index = max((value, index) for index, value in enumerate(abs_evals))
            if M_max_eval > max_eval:
                max_eval = M_max_eval
                leading_evec = evecs[:, max_index]

        scaled_mats = [M*(1/(max_eval**(1/smp_index))) for M in mats]
        V = [leading_evec]
        V_flatten = np.array([])
        
        complex = False
        for entry in leading_evec:
            if entry.imag != 0:
                complex = True
                break

        if complex:
            V.append(np.conjugate(leading_evec))
            for v in V:
                V_flatten = np.append(V_flatten, flatten_complex_vec(v))
        else: 
            V[0] = V[0].real
            dim = len(leading_evec)
            while len(V) <= dim:
                for i in range(len(V)):
                    for M in scaled_mats:
                        V.append(M @ V[i])

        prods_used = set([tuple(v) for v in V])

        for iter_index in range(1, num_iter + 1):
            print(iter_index, flush = True)
            done = True
            prods = []
            
            for i in range(len(V)):
                for M in scaled_mats:
                    prods.append(M @ V[i])

            for prod in prods:
                prod_hashable = tuple(prod)
                point = flatten_complex_vec(prod) if complex else prod
                cloud = V_flatten if complex else V

                if prod_hashable not in prods_used and not in_absco(point, cloud, complex, acc):
                    V.append(prod)
                    prods_used.add(prod_hashable)
                    if complex:
                        V_flatten = np.append(V_flatten, point)
                    done = False

            if done:
                print('JSR = ', max_eval**(1/smp_index), '\nSMP length = ', smp_index, flush = True)
                return max_eval**(1/smp_index)
            
            if prune:
                cloud = V_flatten if complex else V
                V_flatten = essential_vertices(cloud, V, complex, len(V[0]), len(V))
    
    print('JSR not found. Try increasing num_smps or num_iter.')