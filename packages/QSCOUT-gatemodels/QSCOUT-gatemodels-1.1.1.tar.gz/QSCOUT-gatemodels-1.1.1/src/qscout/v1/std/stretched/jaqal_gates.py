# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.
from numpy import abs, diag, pi, kron

import pygsti

from .. import jaqal_gates
from jaqalpaq.core.stretch import stretched_gates

ALL_GATES = jaqal_gates.ALL_GATES.copy()
del ALL_GATES["prepare_all"]
del ALL_GATES["measure_all"]
ALL_GATES = stretched_gates(ALL_GATES, suffix="_stretched")
