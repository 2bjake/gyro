from pygame import Rect

class Board:
    def __init__(self, block_matrix):
        self.block_matrix = block_matrix
        self.rect = Rect(0, 0, len(block_matrix), len(block_matrix[0]))

    def is_inside_border(self, pos):
        return (self.rect.left < pos.x < self.rect.right - 1 and
                self.rect.top < pos.y < self.rect.bottom - 1)

    def add_block_at(self, pos, block):
        if self.is_inside_border(pos):
            self._set_block(pos, block)
            return True
        return False

    def _set_block(self, pos, block):
        self.block_matrix[pos.x][pos.y] = block

    def swap_blocks(self, a_pos, b_pos):
        temp = self.get_block(a_pos)
        self._set_block(a_pos, self.get_block(b_pos))
        self._set_block(b_pos, temp)

    def get_block(self, pos):
        return self.block_matrix[pos.x][pos.y]
