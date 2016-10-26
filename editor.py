class Editor:
    def __init__(self, blocks):
        self.index = 0
        self.blocks = blocks

    def get_selected_block(self):
        return self.blocks[self.index]
