
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

dic = {0,1,2,3}
val = 'a'
print dict([val, dic])