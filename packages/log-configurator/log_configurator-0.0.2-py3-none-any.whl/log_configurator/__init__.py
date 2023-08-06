"""
Provides the top-level load function to users without having to import the loader explicitly.
Additionally, this hides internal functions of the loader.
"""
from .configurator import setup_root_logger, buffer_log  # NOQA: F401
