# Quick Test Guide for MarioKart64 Training

This guide helps you quickly test and optimize your MarioKart64 training setup.

## 🚀 Quick Start

### 1. Run the Quick Test
```bash
cd diamond
python quick_test.py
```

This will run both configurations and show you if everything is working.

### 2. Speed Test
```bash
./test_speed.sh
```

This runs a timed comparison between different configurations.

## 📁 Configuration Files

### `trainer_quick_test.yaml`
- **Purpose**: Minimal test to verify everything works
- **Epochs**: 5
- **Batch size**: 4
- **Steps per epoch**: 10
- **Time**: ~2-5 minutes

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

### Quick Test (5 minutes)
```bash
python src/main.py --config-name=trainer_quick_test
```

### Fast Training (2-4 hours)
```bash
python src/main.py --config-name=trainer_fast
```

### No Upsampling (1-2 hours)
```bash
python src/main.py --config-name=trainer_no_upsampling
```

### Original Full Training (10+ hours)
```bash
python src/main.py --config-name=trainer
```

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

Happy training! 🏎️
