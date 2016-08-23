from board import Board
from blocks import *

def create_board_from_file(file_name):
    with open(file_name,'r') as f:
        lines = f.readlines()
        lines.reverse() # so that 0,0 is at the bottom
        height = len(lines);
        width = len(lines[0])

        block_matrix = [[Block() for y in range(height)] for x in range(width)]

        for y in range(0, height):
            line = lines[y]
            #TODO: if len(line) != width, freak out!
            for x in range(0, width):
                c = line[x]

                if c == ' ':
                    b = EmptyBlock()
                elif c == 'T':
                    b = GroundBlock()
                elif c == 'B':
                    b = PipeBlock(colors.BLUE)
                elif c == 'R':
                    b = PipeBlock(colors.RED)
                else:
                    b = Block()

                block_matrix[x][y] = b

        return Board(block_matrix)