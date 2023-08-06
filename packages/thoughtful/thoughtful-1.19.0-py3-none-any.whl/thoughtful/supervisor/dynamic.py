"""
This file is a deprecated way of getting supervisor objects.

Previously, there were two patterns of using supervisor: one was dynamic with
`supervise()`, and one was non-dynamic with `Supervisor()` and `DigitalWorker()`.

Now, there is only one pattern--dynamic--and so all of that code under the old
`dynamic/` folder is moved to the top level, because it's all that's left.

This file adds backwards compatibility for older code that uses

```
from thoughtful.supervisor.dynamic import ...
```
"""

# These are the imports to make "from thoughtful.supervisor.dynamic import ..." backwards
# compatible

import warnings

from thoughtful.supervisor.default_instances import *  # noqa

warnings.warn(
    "Using `from thoughtful.supervisor.dynamic import ...` is deprecated and "
    "will be removed in the future. You should use `from thoughtful.supervisor "
    "import ...` instead.",
    DeprecationWarning,
)
