import numpy as np
import numba as nb

from .zeta import zeta2
from .utils import Li2
from .color import CA


@nb.njit("f8(f8)", cache=True)
def j(a):
    sa = np.sqrt(a)
    s1pa = np.sqrt(1 + a)
    return 1.0 / (sa * s1pa) * np.log((s1pa + sa) / (s1pa - sa))


@nb.njit("f8(f8)", cache=True)
def i(a):
    sa = np.sqrt(a)
    s1pa = np.sqrt(1 + a)
    return (1.0 / (sa * s1pa)) * (
        -zeta2
        - 0.5 * np.log((s1pa + sa) / (s1pa - sa)) ** 2
        + np.log((s1pa - sa) / (2.0 * s1pa)) ** 2
        + 2.0 * Li2((s1pa - sa) / (2.0 * s1pa))
    )


@nb.njit("f8(f8,f8)", cache=True)
def cg1_LL_FL_VV(z, xi):
    return (
        (xi / z)
        * (CA / (12.0 * np.pi ** 2))
        * (
            (4.0 / xi - 4.0 / 3.0 / (1.0 + xi / 4.0))
            - (3.0 / xi + 1.0 / 4.0 / (1.0 + xi / 4.0)) * i(xi / 4.0)
            + (1.0 - 2.0 / xi - 1.0 / 6.0 / (1.0 + xi / 4.0)) * j(xi / 4.0)
        )
    )


@nb.njit("f8(f8,f8)", cache=True)
def cg1_asy_LL_FL_VV(z, xi):
    lxi = np.log(xi)  # = -LQ of Niccolò
    return (1.0 / z) * (CA / (9.0 * np.pi ** 2)) * (3.0 * lxi - 1.0)


@nb.njit("f8(f8,f8)", cache=True)
def cg1_LL_F2_VV(z, xi):
    return (
        (xi / z)
        * (CA / (12.0 * np.pi ** 2))
        * (
            10.0 / 3.0 / xi
            + (1.0 - 1.0 / xi) * i(xi / 4.0)
            + (13.0 / 6.0 - 5.0 / 3.0 / xi) * j(xi / 4.0)
        )
    )


@nb.njit("f8(f8,f8)", cache=True)
def cg1_asy_LL_F2_VV(z, xi):
    lxi = np.log(xi)  # = -LQ of Niccolò
    return (
        (1.0 / z)
        * (CA / (16.0 * np.pi ** 2))
        * (8.0 / 3.0 * lxi ** 2 + 104.0 / 9.0 * lxi + 40.0 / 9.0 - 16.0 / 3.0 * zeta2)
    )
