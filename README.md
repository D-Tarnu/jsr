# JSR

JSR implements the invariant polytope algorithm described in "Exact computation of joint spectral characteristics of linear operators" by N. Guglielmi and V. Protasov and "Extremal polytope norms for real families" by N. Guglielmi and M. Zennaro. Given a set of matrices `mats`, a maximum product length to consider for spectrum-maximizing products, and a maximum number of iterations to go through each potential spectrum-maximizing product, `jsr` tries to find the joint spectral radius of `mats` and returns/prints it if successful. Here is an example of how you might use it:

```
from jsr.src import jsr

mats = [
    [[-3, -2, 1, 2], [-2, 0, -2, 1], [1, 3, -1, -5], [-3, -3, -2, -1]],
    [[1, 0, -3, -1], [-4, -2, -1, -4], [-1, 0, -1, 2], [-1, -2, -1, 2]]
    ]

jsr.invar_poly(mats, num_smps = 10, num_iter = 10)
```

Things to add: 
- a bit that makes this work if a potential spectrum-maximizing product has multiple leading eigenvectors
- more algorithms to facilitate the computation and approximation of the joint spectral radius
