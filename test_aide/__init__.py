from ._version import __version__

from . import classes
from . import functions

try:
    from . import equality
except ImportError:
    pass

try:
    from . import pandas
except ImportError:
    pass
