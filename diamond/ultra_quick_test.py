#!/usr/bin/env python3
"""
Ultra quick test script for MarioKart64 training.
This script runs just 1 epoch to verify everything works.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_ultra_quick_test():
    """Run an ultra quick test of the training pipeline."""
    
    # Change to the diamond directory
    diamond_dir = Path(__file__).parent
    os.chdir(diamond_dir)
    
    print(f"🚀 Starting ultra quick test")
    print(f"📁 Working directory: {diamond_dir}")
    
    # Set environment variables to avoid interactive prompts
    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'
    
    # Prepare the command
    cmd = [
        sys.executable, "src/main.py",
        "--config-name=trainer_ultra_quick",
        "hydra.mode=RUN"
    ]
    
    print(f"🔧 Running command: {' '.join(cmd)}")
    print("=" * 60)
    
    try:
        # Run the training with pre-set parameters
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
        stdout, _ = process.communicate(timeout=60)  # 1 minute timeout
        
        print("📊 Training output:")
        print(stdout)
        
        if process.returncode == 0:
            print("✅ Ultra quick test completed successfully!")
            return True
        else:
            print(f"❌ Ultra quick test failed with return code: {process.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Ultra quick test timed out after 1 minute")
        process.kill()
        return False
    except Exception as e:
        print(f"💥 Error running ultra quick test: {e}")
        return False

if __name__ == "__main__":
    print("🎮 MarioKart64 Ultra Quick Test")
    print("=" * 40)
    
    success = run_ultra_quick_test()
    
    if success:
        print("\n🎉 SUCCESS! Training is working correctly!")
        print("💡 You can now run longer training sessions with confidence.")
    else:
        print("\n🔧 Training failed. Check the output above for errors.")
