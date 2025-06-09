try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # type: ignore

from schwifty.bban import BBAN
from schwifty.bic import BIC
from schwifty.iban import IBAN


__all__ = [
    "BBAN",
    "BIC",
    "IBAN",
]
__version__ = version(__name__)
