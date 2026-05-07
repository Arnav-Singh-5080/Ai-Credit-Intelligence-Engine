# ⚙️ Setup Guide

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

```bash
git clone https://github.com/Arnav-Singh-5080/Ai-Credit-Intelligence-Engine.git
cd Ai-Credit-Intelligence-Engine
pip install -r ai-credit-intelligence-engine/requirements.txt
streamlit run ai-credit-intelligence-engine/application.py
```

## Model Files

The `models/` directory should contain:
- `loan_model.pkl` — Trained loan prediction model
- `scaler.pkl` — Feature scaler for data preprocessing

If these files are missing, the application will display an error with instructions.
