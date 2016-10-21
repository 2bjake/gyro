from blocks import *
import datetime
from point import Point
from state import GameState

def create_from_file(file_name):
    with open(file_name,'r') as f:
        lines = f.readlines()
        lines.reverse() # so that 0,0 is at the bottom
        height = len(lines);
        width = len(lines[0])

        block_matrix = [[Block() for y in range(height)] for x in range(width)]
        smick_pos_list = []
        coin_pos_list = []

        for y in range(height):
            line = lines[y]
            #TODO: if len(line) != width, freak out!
            for x in range(width):
                c = line[x]
                b = Block()
                pos = Point(x, y)

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
                elif c == 'D':
                    b = DoorBlock()
                elif c == 'c':
                    b = RopeBlock()
                    coin_pos_list.append(pos)
                elif c == 'C':
                    b = EmptyBlock()
                    coin_pos_list.append(pos)
                elif c == 'P':
                    b = EmptyBlock()
                    person_pos = pos
                elif c == 'p':
                    b = RopeBlock()
                    person_pos = pos
                elif c == 'S':
                    b = EmptyBlock()
                    smick_pos_list.append(pos)
                elif c == 's':
                    b = RopeBlock()
                    smick_pos_list.append(pos)

                block_matrix[x][y] = b

        return GameState(block_matrix, person_pos, smick_pos_list, coin_pos_list)

def write_to_file(game_state):
    block_matrix = game_state.board.block_matrix
    width = len(block_matrix)
    height = len(block_matrix[0])
    lines = []

    for y in range(height):
        line = ""
        for x in range(width):
            pos = Point(x, y)
            at_person = (pos == game_state.person.pos)
            at_smick = pos in game_state.smicks
            at_coin = pos in game_state.coins

            block = block_matrix[pos.x][pos.y]
            c = '?'

            if isinstance(block, EmptyBlock):
                if at_person:
                    c = 'P'
                elif at_smick:
                    c = 'S'
                elif at_coin:
                    c = 'C'
                else:
                    c = '.'
            elif isinstance(block, RopeBlock):
                if at_person:
                    c = 'p'
                elif at_smick:
                    c = 's'
                elif at_coin:
                    c = 'c'
                else:
                    c = '|'
            elif isinstance(block, GroundBlock):
                c = 'I'
            elif isinstance(block, PipeBlock) and block.color == colors.BLUE:
                c = 'B'
            elif isinstance(block, PipeBlock) and block.color == colors.RED:
                c = 'R'

            line += c
        lines.append(line)

    lines.reverse()

    file_name = "levels/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    f = open(file_name, 'w')
    f.write("\n".join(lines))
    f.close()