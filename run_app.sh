#!/bin/bash
# Script to start the DeepFake Detector web app

cd "$(dirname "$0")"
source venv/bin/activate
streamlit run app.py
