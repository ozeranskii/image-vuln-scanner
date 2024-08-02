from __future__ import annotations

import asyncio
import json
from typing import Any


class KubernetesClientError(Exception):
    pass


class KubernetesClient:
    def __init__(self, namespace: str) -> None:
        self.namespace: str = namespace

    async def get_resources(self, label_selector: str) -> list[dict[str, Any]]:
        resources_cmd: str = f"kubectl get all -n {self.namespace} -l {label_selector} -o json"
        proc: asyncio.subprocess.Process = await asyncio.create_subprocess_shell(
            resources_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            error_message_full = f"Error getting resources: {stderr.decode()}"
            raise KubernetesClientError(error_message_full)
        resources_data: dict[str, Any] = json.loads(stdout.decode())
        return resources_data["items"]
