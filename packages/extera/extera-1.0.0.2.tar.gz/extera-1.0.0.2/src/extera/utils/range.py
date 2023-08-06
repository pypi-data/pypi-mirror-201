def frange(start, stop, step, n=None):
    """return a WYSIWYG series of float values that mimic range behavior
    by excluding the end point and not printing extraneous digits beyond
    the precision of the input numbers (controlled by n and automatically
    detected based on the string representation of the numbers passed).

    CREDITS
    =======

    Function offered by https://stackoverflow.com/users/1089161/smichr at
    https://stackoverflow.com/questions/7267226/range-for-floats/67053708#67053708

    EXAMPLES
    ========

    non-WYSIWYS simple list-comprehension

    >>> [.11 + i*.1 for i in range(3)]
    [0.11, 0.21000000000000002, 0.31]

    WYSIWYG result for increasing sequence

    >>> list(frange(0.11, .33, .1))
    [0.11, 0.21, 0.31]

    and decreasing sequences

    >>> list(frange(.345, .1, -.1))
    [0.345, 0.245, 0.145]

    To hit the end point for a sequence that is divisibe by
    the step size, make the end point a little bigger by
    adding half the step size:

    >>> dx = .2
    >>> list(frange(0, 1 + dx/2, dx))
    [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

    """
    if step == 0:
        raise ValueError('step must not be 0')
    # how many decimal places are showing?
    if n is None:
        n = max([0 if '.' not in str(i) else len(str(i).split('.')[1])
                for i in (start, stop, step)])
    if step*(stop - start) > 0:  # a non-null incr/decr range
        if step < 0:
            for i in frange(-start, -stop, -step, n):
                yield -i
        else:
            steps = round((stop - start)/step)
            while round(step*steps + start, n) < stop:
                steps += 1
            for i in range(steps):
                yield round(start + i*step, n)

class FRange:
    min: float
    max: float
    step: float

    def __init__(self, min: float, max: float, step: float = 1):
        self.min = min
        self.max = max
        self.step = step
        