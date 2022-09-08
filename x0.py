gf = [['-', '-', '-'],                                  # game field matrix
      ['-', '-', '-'],
      ['-', '-', '-']]

game = []                                               # current game moves pattern


def pr_gf():                                            # printing game field
    print('Game field:')
    print('  0 1 2')
    print('0', gf[0][0], gf[0][1], gf[0][2])
    print('1', gf[1][0], gf[1][1], gf[1][2])
    print('2', gf[2][0], gf[2][1], gf[2][2])


def player_mov():                                       # let the human player make move
    while True:
        try:
            c, r, *a = map(int, input('Make your move(column row): ').split())
        except ValueError:                              # check input validity
            print('Enter two integers please!')         # output tip
            continue                                    # try again
        if r < 0 or r > 2 or c < 0 or c > 2:            # check input validity
            print('Out of game field!')                 # output tip
            continue                                    # try again
        if gf[r][c] == '-':                             # if the place is free
            gf[r][c] = 'x'                              # use it
            game.append(str(c))                         # put down the move
            game.append(str(r))                         # to the current game pattern
            return                                      # move done
        print('Occupied!')                              # try again


def machine_mov():                                      # let the program make move
    for i in range(len(gf)):                            # go down the lines
        for j in range(len(gf[i])):                     # go along the line
            if gf[i][j] != '-':                         # already used ?
                continue                                # look further
            game.append(str(j))                         # put down the move
            game.append(str(i))                         # to the current game pattern
            with open('exp.txt', 'a+') as rf:           # open logfile to check against loosing patterns
                rf.seek(0)                              # positioning to the beginning of the file
                found = 0                               # prepare flag
                for x in rf.readlines():                # read patterns
                    if x == ''.join(game) + '\n':       # compare to current pattern
                        found = 1                       # loosing pattern found
                        break                           # no more search
            if found:                                   # don't use it
                continue                                # move on
            gf[i][j] = '0'                              # put down the move to game field matrix
            return 0                                    # move made
    return 1                                            # no more place to make reasonable move


def vic_check_player():                                 # check if human has won
    if gf[0][0] == 'x' and gf[0][1] == 'x' and gf[0][2] == 'x':
        return 1
    if gf[1][0] == 'x' and gf[1][1] == 'x' and gf[1][2] == 'x':
        return 1
    if gf[2][0] == 'x' and gf[2][1] == 'x' and gf[2][2] == 'x':
        return 1
    if gf[0][0] == 'x' and gf[1][0] == 'x' and gf[2][0] == 'x':
        return 1
    if gf[0][1] == 'x' and gf[1][1] == 'x' and gf[2][1] == 'x':
        return 1
    if gf[0][2] == 'x' and gf[1][2] == 'x' and gf[2][2] == 'x':
        return 1
    if gf[0][0] == 'x' and gf[1][1] == 'x' and gf[2][2] == 'x':
        return 1
    if gf[0][2] == 'x' and gf[1][1] == 'x' and gf[2][0] == 'x':
        return 1                                        # three 'x' in a row found
    return 0                                            # three 'x' in a row not found


def vic_check_machine():                                # check if machine has won
    if gf[0][0] == '0' and gf[0][1] == '0' and gf[0][2] == '0':
        return 2
    if gf[1][0] == '0' and gf[1][1] == '0' and gf[1][2] == '0':
        return 2
    if gf[2][0] == '0' and gf[2][1] == '0' and gf[2][2] == '0':
        return 2
    if gf[0][0] == '0' and gf[1][0] == '0' and gf[2][0] == '0':
        return 2
    if gf[0][1] == '0' and gf[1][1] == '0' and gf[2][1] == '0':
        return 2
    if gf[0][2] == '0' and gf[1][2] == '0' and gf[2][2] == '0':
        return 2
    if gf[0][0] == '0' and gf[1][1] == '0' and gf[2][2] == '0':
        return 2
    if gf[0][2] == '0' and gf[1][1] == '0' and gf[2][0] == '0':
        return 2                                        # three '0' in a row found
    return 0                                            # three '0' in a row not found


while True:                                             # main loop
    pr_gf()                                             # show current game field situation
    player_mov()                                        # make human move
    if vic_check_player():                              # check the result of human move
        del game[-2:]                                   # delete the last move from pattern
        with open('exp.txt', 'a+') as wf:               # open experience logfile
            wf.writelines(game)                         # put down another pattern not to be repeated
            wf.write('\n')                              # EOL after the pattern
        pr_gf()                                         # show current game field situation
        print("You won! I won't do this move again.")   # admit lost
        break                                           # finished, out of main loop
    if machine_mov():                                   # make machine move
        pr_gf()                                         # show current game field situation
        print("It's a draw...")                         # no more free place
        break                                           # finished, out of main loop
    if vic_check_machine():                             # check the result of machine move
        pr_gf()                                         # show current game field situation
        print('Well, I won.')                           # admit victory
        break                                           # finished, out of main loop
