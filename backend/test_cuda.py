"""
Simple script to test CUDA availability and configuration.
Run this to verify GPU support before starting the backend.
"""
import torch

print("=" * 60)
print("CUDA Configuration Test")
print("=" * 60)

# Check PyTorch version
print(f"\nPyTorch Version: {torch.__version__}")

# Check CUDA availability
cuda_available = torch.cuda.is_available()
print(f"CUDA Available: {cuda_available}")

if cuda_available:
    print(f"\n✓ GPU Support Enabled!")
    print(f"  - Device Name: {torch.cuda.get_device_name(0)}")
    print(f"  - CUDA Version: {torch.version.cuda}")
    print(f"  - Number of GPUs: {torch.cuda.device_count()}")
    print(f"  - Current Device: {torch.cuda.current_device()}")
    
    # Memory info
    if torch.cuda.device_count() > 0:
        total_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"  - Total GPU Memory: {total_memory:.2f} GB")
else:
    print(f"\n✗ GPU Support Not Available")
    print(f"  - The application will use CPU for processing")
    print(f"\nTo enable GPU support:")
    print(f"  1. Ensure you have an NVIDIA GPU with CUDA support")
    print(f"  2. Install CUDA Toolkit from https://developer.nvidia.com/cuda-downloads")
    print(f"  3. Install PyTorch with CUDA:")
    print(f"     pip install torch --index-url https://download.pytorch.org/whl/cu118")

print("\n" + "=" * 60)
