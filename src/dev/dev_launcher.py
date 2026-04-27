import tkinter as tk
import torch

from .gui.dev_gui import VisioFUTDevApp


def main() -> None:
    print("Torch:", torch.__version__)
    print("CUDA available:", torch.cuda.is_available())
    print("GPU:", torch.cuda.get_device_name(0))

    root: tk.Tk = tk.Tk()
    _ = VisioFUTDevApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
