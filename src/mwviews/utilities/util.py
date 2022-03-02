import heapq

from more_itertools import peekable


def collate(*iterables, key=lambda i: i):
    # Prepare the iterable queue
    nextq = []
    for i, iterable in enumerate(iterables):
        iterable = peekable(iterable)
        try:
            heapq.heappush(nextq, ((iterable.peek(), i), iterable))
        except StopIteration:
            # Na. We're cool
            pass

    while len(nextq) > 0:
        (_, i), iterable = heapq.heappop(nextq)

        yield next(iterable)

        try:
            heapq.heappush(nextq, ((iterable.peek(), i), iterable))
        except:
            # Again, we're cool.
            pass
