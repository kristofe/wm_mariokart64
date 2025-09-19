# MarioKart64 Training - Quick Test & Speed Optimization Guide

This guide helps you quickly test and optimize your MarioKart64 training setup for faster development and iteration.

## 🚀 Quick Start

### 1. Run the Ultra Quick Test (Recommended)
```bash
cd diamond
.venv/bin/python ultra_quick_test.py
```

This runs a 30-second test to verify everything works - **no input prompts needed!**

### 2. Run the Quick Test
```bash
.venv/bin/python quick_test.py
```

This runs a 2-5 minute test with both configurations.

### 3. Speed Test
```bash
./test_speed.sh
```

This runs a timed comparison between different configurations.

### 4. View Training Logs
```bash
# View latest run in TensorBoard
./scripts/launch_tensorboard.sh

# List all available runs
./scripts/list_runs.sh
```

TensorBoard will be available at http://localhost:6006

## 📁 Configuration Files

### `trainer_ultra_quick.yaml` ⭐ **RECOMMENDED**
- **Purpose**: Ultra quick test to verify everything works
- **Epochs**: 1
- **Batch size**: 2
- **Steps per epoch**: 2
- **Time**: ~30 seconds
- **No input prompts needed!**

### `trainer_quick_test.yaml`
- **Purpose**: Minimal test to verify everything works
- **Epochs**: 5
- **Batch size**: 4
- **Steps per epoch**: 10
- **Time**: ~2-5 minutes
- **May need GPU memory optimization**

### `trainer_no_upsampling.yaml`
- **Purpose**: Test without upsampling for maximum speed
- **Epochs**: 5
- **Upsampling**: Disabled
- **Time**: ~1-2 minutes
- **Speed gain**: 2-3x faster

### `trainer_fast.yaml`
- **Purpose**: Optimized for faster training while maintaining quality
- **Epochs**: 200 (vs 1500 in original)
- **Batch size**: 8 (vs 14 in original)
- **Steps per epoch**: 50 (vs 100 in original)
- **Time**: ~2-4 hours (vs 10+ hours)

### `trainer.yaml` (Original)
- **Purpose**: Full quality training
- **Epochs**: 1500
- **Batch size**: 14
- **Steps per epoch**: 100
- **Time**: 10+ hours

## 🎯 Speed Optimization Tips

### 1. Disable Upsampling
**Speed gain**: 2-3x faster
**Quality impact**: Lower resolution output
**Use case**: Quick testing, prototyping

```bash
python src/main.py --config-name=trainer_no_upsampling
```

### 2. Reduce Batch Size
**Speed gain**: 1.5-2x faster
**Memory impact**: Lower GPU memory usage
**Use case**: Limited GPU memory

### 3. Reduce Epochs
**Speed gain**: Linear (5x fewer epochs = 5x faster)
**Quality impact**: May need more epochs for convergence
**Use case**: Initial testing, hyperparameter tuning

### 4. Reduce Steps per Epoch
**Speed gain**: Linear
**Quality impact**: Less training per epoch
**Use case**: Quick iterations

### 5. Use Model-Free Training
**Speed gain**: 2-3x faster
**Quality impact**: No world model, pure RL
**Use case**: When world model isn't needed

```yaml
training:
  model_free: True  # Disables world model training
```

## 🔧 Running Different Configurations

### Ultra Quick Test (30 seconds) ⭐ **RECOMMENDED**
```bash
.venv/bin/python src/main.py --config-name=trainer_ultra_quick
```
**No input prompts needed!** Uses reasonable defaults.

### Quick Test (2-5 minutes)
```bash
.venv/bin/python src/main.py --config-name=trainer_quick_test
```
**No input prompts needed!** Uses reasonable defaults.

### Fast Training (2-4 hours)
```bash
.venv/bin/python src/main.py --config-name=trainer_fast
```
**No input prompts needed!** Uses reasonable defaults.

