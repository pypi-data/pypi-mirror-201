from __future__ import annotations

import logging
from typing import Optional

from aws_requests_auth.aws_auth import AWSRequestsAuth
from requests import Session

from thoughtful.supervisor.manifest import Manifest
from thoughtful.supervisor.reporting.status import Status
from thoughtful.supervisor.reporting.step_report import StepReport
from thoughtful.supervisor.streaming.payloads import ArtifactsUploadedPayload
from thoughtful.supervisor.streaming.payloads import BotManifestStreamingPayload
from thoughtful.supervisor.streaming.payloads import StatusChangePayload
from thoughtful.supervisor.streaming.payloads import StepReportStreamingPayload
from thoughtful.supervisor.streaming.payloads import StreamingPayload

logger = logging.getLogger(__name__)


class StreamingCallback(Session):
    def __init__(self, run_id: str, callback_url: str, aws_auth: AWSRequestsAuth):
        super().__init__()
        logger.info("testing")
        self.run_id = run_id
        self.callback_url = callback_url
        self.auth = aws_auth

    @classmethod
    def from_env_defaults(
        cls, auth: AWSRequestsAuth, run_id: str, callback_url: str
    ) -> Optional[StreamingCallback]:
        if run_id and callback_url:
            return cls(run_id=run_id, callback_url=callback_url, aws_auth=auth)
        logger.warning("Missing job id or callback url values")

    def post(self, payload: StreamingPayload, **kwargs):
        message_json = payload.__json__()
        timeout_seconds = 10

        try:
            logger.info("Posting streaming message")
            logger.info("URL: %s", self.callback_url)
            logger.info("Payload: %s", message_json)
            response = super().post(
                self.callback_url, json=message_json, timeout=timeout_seconds, **kwargs
            )
        except Exception:
            # A failed stream message shouldn't break a bot, so catch any possible
            # exception and log it
            logger.exception("Could not post step payload to endpoint")
            return

        if not response.ok:
            logger.error(
                f"Received BAD response: ({response.status_code}) {response.text}"
            )
        logger.info(f"Received OK response: ({response.status_code}): {response.text}")
        return response

    def post_step_update(self, report: StepReport):
        logger.info(f"Posting step update id={report.step_id} status={report.status}")
        return self.post(StepReportStreamingPayload(report, self.run_id))

    def post_manifest(self, manifest: Manifest):
        return self.post(BotManifestStreamingPayload(manifest, self.run_id))

    def post_artifacts_uploaded(self, output_uri: str):
        return self.post(
            ArtifactsUploadedPayload(
                run_id=self.run_id, output_artifacts_uri=output_uri
            )
        )

    def post_status_change(self, status: Status):
        return self.post(StatusChangePayload(run_id=self.run_id, status=status))
