#!/bin/bash

# List all available training runs with TensorBoard logs

echo "Available training runs with TensorBoard logs:"
echo "=============================================="

if [ -d "outputs" ]; then
    # Find all runs with TensorBoard logs
    find outputs/ -name "runs" -type d | while read run_dir; do
        # Extract the run path
        run_path=$(dirname "$run_dir")
        run_name=$(basename "$run_path")
        run_date=$(basename $(dirname "$run_path"))
        
        # Count TensorBoard log directories
        log_count=$(find "$run_dir" -maxdepth 1 -type d | grep -v "^$run_dir$" | wc -l)
        
        if [ $log_count -gt 0 ]; then
            echo "📊 $run_date/$run_name ($log_count log directories)"
            echo "   Path: $run_path"
            echo "   TensorBoard: tensorboard --logdir=\"$run_dir\" --port=6006"
            echo ""
        fi
    done
else
    echo "No outputs directory found. Start training to create logs."
fi

echo "To view the latest run:"
echo "  ./scripts/launch_tensorboard.sh"
echo ""
echo "To view a specific run:"
echo "  tensorboard --logdir=\"outputs/YYYY-MM-DD/HH-MM-SS/runs\" --port=6006"
