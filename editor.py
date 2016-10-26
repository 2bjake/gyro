from blocks import *
import colors

class Editor:
    def __init__(self):
        self.index = 0
        self.blocks = [PipeBlock(colors.RED), PipeBlock(colors.BLUE), EmptyBlock(), RopeBlock(), GroundBlock(), DoorBlock()]

    def get_selected_block(self):
        return self.blocks[self.index]
