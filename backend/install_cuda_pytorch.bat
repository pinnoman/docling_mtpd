@echo off
echo ========================================
echo Installing PyTorch with CUDA Support
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate

echo Current PyTorch version:
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}')"
echo.

echo Uninstalling CPU-only PyTorch...
pip uninstall -y torch torchvision torchaudio
echo.

echo Installing PyTorch with CUDA 11.8 support...
echo This may take a few minutes...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
echo.

echo ========================================
echo Installation complete!
echo ========================================
echo.

echo New PyTorch version:
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'CUDA Built: {torch.version.cuda}')"
echo.

echo If CUDA is still not available, you may need to:
echo 1. Install NVIDIA CUDA Toolkit 11.8 from https://developer.nvidia.com/cuda-downloads
echo 2. Ensure you have an NVIDIA GPU with CUDA support
echo 3. Update your NVIDIA drivers
echo.

pause
