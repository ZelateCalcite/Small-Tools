def f(*args):
    t = (i for i in args)
    print(args)
    print(type(args))


def fn(**kwargs):
    print(kwargs)


f(1, 2, '3', 'a', 5, 6, 7, 8)

fn(a=2, b=1)
