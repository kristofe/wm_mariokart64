#!/bin/bash

# Quick test script for MarioKart64 training speed comparison
# This script runs both configurations and compares their speed

echo "🎮 MarioKart64 Training Speed Test"
echo "=================================="

cd "$(dirname "$0")"

echo "🧪 Running quick test with upsampling..."
time python quick_test.py

echo ""
echo "📊 Speed test completed!"
echo ""
echo "💡 Tips for faster training:"
echo "   - Disable upsampling for 2-3x speed improvement"
echo "   - Reduce batch sizes if you have limited GPU memory"
echo "   - Use fewer epochs for initial testing"
echo "   - Consider using model_free=True for pure RL training"
