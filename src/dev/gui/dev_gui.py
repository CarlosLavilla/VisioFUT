import tkinter as tk
from tkinter import ttk

from pathlib import Path

from ..tracker.annotation_service import VisioFUTAnnotationService
from ..tracker.annotation_ui import VisioFUTAnnotationUI


class VisioFUTDevApp:

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._root.title("VisioFUT Developer App")
        self._root.geometry("600x300")
        self._root.resizable(False, False)

        # Shared Services
        self._tracker_service = VisioFUTAnnotationService(Path("models/best.pt"))

        # Setup Tabs
        self._notebook = ttk.Notebook(self._root)
        self._notebook.pack(fill=tk.BOTH, expand=True)

        self._setup_tabs()

    def _setup_tabs(self) -> None:
        # Feature 1: CVAT Generator
        self.cvat_tab = VisioFUTAnnotationUI(self._notebook, self._tracker_service)
        self._notebook.add(self.cvat_tab, text="Video Annotation")
