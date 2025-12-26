# Video Extraction

> [!NOTE]
> The videos are not included in the repository.

To extract the videos I used ffmpeg. I selected meaningful clips of around **10 seconds**. The command I used for this was:

```cmd
ffmpeg -i input.mp4 -ss mm:ss -to mm:ss clips/output.mp4   
```

I used the `data\raw` folder as the root to execute this command (as well as the folder to store the full matches).
