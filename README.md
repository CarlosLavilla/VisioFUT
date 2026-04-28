# VisioFUT

## What is VisioFUT?

## Environment configuration

The project provides a `pyproject.toml` that has all the necessary dependencies for running the project. The only extra step that is needed is, once you have created a virtual environment and installed the dependencies is to run:

```cmd
REM This creates the virtual environment and installs the dependencies in pyproject
python -m venv .venv
pip install .

REM This installs extra dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Which installs **CUDA-enabled Pytorch**.

> [!NOTE]
> The CUDA-enabled Pytorch requires a NVIDIA GPU with the correspondent drivers to work.

## Developer tool

During the development of VisioFUT some necessities for the development were identified. Those necessities are covered under the  `src/dev` folder. This contains a simple tk application with some features that were useful for the development of the main app.

> [!WARNING]
> You must place your .pt model in the root directory, in a `models` folder for some features to work. It must be called `best.pt`.

### Key features

* **Video Annotation**: Automates video annotation. Takes a video and, using the model `models/best.pt`, generates the predictions and outputs a XML file in CVAT 1.1 format. Optionally, the user may select to obtain the video with the annotations overlaid on it.
