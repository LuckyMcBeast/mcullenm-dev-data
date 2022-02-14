#!/usr/bin/env bash
echo "Starting database container..."
docker start mcullenm_dev_db
echo "Starting Python Virtual Enviroment..."
source venv/bin/activate
echo "Starting Uvicorn Server..."
nohup uvicorn src.main:app --reload &
sleep 1
echo "Done."
