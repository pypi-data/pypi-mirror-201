"""
This module contains the Recorder class. This class is responsible for
recording data and logs from the digital worker.

.. code-block:: python

    from thoughtful.supervisor import recorder, step, supervise


    @step("1.1")
    def do_something():
        try:
            ...  # do something
        except Exception as e:
            recorder.record_message(f"Something went wrong: {e}")


    def main():
        do_something()

        recorder.record_message("This is a message")


    if __name__ == "__main__":
        with supervise():
            main()

See more detailed examples below.
"""
from copy import deepcopy
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from warnings import warn

MessageLog = List[str]
DataLog = List[Dict[str, Any]]


class Recorder:
    def __init__(self):
        """
        Logs messages, data, and changes to data during a ``DigitalWorker``
        execution.

        Attributes:
            self.data (list): Data logs.
            self.messages (list): A list of log messages.
        """

        self.data: DataLog = []
        self.messages: MessageLog = []

    def copy_logs(self) -> Tuple[MessageLog, DataLog]:
        """
        Creates deep copies of the logs recorded by this instance.

        Returns:
            Tuple[MessageLog, DataLog]: The log deep copies.
        """
        messages_copy: MessageLog = deepcopy(self.messages)
        data_copy: DataLog = deepcopy(self.data)
        return messages_copy, data_copy

    def record_data(
        self, log_data: any, label: str, description: Optional[str] = None
    ) -> any:
        """
        Log a piece of data for a step that's running.

        Examples:
            .. highlight:: python
            .. code-block:: python

                recorder = Recorder()
                recorder.record_data_change("Ticket#123",
                                             label="Support Ticket",
                                             description="The support ticket being used")

            .. code-block:: json

                "workflow": [
                    {
                    "step_id": "1.2.3",
                    "data_log": {
                        "type": "data",
                        "data": "Ticket#123",
                        "title": "Support Ticket",
                        "description": "The support ticket being used"
                    }
                ]

        Args:
            log_data (any): The data object to record, such as a string or dict.
            label (str): The name for the data object.
            description (str, optional): The description for the data, if any.

        Returns:
            any: The `log_data`.
        """
        warn(
            "The Recorder class is deprecated. Please remove any calls to a Recorder instance.",
            DeprecationWarning,
            stacklevel=2,
        )

        new_entry = {
            "type": RecordType.DATA,
            "data": log_data,
            "label": label,
            "description": description,
        }

        # Cache the record (flushed at end of step execution)
        self.data.append(new_entry)

        # Return the original data
        return log_data

    def record_data_change(
        self,
        before: any,
        after: any,
        label: str,
        description: Optional[str] = None,
    ) -> any:
        """
        Record a change in data.

        Args:
            before (any): The data before the transformation.
            after (any): The data after the transformation.
            label: (str): The name for the data log.
            description (str, optional): The description for the data, if any.

        Example:
            .. highlight:: python
            .. code-block:: python

                recorder = Recorder()
                me = "Dave Arel"
                recorder.record_data_change(me,
                                            me.upper(),
                                            label="Uppercased My Name",
                                            description="Capitalizes my full name")

            .. code-block:: json

                "workflow": [
                    {
                    "step_id": "1.2.3",
                    "data_log": {
                        "type": "transformed",
                        "before": "Dave Arel",
                        "after": "DAVE AREL",
                        "label": "Uppercased Name",
                        "description": "Capitalizes the full name"
                    }
                ]

        Returns:
            any: The data from `before`.
        """
        warn(
            "The Recorder class is deprecated. Please remove any calls to a Recorder instance.",
            DeprecationWarning,
            stacklevel=2,
        )

        transformation = {
            "type": RecordType.TRANSFORMATION,
            "before": before,
            "after": after,
        }
        self.record_data(transformation, label=label, description=description)
        return before

    def record_message(self, message: str) -> None:
        """
        Record a simple message.

        Args:
            message (str): The message to record.

        Examples:
            .. highlight:: python
            .. code-block:: python

                recorder = Recorder()
                recorder.record_data_change("message")

            .. code-block:: json

                "workflow": [
                    {
                    "step_id": "1.2.3",
                    "message_log": ["message"]
                ]

        Returns:
            None
        """
        warn(
            "The Recorder class is deprecated. Please remove any calls to a Recorder instance.",
            DeprecationWarning,
            stacklevel=2,
        )

        # Cache the record (flushed at end of step execution)
        self.messages.append(message)


class RecordType(str, Enum):
    """
    Enum for the different types of manually recorded data structures. **This is
    not to be confused with the records referred to by the record IDs in the
    steps and step contexts.** Those records use the regular ``Status`` enum and
    are not tied in with this enum.

    Data structures of these types must be serializable.

    Transformed data structures can be a string, number, object or list
    of the former, as long as the data is serializable. This could be as
    simple as a string being capitalized, trimmed, edited, etc., or it
    can be as complex as a large tabular data set cleaned up to
    remove duplicates.

    This should be used as a way to record a transformation of data within a
    step so that the data can later be consumed in different ways, such as a
    visual-diff data coming out, or debugging to diagnose whether the problem
    was the data going in or the data going out.
    """

    DATA = "data"
    """A record that is simply recording a static data value"""

    TRANSFORMATION = "transformation"
    """A record that is a step_outputs of data being transformed"""


if __name__ == "__main__":
    r = Recorder()
    r.record_data(
        "Ticket#123",
        label="Support Ticket",
        description="The support ticket being used",
    )
