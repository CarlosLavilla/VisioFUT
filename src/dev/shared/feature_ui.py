import tkinter as tk


class BaseFeatureUI(tk.Frame):
    """Base class for GUI of the dev app features.

    Args:
        tk (tk.Frame): frame where the components of the feature will be placed.
    """

    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        self._initialize_ui()

    def _initialize_ui(self) -> None:
        raise NotImplementedError("Subclasses must implement _initialize_ui")
