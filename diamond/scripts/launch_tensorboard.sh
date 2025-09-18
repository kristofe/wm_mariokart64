#!/bin/bash

# Launch TensorBoard to view training logs
# This script starts TensorBoard and points it to the runs directory

echo "Starting TensorBoard..."
echo "Logs will be available at: http://localhost:6006"
echo ""
echo "Available training runs:"
if [ -d "runs" ]; then
    ls -la runs/ 2>/dev/null | grep "^d" | awk '{print "  " $9}' | grep -v "^\.$\|^\.\.$"
else
    echo "  No runs directory found. Start training to create logs."
fi
echo ""
echo "Press Ctrl+C to stop TensorBoard"

tensorboard --logdir=runs --port=6006
