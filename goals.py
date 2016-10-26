class Coin:
    def __init__(self, pos):
        self.pos = pos
        self.reset()

    def reset(self):
        self.is_available = True
