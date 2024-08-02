from __future__ import annotations

import asyncio
import json
from typing import Any

from tqdm.asyncio import tqdm


class BaseImageScanner:
    scan_command_template: str

    def __init__(self, max_concurrent_tasks: int = 4) -> None:
        self.semaphore: asyncio.Semaphore = asyncio.Semaphore(max_concurrent_tasks)
        self.active_tasks: list[asyncio.Task] = []

    def get_scan_command(self, image: str) -> str:
        return self.scan_command_template.format(image=image)

    async def scan_image(self, image: str, progress_bar: tqdm) -> tuple[str, dict[str, Any] | None]:
        async with self.semaphore:
            scan_command: str = self.get_scan_command(image)
            proc: asyncio.subprocess.Process = await asyncio.create_subprocess_shell(
                scan_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            if proc.returncode != 0:
                return image, None
            scan_data: dict[str, Any] = json.loads(stdout.decode())
            progress_bar.update(1)
            return image, scan_data

    async def scan_images(self, images: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
        tasks: list[asyncio.Task] = []
        total_images: int = len(images)

        with tqdm(
            total=total_images,
            desc="Scanning images",
            unit="image",
            leave=True,
            position=0,
        ) as pbar:
            for image in images:
                task: asyncio.Task = asyncio.create_task(self.scan_image(image, pbar))
                tasks.append(task)
                self.active_tasks.append(task)

            results: list[dict[str, Any]] = []
            for task in asyncio.as_completed(tasks):
                try:
                    image, scan_data = await task
                    if scan_data:
                        vulnerabilities = self.extract_vulnerabilities(scan_data)
                        results.append({"image": image, "vulnerabilities": vulnerabilities})
                except asyncio.CancelledError:  # noqa: PERF203
                    continue

        return results

    @staticmethod
    def extract_vulnerabilities(scan_data: dict[str, Any]) -> list[dict[str, Any]]:
        raise NotImplementedError

    async def shutdown(self) -> None:
        for task in self.active_tasks:
            task.cancel()
        await asyncio.gather(*self.active_tasks, return_exceptions=True)
