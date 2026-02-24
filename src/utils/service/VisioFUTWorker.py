import threading

from pathlib import Path
from typing import Callable

from ..service.VisioFUTService import VisioFUTService


class VisioFUTWorker:

    def __init__(
        self,
        service: VisioFUTService,
        video_path: Path,
        on_progress: Callable[[int], None],
        on_done: Callable[[], None],
        on_error: Callable[[Exception], None],
    ) -> None:
        self._service = service
        self._video_path = video_path
        self._on_progress = on_progress
        self._on_done = on_done
        self._on_error = on_error

    def start(self) -> None:
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self) -> None:
        try:
            for progress in self._service.track_video(self._video_path):
                self._on_progress(progress)

            self._on_done()
        except Exception as exc:
            self._on_error(exc)
