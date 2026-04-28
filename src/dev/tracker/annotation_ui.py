import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from pathlib import Path
from typing import Optional

from ..shared.feature_ui import BaseFeatureUI
from .annotation_service import VisioFUTAnnotationService
from .annotation_worker import VisioFUTAnnotationWorker


ALLOWED_EXTENSIONS: set[str] = {".mp4"}


class VisioFUTAnnotationUI(BaseFeatureUI):

    def __init__(self, parent, annotation_service: VisioFUTAnnotationService) -> None:
        self._service = annotation_service
        self._video_path = tk.StringVar()
        super().__init__(parent)

    def _initialize_ui(self) -> None:

        label: tk.Label = tk.Label(self.container, text="Input video file:")
        label.pack(anchor="w")

        entry: tk.Entry = tk.Entry(
            self.container,
            textvariable=self._video_path,
            width=60,
        )
        entry.pack(fill=tk.X, pady=(5, 10))

        self._save_video_var = tk.BooleanVar(value=False)
        save_check = tk.Checkbutton(
            self.container,
            text="Save annotated video clip",
            variable=self._save_video_var,
        )
        save_check.pack(anchor="w", pady=(0, 10))

        button_frame: tk.Frame = tk.Frame(self.container)
        button_frame.pack(fill=tk.X)

        browse_button: tk.Button = tk.Button(
            button_frame,
            text="Browse",
            command=self._browse_file,
            width=12,
        )
        browse_button.pack(side=tk.LEFT)

        self._submit_button: tk.Button = tk.Button(
            button_frame,
            text="Submit",
            command=self._submit,
            width=12,
        )
        self._submit_button.pack(side=tk.RIGHT)

        self._progress = ttk.Progressbar(
            self.container,
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
        self._submit_button.config(state=tk.DISABLED)
        path_str: str = self._video_path.get().strip()
        video_path: Optional[Path] = self._validate_path(path_str)
        save_video: bool = self._save_video_var.get()

        if video_path is None:
            messagebox.showerror(
                "Invalid File",
                "Please select a valid video file.",
            )
            self._submit_button.config(state=tk.NORMAL)
            return

        # Launch process
        def on_progress(value: int) -> None:
            self.after(0, lambda: self._progress.configure(value=value))

        def on_done() -> None:
            self.after(
                0, lambda: messagebox.showinfo("Done", "Video processing complete!")
            )
            self.after(500, lambda: self._progress.configure(value=0))
            self.after(500, lambda: self._submit_button.config(state=tk.NORMAL))

        def on_exception(exc: Exception):
            self.after(0, lambda: messagebox.showerror("Error", str(exc)))
            self.after(500, lambda: self._progress.configure(value=0))
            self.after(500, lambda: self._submit_button.config(state=tk.NORMAL))

        worker = VisioFUTAnnotationWorker(
            service=self._service,
            video_path=video_path,
            save_video=save_video,
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
