"""
IPython magic, specifically for Jupyter, allowing profiling from inside
a Jupyter notebook.
"""

import os
from typing import Optional, MutableMapping, Mapping
from pathlib import Path
from textwrap import indent
from uuid import uuid1
from html import escape as html_escape

from IPython.core.error import UsageError
from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
from IPython.display import HTML, display

from ..api import profile_job, _load_module
from .._utils import dirname_now

SCIAGRAPH_KERNEL_INSTALLED = False


def sciagraph_kernel_installed():
    """
    This will be called at startup (in _initialization.py) if 'jupyter' mode is
    being used.
    """
    global SCIAGRAPH_KERNEL_INSTALLED
    SCIAGRAPH_KERNEL_INSTALLED = True


def check_access_token(
    access_key: str, access_secret: str, environ: Mapping[str, str]
) -> bool:
    """
    Validate an access token, returning whether it succeeded, and a reason for
    failure if it did not validate.
    """
    module = _load_module("_sciagraph_setup")
    metadata = environ.get("SCIAGRAPH_ACCESS_METADATA", None)
    try:
        module.check_access_token(access_key, access_secret, metadata)
    except ValueError:
        return False
    return True


def ensure_token_loaded(
    username: Optional[str] = None, environ: MutableMapping[str, str] = os.environ
):
    """
    Make sure the Sciagraph access token environment variables are set, via
    ipython-secrets which utilizes the local OS keyring.

    While we don't have valid access tokens:

        a. Get access token from env variable. If validates, set_secret().
        b. If that failed, get secrets from get_secret()
        c. Try to validate
        d. If succeeded, great. If failed, clear get_secret(), go to (a).

    All arguments are there for testing purposes.
    """
    try:
        from ipython_secrets import get_secret, set_secret, delete_secret
    except ImportError:
        raise UsageError(
            "You need the `ipython_secrets` package to be installed to use Sciagraph "
            "with Jupyter. You can either `pip install sciagraph[jupyter]`, or "
            "manually install the package. For more details see "
            "https://www.sciagraph.com/docs/howto/jupyter/"
        )

    access_key: Optional[str] = None
    access_secret: Optional[str] = None

    while True:
        try:
            access_key = environ["SCIAGRAPH_ACCESS_KEY"]
            access_secret = environ["SCIAGRAPH_ACCESS_SECRET"]
        except KeyError:
            pass
        if (
            access_key is not None
            and access_secret is not None
            and check_access_token(access_key, access_secret, environ)
        ):
            break

        access_key = get_secret(
            "SCIAGRAPH_ACCESS_KEY",
            prompt="First, please enter the SCIAGRAPH_ACCESS_KEY for you account "
            + "(find it, or signup for free, at https://account.sciagraph.com/ui/): ",
            username=username,
        )
        access_secret = get_secret(
            "SCIAGRAPH_ACCESS_SECRET",
            prompt="Next, please enter the SCIAGRAPH_ACCESS_SECRET: ",
            username=username,
        )
        assert access_key is not None
        assert access_secret is not None
        if check_access_token(access_key, access_secret, environ):
            break
        else:
            delete_secret("SCIAGRAPH_ACCESS_KEY", username=username)
            delete_secret("SCIAGRAPH_ACCESS_SECRET", username=username)
            environ.pop("SCIAGRAPH_ACCESS_KEY", None)
            environ.pop("SCIAGRAPH_ACCESS_SECRET", None)

    try:
        set_secret("SCIAGRAPH_ACCESS_KEY", access_key, username=username)
        set_secret("SCIAGRAPH_ACCESS_SECRET", access_secret, username=username)
    except Exception as e:
        display(f"Failed to permanently store access token: {e}")

    # Set the environment variables that will be used during initialization.
    environ["SCIAGRAPH_ACCESS_KEY"] = access_key
    environ["SCIAGRAPH_ACCESS_SECRET"] = access_secret


