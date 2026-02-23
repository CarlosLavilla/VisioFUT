import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from pathlib import Path
from typing import Optional

from utils.service.VisioFUTService import VisioFUTService
from utils.service.VisioFUTWorker import VisioFUTWorker

ALLOWED_EXTENSIONS: set[str] = {".mp4"}


class VisioFUTUtilsApp:

    def __init__(self, root: tk.Tk) -> None:

        self._annotation_service = VisioFUTService(Path("models\\best.pt"))

        self._root: tk.Tk = root
        self._root.title("VisioFUT Utils App")
        self._root.geometry("500x150")
        self._root.resizable(False, False)

        self._video_path: tk.StringVar = tk.StringVar()

        self._initialize_ui()

    def _initialize_ui(self) -> None:
        main_frame: tk.Frame = tk.Frame(self._root, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        label: tk.Label = tk.Label(main_frame, text="Input video file:")
        label.pack(anchor="w")

        entry: tk.Entry = tk.Entry(
            main_frame,
            textvariable=self._video_path,
            width=60,
        )
        entry.pack(fill=tk.X, pady=(5, 10))

        button_frame: tk.Frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        browse_button: tk.Button = tk.Button(
            button_frame,
            text="Browse",
            command=self._browse_file,
            width=12,
        )
        browse_button.pack(side=tk.LEFT)

        submit_button: tk.Button = tk.Button(
            button_frame,
            text="Submit",
            command=self._submit,
            width=12,
        )
        submit_button.pack(side=tk.RIGHT)

        self._progress = ttk.Progressbar(
            main_frame,
            orient="horizontal",
            length=400,
            mode="determinate",
        )
        self._progress.pack(pady=10)

    def _browse_file(self) -> None:
        selected_file: str = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video Files", "*.mp4 *.mov *.avi *.mkv"),
                ("All Files", "*.*"),
            ],
        )

        if selected_file:
            self._video_path.set(selected_file)

    def _submit(self) -> None:
        path_str: str = self._video_path.get().strip()
        video_path: Optional[Path] = self._validate_path(path_str)

        if video_path is None:
            messagebox.showerror(
                "Invalid File",
                "Please select a valid video file.",
            )
            return

        # Launch process
        def on_progress(value: int) -> None:
            self._root.after(0, lambda: self._progress.configure(value=value))

        def on_done() -> None:
            self._root.after(
                0, lambda: messagebox.showinfo("Done", "Video processing complete!")
            )

        def on_exception(exc: Exception):
            self._root.after(0, lambda: messagebox.showerror("Error", str(exc)))

        worker = VisioFUTWorker(
            service=self._annotation_service,
            video_path=video_path,
            on_progress=on_progress,
            on_done=on_done,
            on_error=on_exception,
        )

        worker.start()

    def _validate_path(self, path_str: str) -> Optional[Path]:
        if not path_str:
            return None

        path: Path = Path(path_str)

        if not path.exists():
            return None

        if not path.is_file():
            return None

        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            return None

        return path


def main() -> None:
    root: tk.Tk = tk.Tk()
    _ = VisioFUTUtilsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
