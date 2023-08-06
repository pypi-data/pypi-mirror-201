"""
Infrastructure for automatically running sciagraph based on an environment
variable, and for automatic initialization on startup.
"""

import os
import sys
import logging
from ctypes import PyDLL, py_object


def _load_module(name: str):
    """Load a Python module from the pre-loaded Sciagraph shared library."""
    if name in sys.modules:
        return sys.modules[name]
    # The symbols in the current running process:
    this = PyDLL(None)
    try:
        f = getattr(this, f"PyInit_{name}")
    except AttributeError:
        # We're not running under Sciagraph:
        return None
    f.restype = py_object
    module = f()
    sys.modules[name] = module
    return module


def check_user_configured_mode_via_env_var():
    """
    Translate a SCIAGRPAH_MODE environment variable into the relevant
    ``python -m sciagraph`` command-line options.

    This will run in the original process started by the user.
    """
    mode = os.environ.pop("SCIAGRAPH_MODE", None)
    if mode is None:
        return
    if mode not in {"process", "api", "celery"}:
        logging.error(
            "The SCIAGRAPH_MODE environment variable only supports the values"
            f" 'process' and 'api', but you set it to {mode!r}, exiting."
        )
        os._exit(1)

    import ctypes

    # TODO: Python 3.10 and later have sys.orig_argv.
    _argv = ctypes.POINTER(ctypes.c_wchar_p)()
    _argc = ctypes.c_int()
    ctypes.pythonapi.Py_GetArgcArgv(ctypes.byref(_argc), ctypes.byref(_argv))
    argv = _argv[: _argc.value]
    args = [f"--mode={mode}", "run"] + argv[1:]
    from .__main__ import main

    try:
        main(args)
    except SystemExit as e:
        if len(e.args) == 1 and isinstance(e.args[0], str):
            sys.stderr.write(e.args[0] + "\n")
            sys.stderr.flush()
            os._exit(1)
        raise


def check_if_we_need_initialization():
    """
    Check how and if we need to initialize Sciagraph, and do the needful.

    This will run in the final, runtime process created by
    ``python -m sciagraph run``.
    """
    try:
        _check_if_we_need_initialization()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.stderr.flush()
        os._exit(1)


def _check_if_we_need_initialization():
    # __SCIAGRAPH_INITIALIZE is set in __main__.py:
    value = os.environ.pop("__SCIAGRAPH_INITIALIZE", None)
    if value is None:
        return

    setup_module = _load_module("_sciagraph_setup")
    if setup_module is None and sys.platform == "darwin":
        print(
            """\
Loading Sciagraph failed. This is likely because you're using the system Python
built-in to macOS, which due to security restrictions can't be used with
Sciagraph.

To use Sciagraph, please switch to a version of Python installed via Homebrew,
pyenv, macports, or some other version that isn't the one built-in one.

If that is not the issue, please email support@sciagraph.com"""
        )
        os._exit(1)

    if setup_module is None:
        print("Sciagraph failed to load, please email support@sciagraph.com")
        os._exit(1)

    InitializationMode = setup_module.InitializationMode
    sciagraph_initialize = setup_module.sciagraph_initialize

    if value == "process":
        # TODO Currently re-used for spawned child processes, regardless of
        # parent mode... maybe want a child mode.
        sciagraph_initialize(InitializationMode.ParentProcessSingleJob)
        return

    if value == "api":
        sciagraph_initialize(InitializationMode.ParentProcessMultipleJobs)
        return

    if value == "celery":
        # The parent worker process should _not_ run Sciagraph. We want only
        # child processes (the prefork pool) to do so... and we don't want
        # _their_ children to register, either.
        def initialize_only_once(initialized=[]):
            """
            Only initialize once, and not again in worker subprocesses that do
            another fork() 😱.
            """
            if initialized:
                return
            initialized.append(True)
            sciagraph_initialize(InitializationMode.ParentProcessMultipleJobs)

        os.register_at_fork(after_in_child=initialize_only_once)
        return

    if value == "jupyter":
        # Note that we are running in Jupyter mode, presumably via a Jupyter kernel.
        from .integrations._ipython import sciagraph_kernel_installed

        sciagraph_kernel_installed()

        # Initialize Sciagraph but do _not_ do a licensing check yet, it'll
        # happen later.
        sciagraph_initialize(InitializationMode.ParentProcessMultipleJobs, False)
        return

    logging.error(f"__SCIAGRAPH_INITIALIZE is {value}, this is a bug.")
    os._exit(1)
