class TestMessageQueue:
    def __init__(self):
        self._events = []

    def publish(self, event):
        self._events.append(event)

    @property
    def events(self):
        return self._events