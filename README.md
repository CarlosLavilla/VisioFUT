# VisioFUT

## Environment configuration

The project provides a `pyproject.toml` that has all the necessary dependencies for running the project. The only extra step that is needed is, once you have created a virtual environment and installed the dependencies is to run:

```cmd
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Which installs **CUDA-enabled Pytorch**.
