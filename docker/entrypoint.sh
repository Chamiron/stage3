#!/bin/bash
# Watch the shared volume for new code and execute it
while true; do
    if [ -f /shared-volume/main.py ]; then
        echo "New code detected. Executing..."
        python /shared-volume/main.py
    fi
    sleep 5
done