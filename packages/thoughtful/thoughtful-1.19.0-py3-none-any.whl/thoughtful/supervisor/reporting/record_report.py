from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

from thoughtful.supervisor.reporting.record import Record
from thoughtful.supervisor.reporting.status import Status
from thoughtful.supervisor.reporting.step_report import StepReport


@dataclass
class RecordReport(StepReport):
    # Because this class inherits from another dataclass, we need to set a
    # default value for the record field. So use a lambda to create a new
    # mock Record instance.
    record: Record = field(
        default_factory=lambda: Record(record_id="n/a", status=Status.SUCCEEDED)
    )

    @classmethod
    def from_step_report(cls, step_report: StepReport, record: Record) -> RecordReport:
        return cls(
            start_time=step_report.start_time,
            end_time=step_report.end_time,
            step_id=step_report.step_id,
            status=step_report.status,
            message_log=step_report.message_log,
            data_log=step_report.data_log,
            record=record,
        )

    def __json__(self) -> Dict[str, Any]:
        return {
            **super().__json__(),
            "record": self.record.__json__(),
        }
