import asyncio
import signal

import click

from .service import ImageScanningService


@click.command()
@click.option("--namespace", required=True, help="Kubernetes namespace")
@click.option("--label-selector", required=True, help="Label selector for resources")
@click.option("--output-file", default="scan_results.json", help="Output file for scan results")
@click.option(
    "--scanner-type",
    required=True,
    type=click.Choice(["trivy", "grype"]),
    help="Type of scanner to use",
)
@click.option(
    "--max-concurrent-tasks",
    default=4,
    help="Maximum number of concurrent tasks",
    type=int,
)
def main(namespace, label_selector, output_file, scanner_type, max_concurrent_tasks):
    async def run():
        service = ImageScanningService(namespace, label_selector, output_file, scanner_type, max_concurrent_tasks)

        loop = asyncio.get_running_loop()
        shutdown_event = asyncio.Event()

        def stop_service() -> None:
            asyncio.create_task(service.shutdown())  # noqa: RUF006
            shutdown_event.set()

        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, stop_service)

        await service.run()
        await shutdown_event.wait()

    asyncio.run(run())


if __name__ == "__main__":
    main()
