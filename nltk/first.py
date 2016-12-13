
def integers():
    """Infinite sequence of integers."""
    i = 1
    while True:
        yield i
        i = i + 1

def squares():
    for i in integers():
        yield i * i

def take(n, seq):
    """Returns first n values from the given sequence."""
    seq = iter(seq)
    result = []
    try:
        for i in range(n):
            result.append(seq.next())
    except StopIteration:
        pass
    return result

def myGen(n):
    ret = []
    _myGen(n, ret=ret)
    for res in ret:
        yield res

def _myGen(n, ret):
    if n > 1:
        res = _myGen(n-1, ret)
        ret.append(res)
        return [i for i in range(n+1)]
    else:
        return []

x = myGen(5)
while 1:
    try:
        print x.next()
    except Exception as e:
        break

# print take(5, squares()) # prints [1, 4, 9, 16, 25]