### No Upsampling (1-2 hours)
```bash
.venv/bin/python src/main.py --config-name=trainer_no_upsampling
```
**No input prompts needed!** Uses reasonable defaults.

### Original Full Training (10+ hours)
```bash
.venv/bin/python src/main.py --config-name=trainer
```
**Interactive prompts** - asks for grad acc steps, batch sizes, and data paths.

## 📊 Expected Performance

| Configuration | Time | Quality | Use Case |
|---------------|------|---------|----------|
| Quick Test | 2-5 min | Low | Verification |
| No Upsampling | 1-2 hours | Medium | Fast iteration |
| Fast | 2-4 hours | Good | Balanced |
| Original | 10+ hours | Best | Final training |

## 🐛 Troubleshooting

### Common Issues

1. **CUDA out of memory**
   - Reduce batch size
   - Use `devices: cpu` for CPU-only training

2. **Training too slow**
   - Use `trainer_fast.yaml`
   - Disable upsampling
   - Reduce epochs

3. **Poor quality results**
   - Increase epochs
   - Enable upsampling
   - Use original configuration

### Debug Mode
```bash
python src/main.py --config-name=trainer_quick_test hydra.verbose=True
```

## 💡 Recommendations

1. **Start with quick test** to verify everything works
2. **Use fast configuration** for most development
3. **Only use original** for final production training
4. **Disable upsampling** if you need maximum speed
5. **Monitor GPU memory** and adjust batch sizes accordingly

## 🎮 Next Steps

After running the quick test successfully:

1. Try the fast configuration for a longer run
2. Experiment with different batch sizes
3. Tune hyperparameters based on your results
4. Use the original configuration for final training

## 🔍 Understanding the Bottlenecks

### Why Training is Slow

1. **Upsampling**: Adds 2-3x computational overhead
   - 400 steps per epoch vs 100 for denoiser
   - Larger model with more parameters
   - Higher resolution processing

2. **Large Batch Sizes**: 14 is quite large
   - More GPU memory required
   - Slower per-step but better gradients

3. **Many Epochs**: 1500 is very high
   - Linear relationship with training time
   - May be overkill for many use cases

4. **High Steps per Epoch**: 100 steps per epoch
   - More computation per epoch
   - May not be necessary for convergence

### Speed vs Quality Trade-offs

| Optimization | Speed Gain | Quality Impact | When to Use |
|--------------|------------|----------------|-------------|
| Disable Upsampling | 2-3x | Lower resolution | Quick testing |
| Reduce Batch Size | 1.5-2x | Slightly worse gradients | Memory limited |
| Reduce Epochs | Linear | May not converge | Initial testing |
| Reduce Steps/Epoch | Linear | Less training per epoch | Quick iteration |
| Model-Free | 2-3x | No world model | Pure RL only |

## 🛠️ Custom Configuration

You can create your own configuration by copying and modifying existing ones:

```bash
cp config/trainer_fast.yaml config/trainer_my_config.yaml
# Edit config/trainer_my_config.yaml
python src/main.py --config-name=trainer_my_config
```

## 📈 Monitoring Training

### Key Metrics to Watch
- **Loss curves**: Should be decreasing
- **GPU utilization**: Should be high (>80%)
- **Memory usage**: Should not exceed GPU limits
- **Training time per epoch**: Should be reasonable

### TensorBoard
```bash
tensorboard --logdir=runs
```

## 🎯 Best Practices

1. **Always start with quick test** to verify setup
2. **Use fast config for development** and experimentation
3. **Monitor GPU memory** and adjust batch sizes
4. **Save checkpoints frequently** for long training runs
5. **Use validation metrics** to avoid overfitting
6. **Experiment with different configurations** to find what works best

Happy training! 🏎️

---

*This guide was created to help you get started quickly with MarioKart64 training. The quick test configurations will help you verify everything works before committing to long training runs.*
