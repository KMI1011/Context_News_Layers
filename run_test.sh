#!/bin/bash
# Helper script to run tests with correct Python path

cd "$(dirname "$0")"
source context_layer/venv/bin/activate
export PYTHONPATH="$(pwd):$PYTHONPATH"
python utils/test_context.py

