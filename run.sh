#!/bin/bash

port=5000

process_ids=$(lsof -t -i :$port)
if [ -n "$process_ids" ]; then
    echo "Port $port is already in use. Killing the process(es)..."
    kill $process_ids
    echo "Process(es) on port $port killed successfully."
else
    echo "No processes found on port $port."
fi

nohup python app.py > /dev/null 2>&1 & disown
