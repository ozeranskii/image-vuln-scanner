from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from .k8s.client import KubernetesClient
from .k8s.extractor import ResourceImageExtractor
from .report.generator import ReportGenerator
from .scanners.grype import GrypeImageScanner
from .scanners.trivy import TrivyImageScanner

if TYPE_CHECKING:
    from .scanners.base import BaseImageScanner


class ImageScanningService:
    scanner_classes: ClassVar[dict[str, type[BaseImageScanner]]] = {
        "trivy": TrivyImageScanner,
        "grype": GrypeImageScanner,
    }

    def __init__(
        self,
        namespace: str,
        label_selector: str,
        output_file: str,
        scanner_type: str,
        max_concurrent_tasks: int = 4,
    ):
        self.namespace = namespace
        self.label_selector = label_selector
        self.output_file = output_file
        self.max_concurrent_tasks = max_concurrent_tasks
        self.scanner = self.scanner_classes[scanner_type](max_concurrent_tasks=self.max_concurrent_tasks)

    async def run(self) -> None:
        k8s_client = KubernetesClient(self.namespace)
        resources = await k8s_client.get_resources(self.label_selector)

        image_extractor = ResourceImageExtractor()
        images = image_extractor.get_images(resources)

        scan_results = await self.scanner.scan_images(images)

        report_generator = ReportGenerator(self.output_file)
        report = report_generator.generate_report(images, scan_results)
        report_generator.save_report(report)

    async def shutdown(self) -> None:
        await self.scanner.shutdown()
