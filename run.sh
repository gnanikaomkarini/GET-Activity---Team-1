#!/bin/bash
cd /home/gnanika/Downloads/GET-Activity---Team-1
export PYTHONPATH="${PYTHONPATH}:."
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
