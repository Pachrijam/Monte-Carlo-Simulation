import sys
import threading
import time

class ColonBlinker:
    def __init__(self, prompt, delay=0.5):
        self.prompt = prompt
        self.delay = delay
        self._running = False
        self._thread = None
        self._visible = False

    def _update_colon(self, char):
        sys.stdout.write('\x1b[s')
        sys.stdout.write(f'\x1b[{len(self.prompt) + 1}G')
        sys.stdout.write(char + ' ')
        sys.stdout.write('\x1b[u')
        sys.stdout.flush()

    def _run(self):
        while self._running:
            self._visible = not self._visible
            self._update_colon(':' if self._visible else ' ')
            time.sleep(self.delay)
        self._update_colon(':')

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
        self._update_colon(':')
        self._thread.join()
        self._thread = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()


def blinking_input(prompt: str) -> str:
    stripped_prompt = prompt.rstrip()
    if not stripped_prompt.endswith(':'):
        return input(prompt)
    base = stripped_prompt[:-1]
    sys.stdout.write(base + ': ')
    sys.stdout.flush()
    with ColonBlinker(base):
        return input('')