HOPEFULLY_UNIQUE_VAR = "__arghXKYbldsada__"

# We use a variable that is unlikely to conflict with user code as the name of
# the profiling function. We also:
#
# 1. Make sure line numbers line up with original code (first line is a magic,
#    so we can put stuff there!)
# 2. Make sure user code runs in a function, so top-level lines get recorded.
# 3. __magic_sciagraph_profile() will return its locals, so that we can update
#    the globals appropriately.
TEMPLATE = """\
def __magic_sciagraph_profile():
{}
globals().update(%s(__magic_sciagraph_profile))
del __magic_sciagraph_profile
del %s
""" % (
    HOPEFULLY_UNIQUE_VAR,
    HOPEFULLY_UNIQUE_VAR,
)


@magics_class
class SciagraphMagics(Magics):
    """Magics for profiling."""

    @line_magic
    def sciagraph_reset_token(self, line=None, cell=None):
        """Clear the current access key and secret."""
        from ipython_secrets import delete_secret

        delete_secret("SCIAGRAPH_ACCESS_KEY")
        delete_secret("SCIAGRAPH_ACCESS_SECRET")
        os.environ.pop("SCIAGRAPH_ACCESS_KEY")
        os.environ.pop("SCIAGRAPH_ACCESS_SECRET")

    @cell_magic
    def sciagraph_profile(self, line, cell):
        """Memory profile the code in the cell."""
        # Inject run_with_profile:
        self.shell.push({HOPEFULLY_UNIQUE_VAR: run_with_profile})

        # Pre-process the code:
        cell = self.shell.transform_cell(cell) + "\nreturn locals()"

        # Generate the code.
        #
        # We use a template that does the Sciagraph setup inside the cell, rather
        # than here, so as to keep a whole pile of irrelevant IPython code
        # appearing as frames at the top of the profiling graphs.
        #
        # Empirically inconsistent indents are just fine as far as Python is
        # concerned(?!), so we don't need to do anything special for code that
        # isn't 4-space indented.
        self.shell.run_cell(TEMPLATE.format(indent(cell, "    ")))

        # Uninject run_with_profile:
        self.shell.drop_by_id({HOPEFULLY_UNIQUE_VAR: run_with_profile})


def run_with_profile(function_to_profile):
    """Run some code under Sciagraph, display result."""
    top_dir = Path("sciagraph-result")
    if not top_dir.exists():
        top_dir.mkdir()

    report_dir = top_dir / dirname_now()
    report_id = str(uuid1())
    try:
        with profile_job(report_id, report_dir):
            return function_to_profile()
    finally:
        report_path = report_dir / "index.html"
        if report_path.exists():
            display_report(report_id, report_dir)


def display_report(report_id: str, report_dir: Path):
    """Display a report in the notebook."""
    report_html = html_escape(
        '<base href="__SCIAGRAPH_REPLACE_ME__">'
        + (report_dir / "index.html").read_text(),
        quote=True,
    )

    display(
        HTML(
            f'<img id="{report_id}" src="{report_dir}/peak-memory.svg" style="display: none;" width="0" height="0">'  # noqa: E501
        )
    )
    display(
        HTML(
            f'<iframe id="{report_id}-iframe" srcdoc="{report_html}" width="100%" height="900">'  # noqa: E501
            + "</iframe></html>"
            + (
                """<script>
            (function() {
                var img = document.getElementById("%s");
                var base_url = img.src.split("peak-memory.svg")[0];
                var iframe = document.getElementById("%s-iframe");
                iframe.srcdoc = iframe.srcdoc.replace("__SCIAGRAPH_REPLACE_ME__",
                                                      base_url);
                iframe.onload = function() {
                    iframe.style.height = (
                        iframe.contentWindow.document.body.scrollHeight + 'px');
                };
            })();
            """
                % (report_id, report_id)
            )
        )
    )
