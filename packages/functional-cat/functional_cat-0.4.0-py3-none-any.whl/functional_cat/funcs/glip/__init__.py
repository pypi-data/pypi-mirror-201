try:
    import glip  # noqa: F401
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        f"`functional-cat` was not installed with GLIP support so the module `{__name__}` cannot be used. "
        "Please run `pip install functional-cat[glip]` to install."
    )

from .glip import GLIP

__all__ = ["GLIP"]
