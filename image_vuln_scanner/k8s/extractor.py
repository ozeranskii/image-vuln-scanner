from __future__ import annotations

from typing import Any


class ResourceImageExtractor:
    def get_images(self, resources: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
        images: dict[str, dict[str, str]] = {}

        for resource in resources:
            kind: str = resource["kind"]
            name: str = resource["metadata"]["name"]
            containers: list[dict[str, str]] = self._get_containers(resource)

            for container in containers:
                image: str = container["image"]
                if image not in images:
                    images[image] = {"resource_kind": kind, "resource_name": name}

        return images

    @staticmethod
    def _get_containers(resource: dict[str, Any]) -> list[dict[str, str]]:
        if "template" in resource["spec"]:
            return resource["spec"]["template"]["spec"]["containers"]
        if "containers" in resource["spec"]:
            return resource["spec"]["containers"]
        return []
