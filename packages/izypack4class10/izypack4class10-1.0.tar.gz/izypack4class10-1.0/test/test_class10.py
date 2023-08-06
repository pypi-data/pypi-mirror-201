from izypack4class10 import class10

def test(a=class10()):
    a.plus10()
    assert a.memory == 10
