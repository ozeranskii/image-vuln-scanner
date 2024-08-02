from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ReportGenerator:
    def __init__(self, filename: str):
        self.filename = Path(filename)

    @staticmethod
    def generate_report(images: dict[str, dict[str, str]], scan_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        report: list[dict[str, Any]] = []

        for result in scan_results:
            image: str = result["image"]
            metadata: dict[str, str] = images[image]
            report.append(
                {
                    "resource_kind": metadata["resource_kind"],
                    "resource_name": metadata["resource_name"],
                    "image": image,
                    "vulnerabilities": result["vulnerabilities"],
                },
            )

        return report

    def save_report(self, report: list[dict[str, Any]]) -> None:
        with self.filename.open("w") as f:
            json.dump(report, f, indent=4)
