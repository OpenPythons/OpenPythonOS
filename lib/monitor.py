from component import Component

__all__ = ["Monitor", "monitor", "_set_monitor"]


class Monitor:
    def __init__(self, gpu: Component):
        self.gpu = gpu
        self.w = 80
        self.h = 25
        self.x = 1
        self.y = 1
        self.bc = 0

    def scroll(self):
        self.gpu.copy(1, 2, self.w, self.h, 0, - 1)
        self.gpu.fill(1, self.h, self.w, 1, " ")

    def put(self, char: str):
        assert len(char) == 1
        if char == "\n":
            self.x = 1
            self.y += 1

        if self.x > self.w:
            self.x = 1
            self.y += 1

        if self.y > self.h:
            self.scroll()
            self.y = self.h

        if char == "\r" or char == "\n":
            return

        if self.bc > 0:
            self.bc -= 1
        elif char == "\b":
            self.x -= 1
            self.gpu.set(self.x, self.y, " ")
            self.bc = 3
        else:
            self.gpu.set(self.x, self.y, char)
            self.x += 1


monitor = None


def _set_monitor(obj):
    global monitor
    monitor = obj
