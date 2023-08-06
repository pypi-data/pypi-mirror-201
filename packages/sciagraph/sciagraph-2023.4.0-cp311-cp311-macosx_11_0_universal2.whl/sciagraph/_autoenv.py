"""
This will be automatically imported when any Python process starts up, via the
.pth file installed by Sciagraph, and it will automatically run the up-to-two
steps of initialization.
"""

from ._initialization import (
    check_if_we_need_initialization,
    check_user_configured_mode_via_env_var,
)


# In some cases users might start Sciagraph by setting an environment variable
# (SCIAGRAPH_MODE=process, say). Handle that case when a generic Python process
# starts:
check_user_configured_mode_via_env_var()

# Once a Python process is started with Sciagraph code pre-loaded (via
# LD_PRELOAD or equivalent), we need to do initialization before the user's
# code starts running. That happens here:
check_if_we_need_initialization()
