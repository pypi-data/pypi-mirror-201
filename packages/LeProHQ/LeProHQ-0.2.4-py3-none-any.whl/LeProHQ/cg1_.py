# -*- coding: utf-8 -*-
import numpy as np

from .cg0_ import cg0t
from .color import CA, CF
from .partonic_vars import build_eta
from .raw import cg1_a10 as raw_cg1_a10
from .utils import ln2, raw_c
from . import bmsn


def ag(proj, cc, xi):
    """Gluon NLO resummation coefficients."""
    a12 = 1.0
    a11 = -5.0 / 2.0 + 3.0 * ln2
    if proj == "FL" and cc == "VV":
        a11 -= 2.0 / 3.0
    a10_OK = raw_cg1_a10.__getattribute__(  # pylint: disable=no-member
        f"cg1_a10_{proj}_{cc}_OK"
    )(xi)
    a10_QED = raw_cg1_a10.__getattribute__(  # pylint: disable=no-member
        f"cg1_a10_{proj}_{cc}_QED"
    )(xi)
    return a12, a11, a10_OK, a10_QED


def cg1t(proj, cc, xi, eta):
    """Threshold limit of cg1."""
    rho, beta, chi = build_eta(eta)
    coulomb = np.pi ** 2 / (16.0 * beta) * (2.0 * CF - CA)
    a12, a11, a10_OK, a10_QED = ag(proj, cc, xi)
    res = (
        CA * (a12 * np.log(beta) ** 2 + a11 * np.log(beta) + a10_OK)
        + 2.0 * CF * a10_QED
    )
    return cg0t(proj, cc, xi, eta) / np.pi ** 2 * (coulomb + res)

def cg1hv(proj,cc,xi,eta):
    """High virtuality limit of cg1."""
    l = np.log(xi)
    z = xi / (4.*(1.+eta) + xi)
    n = xi * 4**2 * np.pi / z
    if proj == "F2":
        return (bmsn.c2g2am0_aq2(z) * l**2 + bmsn.c2g2am0_aq(z) * l + bmsn.c2g2am0_a0(z)) / n
    elif proj == "FL":
        return (bmsn.clg2am0_aq(z) * l + bmsn.clg2am0_a0(z)) / n
    raise ValueError(f"High virtuality limit of {proj}_{cc} is not known!")

def cg1(proj, cc, xi, eta, path=None):
    """NLO gluon coefficient function."""
    return raw_c(proj, cc, xi, eta, path, "cg1", cg1t, cg1hv, np.log(1e-1), np.log(1.5e3))
