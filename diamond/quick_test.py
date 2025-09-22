#!/usr/bin/env python3
"""
Quick test script for MarioKart64 training.
This script runs a minimal training session to verify everything works.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_quick_test(config_name="trainer_quick_test", disable_upsampling=False):
    """
    Run a quick test of the training pipeline.
    
    Args:
        config_name: Name of the config file to use
        disable_upsampling: If True, use the no-upsampling config
    """
    
    # Change to the diamond directory
    diamond_dir = Path(__file__).parent
    os.chdir(diamond_dir)
    
    # Set the config name
    if disable_upsampling:
        config_name = "trainer_no_upsampling"
    
    print(f"🚀 Starting quick test with config: {config_name}")
    print(f"📁 Working directory: {diamond_dir}")
    
    # Set environment variables to avoid interactive prompts
    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'
    
    # Prepare the command
    cmd = [
        sys.executable, "src/main.py",
        f"--config-name={config_name}",
        "hydra.mode=RUN"
    ]
    
    print(f"🔧 Running command: {' '.join(cmd)}")
    print("=" * 60)
    
    try:
        # Run the training with pre-set parameters
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            text=True,
            env=env,
            bufsize=1,
            universal_newlines=True
        )
        
        # No inputs needed - using config defaults
        stdout, _ = process.communicate(timeout=300)  # 5 minute timeout
        
        print("📊 Training output:")
        print(stdout)
        
        if process.returncode == 0:
            print("✅ Quick test completed successfully!")
            return True
        else:
            print(f"❌ Quick test failed with return code: {process.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Quick test timed out after 5 minutes")
        process.kill()
        return False
    except Exception as e:
        print(f"💥 Error running quick test: {e}")
        return False

def main():
    """Main function to run different test configurations."""
    
    print("🎮 MarioKart64 Training Quick Test")
    print("=" * 40)
    
    # Test 1: Quick test with upsampling
    print("\n🧪 Test 1: Quick test with upsampling enabled")
    print("-" * 50)
    success1 = run_quick_test("trainer_quick_test", disable_upsampling=False)
    
    if success1:
        print("\n✅ Test 1 passed! Basic training works.")
    else:
        print("\n❌ Test 1 failed! Check the output above for errors.")
        return
    
    # Test 2: Quick test without upsampling
    print("\n🧪 Test 2: Quick test with upsampling disabled")
    print("-" * 50)
    success2 = run_quick_test("trainer_no_upsampling", disable_upsampling=True)
    
    if success2:
        print("\n✅ Test 2 passed! Training without upsampling works.")
        print("\n📈 Speed comparison:")
        print("   - With upsampling: Slower but higher quality")
        print("   - Without upsampling: Faster but lower resolution")
    else:
        print("\n❌ Test 2 failed! Check the output above for errors.")
    
    print("\n🎯 Summary:")
    print(f"   - Basic training: {'✅ Working' if success1 else '❌ Failed'}")
    print(f"   - No upsampling: {'✅ Working' if success2 else '❌ Failed'}")
    
    if success1 and success2:
        print("\n🚀 Both tests passed! Your training setup is working correctly.")
        print("💡 You can now run full training with either configuration.")
    else:
        print("\n🔧 Some tests failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
