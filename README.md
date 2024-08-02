# Image Scanner

A CLI tool for scanning Docker images for vulnerabilities using Trivy and Grype.

## Installation

### Prerequisites

Before you begin, ensure you have the following dependencies installed:

1. **Python 3.8+**: You can download Python from the [official website](https://www.python.org/downloads/).
2. **Poetry**: Poetry is a tool for dependency management and packaging in Python. You can install it by following the instructions [here](https://python-poetry.org/docs/#installation).
3. **kubectl**: `kubectl` is a command-line tool for interacting with Kubernetes clusters. You can install it by following the instructions below.
4. **Trivy or Grype**: These are vulnerability scanners. Installation instructions for each are provided below.

### Install the project dependencies

Use Poetry to install the dependencies and the package:

```shell
poetry install
```
This will install all required dependencies listed in pyproject.toml and create a virtual environment for the project.

#### Install kubectl

To use this tool, you need to have `kubectl` installed and configured to access your Kubernetes cluster. To install kubectl, follow the instructions [here](https://kubernetes.io/docs/tasks/tools/).

Example installation on macOS using Homebrew:

```shell
brew install kubectl
```

### Install Trivy and Grype

Ensure you have Trivy and Grype installed on your system:

#### Trivy

Trivy is a comprehensive and easy-to-use vulnerability scanner for containers. To install Trivy, follow the instructions [here](https://github.com/aquasecurity/trivy#installation).

Example installation on macOS using Homebrew:

```shell
brew install aquasecurity/trivy/trivy
```

#### Grype

Grype is a vulnerability scanner for container images and filesystems. To install Grype, follow the instructions [here](https://github.com/anchore/grype#installation).

Example installation on macOS using Homebrew:

```shell
brew tap anchore/grype
brew install grype
```

## Usage

To use the CLI tool, you need to specify the Kubernetes namespace, label selector, output file, and the scanner type (either `trivy` or `grype`).

Example command:

```shell
poetry run image-vuln-scanner --namespace production --label-selector stack=python --output-file scan_results.json --scanner-type grype
```

## CLI Arguments

- `--namespace` (required): The Kubernetes namespace to scan.
- `--label-selector` (required): The label selector to filter the resources.
- `--output-file` (optional): The output file to save the scan results.
- `--scanner-type` (required): The vulnerability scanner to use (`trivy` or `grype`).
- `--max-concurrent-tasks` (optional): The maximum number of concurrent tasks (default is 4).
