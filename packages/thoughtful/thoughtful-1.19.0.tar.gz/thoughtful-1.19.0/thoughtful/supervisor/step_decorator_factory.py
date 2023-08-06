"""
This module contains the functions necessary to fuel the step decorator
factory function ``create_step_decorator``. This step decorator—``@step``—is
used to supervise the execution of a function in a digital worker.

.. code-block:: python

    from thoughtful.supervisor import supervise, step

    @step("1.1")
    def times_two(integers: list) -> None:
        return integers * 2

    @step("1.2")
    def times_three(integer: int) -> None:
        return integer * 3

    def main():
        num_list = [1, 2, 3, 4, 5]

        num_list = times_two(num_list)

        for num in num_list:
            num = times_three(num)

    if __name__ == '__main__':
        with supervise():
            main()

The decorator produced by the factory does not have any immediate support for
records, nor for setting the step status like the step context does. However,
some helpers have been implemented to simulate this functionality. For the
record IDs, the decorator will look for a function kwarg called
``supervisor_record_id`` and use that as the record ID.

.. code-block:: python

    @step("1.2")
    def times_three(integer: int, supervisor_record_id: str = None) -> None:
        return integer * 3

    num = times_three(3, supervisor_record_id=str(3))

As for the step status, a helper function, ``set_step_status``, has been
implemented to set the status of a step.

.. code-block:: python

    @step("1.1")
    def times_two(integers: list) -> None:
        return integers * 2

    num_list = [1, 2, 3, 4, 5]
    num_list = times_two(num_list)
    set_step_status("1.1", "warning")
"""

from __future__ import annotations

import contextlib
import functools
import json
import logging
import warnings
from typing import Any, Callable, Dict, List, Optional

from thoughtful.supervisor.recorder import Recorder
from thoughtful.supervisor.reporting.report_builder import ReportBuilder
from thoughtful.supervisor.reporting.report_builder import StepReportBuilder
from thoughtful.supervisor.reporting.status import Status
from thoughtful.supervisor.reporting.timer import Timer
from thoughtful.supervisor.streaming.callback import StreamingCallback


def create_step_decorator(
    report_builder: ReportBuilder,
    recorder: Recorder,
    streaming_callback: StreamingCallback = None,
) -> Callable:
    """
    A step decorator generator that as input receives a ``ReportBuilder``
    object and a ``Recorder`` object. The returned decorator will use these
    objects to record the execution of the decorated function.

    Note that the return type here is `Any`, because proper type hinting
    for decorators is not yet obvious. PEP 612 specifies a way to type
    hint decorators starting in 3.10, but this project supports >= 3.7. See
    more here: https://stackoverflow.com/a/68290080/2597913.

    Args:
        report_builder (ReportBuilder): The report builder to use to record
            the execution of the decorated function.
        recorder (Recorder): The recorder to use to record the execution of
            the decorated function.
        streaming_callback (StreamingCallback, optional): If set, streams
            the status of work report steps to that callback handler.
            Defaults to `None`.

    Returns:
        Any: A decorator to attach to functions.
    """

    # The decorator to be returned as the property
    # This handles the inputs to the decorator itself
    def returned_decorator(*step_id):
        """
        A decorator to mark a function as the implementation of a step in a
        digital worker's manifest.

        To include a `supervisor_record_id`, pass it to the decorated function
        as a kwarg. For example,
        ```
            @step(1)
            def my_func(*args, supervisor_record_id: str):
                do stuff
                ...

            my_func(supervisor_record_id="my_record_id")
        ```
        """
        step_id = _step_id_from_args(step_id)

        # The decorator to grab the function callable itself
        def inner_decorator(fn):
            # And the wrapper around the function to call it with its
            # args and kwargs arguments
            @functools.wraps(fn)
            def wrapper(*fn_args, **fn_kwargs):
                return _run_wrapped_func(
                    fn,
                    step_id,
                    report_builder,
                    recorder,
                    streaming_callback,
                    *fn_args,
                    **fn_kwargs,
                )

            return wrapper

        return inner_decorator

    return returned_decorator


