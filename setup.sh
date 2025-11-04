#!/usr/bin/env bash
set -e

echo "Setting up AI Resume Parser (Docker Version)..."

echo "Stopping running containers (if any)..."
docker compose down || true


echo "Building Docker images (no cache)..."
docker compose build --no-cache


echo "Starting containers..."
docker compose up -d


echo "Waiting for PostgreSQL to start..."
sleep 10

docker compose ps

echo ""
echo "Setup complete!"
echo "Visit the API docs at: http://localhost:8000/docs"
echo "Health check:         http://localhost:8000/health"
echo ""
echo "To view logs:         docker compose logs -f"
echo "To run tests:         docker compose exec api pytest -v"
echo ""
echo "To stop everything:   docker compose down"
