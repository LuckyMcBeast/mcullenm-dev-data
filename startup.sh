#!/usr/bin/env bash

echo "Initializing  database container..."
docker start mcullenm_dev_db
echo "Starting Python Virtual Enviroment..."
source venv/bin/activate
echo "Starting Uvicorn Server..."
uvicorn src.main:app --reload

