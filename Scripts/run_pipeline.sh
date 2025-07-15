#!/bin/bash
# scripts/run_pipeline.sh

# Activate virtual environment
source venv/bin/activate

# Run the Python pipeline script
python src/main_pipeline.py

# Deactivate virtual environment (optional)
deactivate