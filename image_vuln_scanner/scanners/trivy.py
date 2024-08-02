from __future__ import annotations

from typing import Any

from .base import BaseImageScanner


class TrivyImageScanner(BaseImageScanner):
    scan_command_template: str = "trivy image --quiet --format json {image}"

    @staticmethod
    def extract_vulnerabilities(scan_data: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "Severity": vulnerability["Severity"],
                "VulnerabilityID": vulnerability["VulnerabilityID"],
                "Status": vulnerability.get("Status", "Unknown"),
                "PkgName": vulnerability["PkgName"],
            }
            for result in scan_data["Results"]
            for vulnerability in result.get("Vulnerabilities", [])
        ]
