

try:
    x = 2
    print(f'all done, x = {x}')
    assert x < 2, 'test message'
except AssertionError as err:
    print(err.args[0])
