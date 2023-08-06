import importlib.metadata
import os

from functional_cat.io import MODELS_CACHE_PATH

try:
    __version__ = importlib.metadata.version("functional-cat")
except importlib.metadata.PackageNotFoundError:
    __version__ = ""

if not os.path.exists(MODELS_CACHE_PATH):
    os.makedirs(MODELS_CACHE_PATH)
