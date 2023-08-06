"""
Sciagraph, the production memory profiler for scientists and data scientists.

This is proprietary software.
"""
try:
    from importlib.metadata import version  # type: ignore
except ImportError:
    from importlib_metadata import version  # type: ignore

__version__ = version("sciagraph")
del version


def load_ipython_extension(ipython):
    """Load our IPython magic, initializing Scigraph along the way."""
    from IPython.core.error import UsageError
    from .integrations._ipython import (
        SCIAGRAPH_KERNEL_INSTALLED,
        SciagraphMagics,
        ensure_token_loaded,
    )
    from ._initialization import _load_module

    if not SCIAGRAPH_KERNEL_INSTALLED:
        raise UsageError(
            "In order to use Sciagraph, you need to run your notebook with the "
            "Sciagraph kernel.\n\n"
            'You can change the kernel by going to the "Kernel" menu, '
            'choosing "Change Kernel...", and then selecting the '
            '"Python 3 with Sciagraph" kernel.'
        )

    ensure_token_loaded()
    _load_module("_sciagraph_setup").validate_licensing()
    ipython.register_magics(SciagraphMagics)
