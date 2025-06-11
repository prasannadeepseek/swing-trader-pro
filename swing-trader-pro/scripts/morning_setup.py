#!/bin/bash
# scripts/morning_setup.py
import os
from core.data_pipeline import DataPipeline

if __name__ == "__main__":
    print("Running morning setup...")
    DataPipeline().prefetch_universe()
    print("Setup complete!")
