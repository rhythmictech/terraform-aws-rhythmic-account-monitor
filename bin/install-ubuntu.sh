#!/bin/bash
# Installs pinned versions of the tools pre-commit needs. Used by CI.
# Terraform itself is installed separately (see .terraform-version).
set -euo pipefail

PRE_COMMIT_VERSION=4.7.0
TERRAFORM_DOCS_VERSION=0.24.0
TERRAFORM_DOCS_SHA256=9005daf969de0b50134493a2c00078b49f5f5b39d021cda7c89bf4d4f3d776d3
TFLINT_VERSION=0.66.0
TFLINT_SHA256=22be11cadc25cd02401e94c0ccc91aa63467debb8485c2a755d98f4c0a9d1e2e
TRIVY_VERSION=0.76.2
TRIVY_SHA256=bc0fc726e017b8927a62b2d3531d7a84ee01769daf5c99ed866dced54089fdbf

echo 'installing dependencies'
pip3 install "pre-commit==${PRE_COMMIT_VERSION}"

workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT
cd "$workdir"

fetch() { # url sha256 filename
  curl -fsSL -o "$3" "$1"
  echo "$2  $3" | sha256sum -c -
}

fetch "https://github.com/terraform-docs/terraform-docs/releases/download/v${TERRAFORM_DOCS_VERSION}/terraform-docs-v${TERRAFORM_DOCS_VERSION}-linux-amd64.tar.gz" "$TERRAFORM_DOCS_SHA256" terraform-docs.tar.gz
tar -xzf terraform-docs.tar.gz terraform-docs

fetch "https://github.com/terraform-linters/tflint/releases/download/v${TFLINT_VERSION}/tflint_linux_amd64.zip" "$TFLINT_SHA256" tflint.zip
unzip -q tflint.zip tflint

fetch "https://github.com/aquasecurity/trivy/releases/download/v${TRIVY_VERSION}/trivy_${TRIVY_VERSION}_Linux-64bit.tar.gz" "$TRIVY_SHA256" trivy.tar.gz
tar -xzf trivy.tar.gz trivy

sudo install -m 0755 terraform-docs tflint trivy /usr/local/bin/
