from blocks import *
import datetime

def create_from_file(file_name):
    with open(file_name,'r') as f:
        lines = f.readlines()
        lines.reverse() # so that 0,0 is at the bottom
        height = len(lines);
        width = len(lines[0])

        block_matrix = [[Block() for y in range(height)] for x in range(width)]
        smick_pos_list = []

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
                elif c == 'p':
                    b = RopeBlock()
                    person_pos = (x, y)
                elif c == 'S':
                    b = EmptyBlock()
                    smick_pos_list.append((x, y))
                elif c == 's':
                    b = RopeBlock()
                    smick_pos_list.append((x, y))

                block_matrix[x][y] = b

        return block_matrix, person_pos, smick_pos_list

def write_to_file(block_matrix, person, all_smicks):
    width = len(block_matrix)
    height = len(block_matrix[0])
    lines = []

    for y in range(height):
        line = ""
        for x in range(width):
            at_person = x == person.start_x and y == person.start_y
            at_smick = (x, y) in all_smicks

            block = block_matrix[x][y]
            c = '?'

            if isinstance(block, EmptyBlock):
                if at_person:
                    c = 'P'
                elif at_smick:
                    c = 'S'
                else:
                    c = '.'
            elif isinstance(block, RopeBlock):
                if at_person:
                    c = 'p'
                elif at_smick:
                    c = 's'
                else:
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