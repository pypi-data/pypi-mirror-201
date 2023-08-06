

class LastValueCallbacks:

    def __init__(self, value) -> None:
        self.last_value = value
        self.callbacks = []

    def append(self, callback):
        self.callbacks.append(callback)

    def remove(self, callback):
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def update(self, value):
        if value != self.last_value:
            for callback in self.callbacks:
                if callback != None:
                    callback(value)
        self.last_value = value