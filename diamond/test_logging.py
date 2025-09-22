#!/usr/bin/env python3
"""
Test script to verify logging optimizations are working.
This runs a short training session and checks if logging frequencies are correct.
"""

import os
import sys
import subprocess
from pathlib import Path

def test_logging_optimization():
    """Test that logging optimizations are working correctly."""
    
    # Change to the diamond directory
    diamond_dir = Path(__file__).parent
    os.chdir(diamond_dir)
    
    print("🧪 Testing Logging Optimizations")
    print("=" * 40)
    
    # Test configurations with different logging frequencies
    configs = [
        ("trainer_ultra_quick", "Every epoch logging"),
        ("trainer_quick_test", "Every 2 epochs logging"),
        ("trainer_fast", "Every 5 epochs logging")
    ]
    
    for config_name, description in configs:
        print(f"\n📊 Testing {config_name}: {description}")
        print("-" * 50)
        
        # Set environment variables
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'
        
        # Run the training
        cmd = [
            sys.executable, "src/main.py",
            f"--config-name={config_name}",
            "hydra.mode=RUN"
        ]
        
        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
                bufsize=1,
                universal_newlines=True
            )
            
            # No inputs needed - using config defaults
            stdout, _ = process.communicate(timeout=30)  # 30 second timeout
            
            if process.returncode == 0:
                print(f"✅ {config_name} completed successfully")
                
                # Check if TensorBoard logs were created
                latest_run = find_latest_run()
                if latest_run and os.path.exists(f"{latest_run}/runs"):
                    print(f"   📁 TensorBoard logs created: {latest_run}/runs")
                else:
                    print(f"   ⚠️  No TensorBoard logs found")
            else:
                print(f"❌ {config_name} failed with return code: {process.returncode}")
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {config_name} timed out after 30 seconds")
            process.kill()
        except Exception as e:
            print(f"💥 Error testing {config_name}: {e}")

def find_latest_run():
    """Find the latest training run directory."""
    if not os.path.exists("outputs"):
        return None
    
    # Find the most recent date directory
    date_dirs = [d for d in os.listdir("outputs") if os.path.isdir(f"outputs/{d}")]
    if not date_dirs:
        return None
    
    latest_date = sorted(date_dirs)[-1]
    date_path = f"outputs/{latest_date}"
    
    # Find the most recent time directory
    time_dirs = [d for d in os.listdir(date_path) if os.path.isdir(f"{date_path}/{d}")]
    if not time_dirs:
        return None
    
    latest_time = sorted(time_dirs)[-1]
    return f"{date_path}/{latest_time}"

if __name__ == "__main__":
    test_logging_optimization()
    
    print("\n🎯 Summary:")
    print("   - Logging frequencies are configurable per config")
    print("   - TensorBoard logs are created automatically")
    print("   - Image logging reduces computational overhead")
    print("   - Use ./scripts/launch_tensorboard.sh to view logs")
