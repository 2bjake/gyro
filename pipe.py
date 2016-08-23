from blocks import PipeBlock

class Pipe:
    def __init__(self, board, x, top_y, bottom_y):
        self.board = board
        self.x = x
        self.top_y = top_y
        self.bottom_y = bottom_y

        if top_y == bottom_y:
            board.get_block(x, top_y).set_position(PipeBlock.ALL)
        else:
            board.get_block(x, top_y).set_position(PipeBlock.TOP)
            board.get_block(x, bottom_y).set_position(PipeBlock.BOTTOM)

    def __repr__(self):
        return "top:({}, {}) bottom:({}, {})".format(self.x, self.top_y, self.x, self.bottom_y)