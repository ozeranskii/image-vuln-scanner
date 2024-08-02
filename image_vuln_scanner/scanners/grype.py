from __future__ import annotations

from typing import Any

from .base import BaseImageScanner


class GrypeImageScanner(BaseImageScanner):
    scan_command_template: str = "grype {image} -o json"

    @staticmethod
    def extract_vulnerabilities(scan_data: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "Severity": vulnerability["severity"],
                "VulnerabilityID": vulnerability["id"],
                "Status": vulnerability.get("fix", {}).get("state", "Unknown"),
                "PkgName": match["artifact"]["name"],
            }
            for match in scan_data["matches"]
            for vulnerability in [match["vulnerability"]]
        ]
