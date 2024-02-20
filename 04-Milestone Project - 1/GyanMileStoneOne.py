import random
#import pdb
#pdb.set_trace()

def display_board(board):
    board0=board[0:3]
    board1=board[3:6]
    board2=board[6:9]

    print(board0)
    print(board1)
    print(board2)

def player_input():
    X_or_O = ""
    while not (X_or_O == "X" or X_or_O == "O"):
        X_or_O = input("Do you want to play X or O? Input: (X/O)")
        
        if X_or_O == "X" or X_or_O == "x":
            return("X", "O")
        elif X_or_O == "O" or X_or_O == "o":
            return("O", "X")

def place_marker(board, X_or_O, position):
    board[position] = X_or_O

def win_check(board,mark):
    return ((board[0] == mark and board[1] == mark and board[2] == mark) or
    (board[3] == mark and board[4] == mark and board[5] == mark) or
    (board[6] == mark and board[7] == mark and board[8] == mark) or
    (board[0] == mark and board[3] == mark and board[6] == mark) or
    (board[1] == mark and board[4] == mark and board[7] == mark) or
    (board[2] == mark and board[5] == mark and board[8] == mark) or
    (board[0] == mark and board[4] == mark and board[8] == mark) or
    (board[2] == mark and board[4] == mark and board[6] == mark))

def choose_first():
    random_player = random.choice(["Player 1", "Player 2"])
    return random_player

def space_check(board, position):
    return type(board[position]) == type(8)

def full_board_check(board):
    for space in range(0,9):
        if space_check(board, space):
            return False
    return True

def player_choice(board):
    position = -1
    while position not in [0,1,2,3,4,5,6,7,8] or not space_check(board, position):
        position = int(input('Choose your next position: (0-8) '))
    return position

def replay():
    return input('Do you want to play again? Input (Y/N)').lower().startswith('y')

print('Welcome to Tic Tac Toe!')

while True:
    board = [0,1,2,3,4,5,6,7,8]
    (player1_marker, player2_marker) = player_input()
    turn = choose_first()
    print(turn + ' will go first.')
    
    play_game = input('Are you ready to play? Input: (Y/N)')
    
    if play_game.lower()[0] == 'y':
        game_on = True
    else:
        game_on = False

    while game_on:
        if turn == 'Player 1':
            # Player1's turn.
            
            display_board(board)
            position = player_choice(board)
            place_marker(board, player1_marker, position)

            if win_check(board, player1_marker):
                display_board(board)
                print('Player 1 has won!')
                game_on = False
            elif full_board_check(board):
                display_board(board)
                print('The game is a draw!')

            else:
                turn="Player 2"
                
        else:
            # Player2's turn.
            
            display_board(board)
            position = player_choice(board)
            place_marker(board, player2_marker, position)

            if win_check(board, player2_marker):
                display_board(board)
                print('Player 2 has won!')
                game_on = False
            elif full_board_check(board):
                display_board(board)
                print('The game is a draw!')
                
            else:
                turn="Player 1"
    
    if not replay():
        break

    #1-9
    #user input