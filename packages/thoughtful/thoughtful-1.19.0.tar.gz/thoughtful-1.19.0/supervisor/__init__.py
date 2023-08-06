# isort: skip_file due to the importance of the python parsing order of these
# modules

from warnings import warn

from thoughtful.supervisor import *  # noqa

warn(
    "Using `import supervisor` is deprecated and will be removed in the future."
    " Please use `import thoughtful.supervisor` instead.",
    DeprecationWarning,
    stacklevel=2,
)
