from logging import FileHandler
import time
import os


class DailyFileHandler(FileHandler):
    DATE_FORMAT = '%Y-%m-%d'

    _origin_filename__name: str
    _origin_filename__ext: str

    def __init__(self, filename, *args, **kwargs):
        root, ext = os.path.splitext(os.path.abspath(os.fspath(filename)))
        self._origin_filename__name, self._origin_filename__ext = root, ext

        filename = self._inject_time()
        super().__init__(filename, *args, **kwargs)

    @property
    def _is_new_day(self):
        return time.strftime(self.DATE_FORMAT) not in self.baseFilename

    def _inject_time(self):
        return f'{self._origin_filename__name}_{time.strftime(self.DATE_FORMAT)}{self._origin_filename__ext}'

    def emit(self, record):
        if self._is_new_day:
            self.close()
            self.baseFilename = self._inject_time()
            self.stream = self._open()

        return super().emit(record)
