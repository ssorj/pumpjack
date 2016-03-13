import proton.reactor as _reactor

class Container(object):
    def __init__(self, handler=None, id=None):
        self._container = _reactor.Container(handler, id)
        print(self._container)

    def run(self):
        return self._container.run()
