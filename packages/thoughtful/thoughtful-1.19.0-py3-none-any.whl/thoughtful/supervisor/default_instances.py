"""
Default instances for dynamic runs.

Typically, developers will only run one digital worker on a Python
runtime, and it is tricky to initialize an object and pass that object
instance down into other files in a project for a custom decorator.
This package provides a set of default instances of objects and contexts
for dynamic runs.

This file initializes a shared `ReportBuilder` and `Recorder` for
individual steps and sub steps to share, then creates:

    - a default ``MainContext`` named ``supervise``,
    - a decorator to annotate steps called ``step``,
    - a ``StepContext`` named ``step_context``,
    - a function to set step statuses called ``set_step_status``,
    - and a function to set record statuses called ``set_record_status``.

See the quickstart for, well, quickstarts on each of these methods.
"""

import logging
import pathlib
import warnings
from typing import Optional, Union
from urllib.parse import urlparse

import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth

from thoughtful.supervisor.environment_variables import EnvironmentVariables
from thoughtful.supervisor.main_context import MainContext
from thoughtful.supervisor.manifest import Manifest
from thoughtful.supervisor.recorder import Recorder
from thoughtful.supervisor.reporting.report_builder import ReportBuilder
from thoughtful.supervisor.step_context import StepContext
from thoughtful.supervisor.step_decorator_factory import create_step_decorator
from thoughtful.supervisor.streaming.callback import StreamingCallback

logger = logging.getLogger(__name__)
env_vars = EnvironmentVariables()

# If callback url is in environment, we will stream to that url
streaming_callback: Optional[StreamingCallback] = None
if env_vars.callback_url and env_vars.run_id:
    credentials = boto3.Session().get_credentials()
    host = urlparse(env_vars.callback_url).hostname
    aws_auth = AWSRequestsAuth(
        aws_access_key=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        aws_token=credentials.token,
        aws_host=host,
        aws_region="us-east-1",
        aws_service="execute-api",
    )
    streaming_callback = StreamingCallback.from_env_defaults(
        auth=aws_auth, run_id=env_vars.run_id, callback_url=env_vars.callback_url
    )
else:
    logger.warning("Missing ENV variable for callback url or job id")

#: A shared ``ReportBuilder`` for steps and step contexts to add step reports
#: to.
report_builder = ReportBuilder()

#: A shared ``Recorder`` for steps and step contexts to record messages to.
recorder = Recorder()

#: Use this decorator on your own functions to mark what workflow step each
#: Python function is matched to.
step = create_step_decorator(report_builder, recorder, streaming_callback)

#: Use this function to mark a step as failed.
#: This is just a shortcut for ``set_step_status(step_id, "failed")``.
#: Exposes ``report_builder.fail_step``.
fail_step = report_builder.fail_step

#: Expose the report builder's ability to override a step's status as a
#: top-level call. Exposes ``report_builder.set_step_status``.
set_step_status = report_builder.set_step_status

#: Expose the report builder's ability to override a step's record's status as a
#: top-level call. Exposes ``report_builder.set_record_status``.
set_record_status = report_builder.set_record_status

#: Expose the report builder's ability to override a run's status as a
#: top-level call. Exposes ``report_builder.set_run_status``.
set_run_status = report_builder.set_run_status


# noinspection PyPep8Naming
class step_scope(StepContext):
    """
    It's a context manager that provides a scope for a step using the
    aforementioned default instances of ``report_builder`` and ``recorder``.
    """

    def __init__(self, *step_id, record_id: Optional[str] = None):
        """
        A default `StepContext` that uses the root level `report_builder` and
        `recorder`.

        Args:
            *step_id: The list of integers that represent the step ID.
            record_id: An optional ID of the record being actively processed
        """
        super().__init__(
            report_builder,
            recorder,
            *step_id,
            streaming_callback=streaming_callback,
            record_id=record_id,
        )


# noinspection PyPep8Naming
class substep(step_scope):
    """
    The deprecated version of ``step_scope``.
    """

    def __init__(self, *step_id):
        warnings.warn(
            f"`{self.__class__.__name__}` has been renamed to `step_scope`. "
            f"Please use that class name instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*step_id)


# noinspection PyPep8Naming
class supervise(MainContext):
    """
    It's a context manager that provides a scope for the main context using the
    aforementioned default instances of ``report_builder`` and ``recorder``.
    """

    def __init__(
        self,
        manifest: Union[Manifest, str, pathlib.Path] = "manifest.yaml",
        output_dir: Union[str, pathlib.Path] = "output/",
        *args,
        **kwargs,
    ):
        """
        A default `MainContext` that uses the root level `report_builder` and
        `recorder`.

        Args:
            *args: Extra arguments to the `MainContext` constructor.
            **kwargs: Extra keyword arguments to the `MainContext` constructor.
            manifest (str): The digital worker's manifest definition
            output_dir (str): Where the work report and drift report will
                be written to
        """
        super().__init__(
            report_builder=report_builder,
            recorder=recorder,
            manifest=manifest,
            output_dir=output_dir,
            upload_uri=env_vars.s3_bucket_uri,
            streaming_callback=streaming_callback,
            *args,
            **kwargs,
        )
