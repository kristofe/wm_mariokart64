#!/bin/bash

# Launch TensorBoard to view training logs
# This script finds the latest run and starts TensorBoard

echo "Starting TensorBoard..."
echo "Logs will be available at: http://localhost:6006"
echo ""

# Find the latest run directory
LATEST_RUN=""
if [ -d "outputs" ]; then
    # Find the most recent date directory
    LATEST_DATE=$(ls -1t outputs/ 2>/dev/null | head -1)
    if [ -n "$LATEST_DATE" ] && [ -d "outputs/$LATEST_DATE" ]; then
        # Find the most recent time directory within that date
        LATEST_TIME=$(ls -1t "outputs/$LATEST_DATE" 2>/dev/null | head -1)
        if [ -n "$LATEST_TIME" ] && [ -d "outputs/$LATEST_DATE/$LATEST_TIME" ]; then
            LATEST_RUN="outputs/$LATEST_DATE/$LATEST_TIME"
        fi
    fi
fi

if [ -n "$LATEST_RUN" ] && [ -d "$LATEST_RUN/runs" ]; then
    echo "Using latest run: $LATEST_RUN"
    echo "Available TensorBoard logs:"
    ls -la "$LATEST_RUN/runs/" 2>/dev/null | grep "^d" | awk '{print "  " $9}' | grep -v "^\.$\|^\.\.$"
    echo ""
    echo "Press Ctrl+C to stop TensorBoard"
    echo ""
    # Use the virtual environment if available
    if [ -f "../.venv/bin/tensorboard" ]; then
        echo "Starting TensorBoard on http://localhost:6006"
        ../.venv/bin/tensorboard --logdir="$LATEST_RUN/runs" --port=6006 --host=0.0.0.0
    elif [ -f ".venv/bin/tensorboard" ]; then
        echo "Starting TensorBoard on http://localhost:6006"
        .venv/bin/tensorboard --logdir="$LATEST_RUN/runs" --port=6006 --host=0.0.0.0
    else
        echo "Starting TensorBoard on http://localhost:6006"
        tensorboard --logdir="$LATEST_RUN/runs" --port=6006 --host=0.0.0.0
    fi
else
    echo "No training runs found with TensorBoard logs."
    echo "Available runs:"
    if [ -d "outputs" ]; then
        find outputs/ -name "runs" -type d 2>/dev/null | head -10
    else
        echo "  No outputs directory found. Start training to create logs."
    fi
    echo ""
    echo "You can also manually specify a run directory:"
    echo "  tensorboard --logdir=outputs/YYYY-MM-DD/HH-MM-SS/runs --port=6006"
fi
