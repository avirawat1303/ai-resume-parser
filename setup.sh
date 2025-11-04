#!/usr/bin/env bash
set -e

echo "Setting up AI Resume Parser..."


python -m venv .venv
source .venv/bin/activate || source .venv/Scripts/activate


echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt


if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

echo "Setup complete!"
echo ""
echo " Run the API with:"
echo "python -m uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000"
