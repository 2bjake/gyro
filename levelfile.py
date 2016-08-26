from blocks import *
import datetime

def create_from_file(file_name):
    with open(file_name,'r') as f:
        lines = f.readlines()
        lines.reverse() # so that 0,0 is at the bottom
        height = len(lines);
        width = len(lines[0])

        block_matrix = [[Block() for y in range(height)] for x in range(width)]

        for y in range(height):
            line = lines[y]
            #TODO: if len(line) != width, freak out!
            for x in range(width):
                c = line[x]
                b = Block()

                if c == '.':
                    b = EmptyBlock()
                elif c == '|':
                    b = RopeBlock()
                elif c == 'I':
                    b = GroundBlock()
                elif c == 'B':
                    b = PipeBlock(colors.BLUE)
                elif c == 'R':
                    b = PipeBlock(colors.RED)
                elif c == 'G':
                    b = PipeBlock(colors.GREEN)
                elif c == 'Y':
                    b = PipeBlock(colors.YELLOW)
                elif c == 'P':
                    b = EmptyBlock()
                    person_pos = (x, y)

                block_matrix[x][y] = b

        return block_matrix, person_pos

def write_to_file(block_matrix, person_x, person_y):
    width = len(block_matrix)
    height = len(block_matrix[0])

    lines = []

    for y in range(height):
        line = ""
        for x in range(width):
            block = block_matrix[x][y]
            c = '?'

            if x == person_x and y == person_y:
                c = 'P'
            elif isinstance(block, EmptyBlock):
                c = '.'
            elif isinstance(block, RopeBlock):
                c = '|'
            elif isinstance(block, GroundBlock):
                c = 'I'
            elif isinstance(block, PipeBlock) and block.color == colors.BLUE:
                c = 'B'
            elif isinstance(block, PipeBlock) and block.color == colors.RED:
                c = 'R'

            line += c
        line += '\n'
        lines.append(line)

    lines.reverse()

    file_name = "levels/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    f = open(file_name, 'w')
    f.writelines(lines)
    f.close()