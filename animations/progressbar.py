import sys
import time

def progress_bar(iterable, total=None, prefix='', size=40, file=None):
    if file is None:
        file = sys.stdout
    start = time.time()
    if total is None:
        try:
            total = len(iterable)
        except Exception:
            total = None

    def render(i):
        if total:
            frac = i / total
            filled = int(size * frac)
            bar = '█' * filled + '-' * (size - filled)
            elapsed = time.time() - start
            rate = i / elapsed if elapsed > 0 else 0
            eta = int((total - i) / rate) if rate > 0 else 0
            file.write(f'\r{prefix} |{bar}| {i}/{total} ETA {eta}s')
        else:
            filled = int(size * (i % (size + 1)) / max(1, size))
            bar = '█' * filled + '-' * (size - filled)
            file.write(f'\r{prefix} |{bar}| {i}')
        file.flush()

    i = 0
    for item in iterable:
        i += 1
        render(i)
        yield item

    if total:
        file.write(f'\r{prefix} |' + '█' * size + f'| {total}/{total} Done\n')
    else:
        file.write('\n')
    file.flush()


def render_progress(current, total, prefix='', size=40, file=None):
    if file is None:
        file = sys.stdout
    frac = current / total if total and total > 0 else 0
    filled = int(size * frac)
    bar = '█' * filled + '-' * (size - filled)
    file.write(f'\r{prefix} |{bar}| {current}/{total}')
    file.flush()


class Progress:
    def __init__(self, prefix='', size=40, file=None, min_interval=0.08):
        self.prefix = prefix
        self.size = size
        self.file = file or sys.stdout
        self.min_interval = min_interval
        self.start = None
        self.last = 0.0
        self.last_render = 0

    def __call__(self, current, total):
        now = time.time()
        if self.start is None:
            self.start = now
            self.last = now
        if total and total > 0:
            frac = current / total
        else:
            frac = 0
        if now - self.last < self.min_interval and current < total:
            return
        self.last = now

        filled = int(self.size * frac)
        bar = '█' * filled + '·' * (self.size - filled)
        elapsed = now - self.start
        rate = (current / elapsed) if elapsed > 0 else 0
        eta = int((total - current) / rate) if rate > 0 and total and total > 0 else 0
        pct = int(frac * 100) if total and total > 0 else 0
        self.file.write(f'\r{self.prefix:10s} |{bar}| {pct:3d}% {current}/{total} ETA {eta:3d}s')
        self.file.flush()
