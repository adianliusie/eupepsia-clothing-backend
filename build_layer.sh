#!/bin/bash
# Builds the python dependency layer for x86_64 Lambda using the SAM build image.
set -euo pipefail
OUT_DIR="services_modules/python"
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"
docker run --platform linux/amd64 --rm -v "$(pwd)":/app -w /app \
  public.ecr.aws/sam/build-python3.12:latest \
  pip install -r services/src/requirements.txt --target "$OUT_DIR"