def _run_wrapped_func(
    fn: Callable,
    step_id: str,
    report_builder: ReportBuilder,
    recorder: Recorder,
    streaming_callback: StreamingCallback,
    *fn_args: Optional[Any],
    **fn_kwargs: Optional[Any],
) -> Any:
    """
    Runs `fn` with the given args `args` and `kwargs`, times how long it
    takes to run, and records the execution of this function under `step_id`
    in the work report.

    Args:
        fn (Callable): The function to run.
        step_id (str): The ID of the step representing the function to
        execute.
        *args (List[Any]): The input arguments to the function.
        **kwargs (Dict[str, Any]): The input keyword arguments to the function.

    Returns:
    Any: Whatever is returned by executing the function
    """

    """Set up the step"""
    caught_exception: Optional[Exception] = None
    final_status: Status

    # Time the function
    func_timer = Timer()
    func_timer.start()

    this_steps_report_builder = StepReportBuilder(
        step_id=step_id,
        start_time=func_timer.start_time,
        end_time=None,
        status=Status.RUNNING,
        message_log=recorder.messages,
        data_log=recorder.data,
    )

    # Initialize the record if an ID was provided
    if record_id := fn_kwargs.get("supervisor_record_id"):
        warnings.warn(
            "Using `record_id` in an @step function is deprecated and will be "
            "removed in a later release. Use `set_record_status` instead.",
            DeprecationWarning,
            stacklevel=3,
        )
        this_steps_report_builder.set_record_status(record_id, Status.RUNNING)

    if streaming_callback:
        for report in this_steps_report_builder.to_reports():
            streaming_callback.post_step_update(report)

    """Run the step"""
    try:
        fn_result = fn(*fn_args, **fn_kwargs)
        final_status = Status.SUCCEEDED
    except Exception as ex:
        fn_result = None
        caught_exception = ex
        final_status = Status.FAILED
    timer_result = func_timer.end()

    """Step teardown"""
    if record_id:
        this_steps_report_builder.set_record_status(record_id, final_status)

    # Finish the report
    this_steps_report_builder.end_time = timer_result.end
    this_steps_report_builder.status = final_status
    this_steps_report_builder.message_log = recorder.messages
    this_steps_report_builder.data_log = recorder.data
    report_builder.step_report_builders.append(this_steps_report_builder)

    if streaming_callback:
        for report in this_steps_report_builder.to_reports():
            streaming_callback.post_step_update(report)

    # Reset the recorder for the next step
    recorder.messages = []
    recorder.data = []

    """Passthrough the step's return value or raised exception"""
    # If the step failed and raised an exception, raise that instead
    # of returning None
    if caught_exception:
        raise caught_exception

    # Passthrough the function's returned data back up
    return fn_result


def _step_id_from_args(args: tuple) -> str:
    """
    Joins decorator number args into a step ID string. This was more necessary
    when the user was expected to pass in a series of integers as the step ID,
    but now it's just a string. This is still here for backwards compatibility.

    For example,
    ```
        @step(1, 2, 3)
        def my_func():
            ...
    ```
    would return "1.2.3".


    Args:
        args (tuple): The arguments to the decorator.

    Returns:
        str: The step ID.
    """
    if len(args) > 1:
        warnings.warn(
            "Passing multiple step ids to StepContext is deprecated. "
            "Instead, pass a single step id string with dots, ie '1.1'",
            DeprecationWarning,
            stacklevel=3,
        )

    return ".".join([str(arg) for arg in args])


def to_safe_jsonable(value: Any) -> Any:
    """
    Returns a version of `value` that can be converted into JSON
    format using the `json` library.

    Args:
        value: The value to ensure is safe to JSON serialize.

    Returns:
        Any: The JSON safe value
    """
    # If the standard JSON library knows how to encode the object,
    # go with that
    with contextlib.suppress(TypeError):
        json.dumps(value)
        return value
    # Otherwise, check if the object has a .__json__() method
    json_attribute = getattr(value, "__json__", None)
    if callable(json_attribute):
        try:
            return value.__json__()
        except Exception:
            # [CX-234] If the call fails, warn and continue trying other options
            logging.warning("__json__ method raised exception", exc_info=True)

    # Use the raw string as a last resort
    return str(value)
