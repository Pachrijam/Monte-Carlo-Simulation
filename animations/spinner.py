from itertools import cycle
import sys
import threading
import time

class Spinner:
    def __init__(self, message='', delay=0.1):
        self.message = message
        self.delay = delay
        self._running = False
        self._thread = None
        self._spinner = cycle('⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏')

    def _run(self):
        while self._running:
            ch = next(self._spinner)
            sys.stderr.write('\x1b[s')
            sys.stderr.write('\x1b[1G')
            sys.stderr.write(f'{self.message} {ch}')
            sys.stderr.write('\x1b[u')
            sys.stderr.flush()
            time.sleep(self.delay)
        sys.stderr.write('\x1b[s')
        sys.stderr.write('\x1b[1G')
        sys.stderr.write(' ' * (len(self.message) + 2))
        sys.stderr.write('\x1b[u')
        sys.stderr.flush()

    def start(self):
        if self._running:
            return self
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        return self

    def stop(self):
        if not self._running:
            return
        self._running = False
        self._thread.join()
        self._thread = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()
