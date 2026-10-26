"""Shared static contracts for validated JSON and scientific arrays.

Config and Report retain heterogeneous JSON at the existing validation/serialization
boundaries. They do not claim a static schema or empirical validity. Numerical
interfaces use ArrayLike inputs and float64 arrays after their existing checks.
"""

from typing import Any

import numpy as np
from numpy.typing import NDArray

type FloatArray = NDArray[np.float64]
type StateArrays = dict[str, FloatArray]
type Config = dict[str, Any]
type Report = dict[str, Any]
