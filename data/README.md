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

For the first iteration of the model I labeled a small dataset myself. The first dataset I prepared consisted on 10 clips (10 seconds each).

Each video was labeled using **Computer Vision Annotation Tool** (CVAT). The procedure followed was to label the clips each 10 frames (and of course correct the step).
