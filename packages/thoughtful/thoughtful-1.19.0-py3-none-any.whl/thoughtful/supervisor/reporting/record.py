"""
This module contains the ``Record`` class, a non-user facing class that is used
to store information about a step's record. This class is represented in the
run report as a json object.

.. code-block:: json

    {
        "workflow": [
            {
                "step_id": "1.1",
                "step_status": "succeeded",
                "record": {
                    "id": "1",
                    "status": "succeeded"
                }
            }
        ]
    }

"""

from dataclasses import dataclass

from thoughtful.supervisor.reporting.status import Status


@dataclass
class Record:
    """
    A record can refer to any object that is being processed by a step. It
    is here represented by its ID and its status.
    """

    record_id: str
    """
    str: The status of the record.
    """

    status: Status
    """
    Status: The status of the record.
    """

    def __json__(self):
        return {
            "id": self.record_id,
            "status": self.status.value,
        }
