# Dataset preparation

## Video Extraction

> [!NOTE]
> The videos are not included in the repository.

To extract the videos I used ffmpeg. I selected meaningful clips of around **10 seconds**. The command I used for this was:

```cmd
ffmpeg -i input.mp4 -ss mm:ss -to mm:ss clips/output.mp4   
```

I used the `data\raw` folder as the root to execute this command (as well as the folder to store the full matches).

## Video annotation

Each video was labeled using **Computer Vision Annotation Tool** (CVAT). The procedure followed was to label the clips each 10 frames. Then I exported the datasets obtained from them using the **Ultralytics YOLO Detection 1.0** export format and saving the images.

Initially one 10 seconds clip was manually annotated. Then, the successive models obtained from training were used as the base annotation source, correcting the annotations each 10 frames. The command used for using the model for annotation is:

```cmd
yolo detect predict model=runs/detect/train<x>/weights/best.pt source=<path_to_video> save_txt=True save_conf=True project=predictions name=video_prediction
```

## Naming convention for datasets

Datasets will be placed in subfolders of `data`. The naming is to be `football_detection_cvat_v<n>`.

Before a training iteration, inside the folder the following contents must be present:

```txt
football_detection_cvat_v<n>/
├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/
├── data.yaml
```

## Training

The model to use at the early stages of the project is `yolov8n.pt`. This will help fast iteration and will be enough for the small set of data available at the beginning of the project.

The training command to be used is:

```cmd
yolo detect train model=yolov8n.pt data=data/football_detection_cvat_v<n>/data.yaml imgsz=1280 epochs=50 batch=8 device=0
```

However, the model will be upscaled when the data available is big enough and the nano model is fairly accurate.

The initial idea is to upscale to the **small** version and then to the **medium**. But this will be decided on the go. What is not to be decided is whether there will be an upscaling, because the nano model will start to be not enough when the dataset grows.

### Iterations

For each iteration the previous model is used for pre-annotation. This way I only need to correct what the model predicts and the workload decreases drastically. For detection the following command can be used (once a first model is present):

```cmd
yolo track model=runs/detect/train<x>/weights/best.pt source=path_to_clip.mp4 save_txt=True save_conf=True project=predictions name=destination_folder_name
```
