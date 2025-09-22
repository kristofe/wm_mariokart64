#!/usr/bin/env python3
"""
Test script to verify denoising trajectory logging to TensorBoard.
This script creates a simple test environment and logs denoising trajectories.
"""

import sys
import torch
from pathlib import Path
from datetime import datetime
from torch.utils.tensorboard import SummaryWriter

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agent import Agent
from envs import WorldModelEnv
from data import Dataset
from omegaconf import DictConfig, OmegaConf
from hydra.utils import instantiate

def test_denoising_logging():
    """Test denoising trajectory logging to TensorBoard."""
    
    print("🧪 Testing denoising trajectory logging...")
    
    # Create a simple config
    cfg = OmegaConf.create({
        'agent': {
            'denoiser': {
                'inner_model': {
                    'num_steps_conditioning': 4,
                    'num_steps_denoising': 10
                }
            }
        },
        'world_model_env': {
            'horizon': 100,
            'diffusion_sampler_next_obs': {
                'num_steps_denoising': 10,
                'sigma_min': 0.01,
                'sigma_max': 10.0,
                'rho': 7,
                'order': 2,
                's_churn': 0.0,
                's_tmin': 0.0,
                's_tmax': float('inf'),
                's_noise': 1.0,
                's_cond': 0.0
            }
        }
    })
    
    # Create TensorBoard writer
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = f"test_runs/denoising_test_{timestamp}"
    tb_writer = SummaryWriter(log_dir=log_dir)
    print(f"📊 TensorBoard logs will be saved to: {log_dir}")
    
    # Create a simple agent (mock)
    class MockAgent:
        def __init__(self):
            self.denoiser = None
            self.upsampler = None
            self.rew_end_model = None
    
    # Create mock denoiser that returns denoising trajectories
    class MockDenoiser:
        def __init__(self):
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.cfg = OmegaConf.create({'inner_model': {'num_steps_conditioning': 4}})
        
        def denoise(self, x, sigma, sigma_cond, prev_obs, prev_act):
            # Return a simple denoised version
            return x * 0.9
        
        def apply_noise(self, x, sigma, sigma_offset_noise=0):
            return x
    
    # Create mock diffusion sampler
    class MockDiffusionSampler:
        def __init__(self, denoiser, cfg):
            self.denoiser = denoiser
            self.cfg = cfg
            self.sigmas = torch.linspace(cfg.sigma_max, cfg.sigma_min, cfg.num_steps_denoising)
        
        def sample(self, prev_obs, prev_act):
            batch_size = prev_obs.shape[0]
            device = prev_obs.device
            
            # Create mock trajectory
            trajectory = []
            x = torch.randn(batch_size, 3, 64, 64, device=device)
            
            for i in range(self.cfg.num_steps_denoising):
                trajectory.append(x.clone())
                x = x * 0.9 + torch.randn_like(x) * 0.1
            
            return x, trajectory
    
    # Create mock world model env
    class MockWorldModelEnv:
        def __init__(self):
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.return_denoising_trajectory = True
            self.num_envs = 1
            
        def reset(self):
            return torch.randn(1, 3, 64, 64, device=self.device), {}
        
        def step(self, action):
            # Create mock denoising trajectory
            trajectory = []
            for i in range(10):  # 10 denoising steps
                step_img = torch.randn(1, 3, 64, 64, device=self.device)
                trajectory.append(step_img)
            
            trajectory_tensor = torch.stack(trajectory, dim=1)  # [batch, steps, channels, height, width]
            
            info = {}
            if self.return_denoising_trajectory:
                info["denoising_trajectory"] = trajectory_tensor
            
            return (torch.randn(1, 3, 64, 64, device=self.device), 
                    torch.tensor([1.0], device=self.device), 
                    torch.tensor([0], device=self.device), 
                    torch.tensor([0], device=self.device), 
                    info)
    
    # Test the logging
    print("🔄 Running test steps...")
    
    env = MockWorldModelEnv()
    obs, _ = env.reset()
    
    for step in range(5):
        action = torch.tensor([0], device=env.device)
        next_obs, rew, end, trunc, info = env.step(action)
        
        # Test TensorBoard logging
        if "denoising_trajectory" in info:
            trajectory = info["denoising_trajectory"]
            print(f"📸 Step {step}: Captured denoising trajectory with shape {trajectory.shape}")
            
            # Log to TensorBoard
            value_normalized = (trajectory + 1) / 2  # Convert [-1,1] to [0,1]
            num_steps_to_log = min(5, trajectory.shape[1])
            
            for i in range(num_steps_to_log):
                step_image = value_normalized[0, i]  # [channels, height, width]
                tb_writer.add_images(f"test_denoising_trajectory/step_{i}", step_image.unsqueeze(0), step)
            
            print(f"✅ Logged {num_steps_to_log} denoising images to TensorBoard")
        
        obs = next_obs
    
    tb_writer.close()
    print(f"🎉 Test completed! Check TensorBoard at: {log_dir}")
    print("Run: tensorboard --logdir test_runs/")

if __name__ == "__main__":
    test_denoising_logging()
