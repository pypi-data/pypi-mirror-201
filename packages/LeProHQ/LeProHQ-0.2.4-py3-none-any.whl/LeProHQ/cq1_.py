# -*- coding: utf-8 -*-
import numba as nb
import numpy as np

from .cg0_ import cg0t
from .color import Kgph, Kqph
from .partonic_vars import build_eta, build_xi
from .utils import ln2, raw_c
from . import bmsn

@nb.njit("UniTuple(f8,2)(string,string)", cache=True)
def aq(proj, cc):
    """Quark NLO resummation coefficients"""
    a11 = 1.0
    a10 = -13.0 / 12.0 + 3.0 / 2.0 * ln2
    if proj == "FL" and cc == "VV":
        a11 -= 2.0 / 5.0
        a10 = -77.0 / 100.0 + 9.0 / 10.0 * ln2
    elif proj == "x2g1" and cc == "VV":
        a10 -= 1.0 / 4.0
    return a11, a10


@nb.njit("f8(string,string, f8,f8)", cache=True)
def cq1t(proj, cc, xi, eta):
    """Threshold limit of cq1"""
    rho, beta, chi = build_eta(eta)
    rho_q, _beta_q, _chi_q = build_xi(xi)
    a11, a10 = aq(proj, cc)
    return (
        cg0t(proj, cc, xi, eta)
        * beta ** 2
        / np.pi ** 2
        * (rho_q / (rho_q - 1.0))
        * (Kqph / 6.0 / Kgph)
        * (a11 * np.log(beta) + a10)
    )

def cq1hv(proj,cc,xi,eta):
    """High virtuality limit of cq1."""
    l = np.log(xi)
    z = xi / (4.*(1.+eta) + xi)
    n = xi * 4**2 * np.pi / z
    if proj == "F2":
        return (bmsn.c2ps2am0_aq2(z) * l**2 + bmsn.c2ps2am0_aq(z) * l + bmsn.c2ps2am0_a0(z)) / n
    elif proj == "FL":
        return (bmsn.clps2am0_aq(z) * l + bmsn.clps2am0_a0(z)) / n
    raise ValueError(f"High virtuality limit of {proj}_{cc} is not known!")

def cq1(proj, cc, xi, eta, path=None):
    """NLO Bethe-Heitler Quark coefficient function"""
    return raw_c(proj, cc, xi, eta, path, "cq1", cq1t, cq1hv, np.log(1e0), np.log(1.5e3))
