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
