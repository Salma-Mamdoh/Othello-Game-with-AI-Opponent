def initialize_board():
    board = [[' ' for _ in range(8)] for _ in range(8)]
    board[3][3] = 'W'
    board[3][4] = 'B'
    board[4][3] = 'B'
    board[4][4] = 'W'
    return board

def print_board(board, available_moves=None, current_player=None):
    print("  |  0 |  1 |  2 |  3 |  4 |  5 | 6  |  7 ")
    print("+------------------------------------------+")
    for i in range(8):
        print(f"{i} |", end=" ")
        for j in range(8):
            if board[i][j] == 'W':
                print('W', end='  | ')
            elif board[i][j] == 'B':
                print('B', end='  | ')
            elif available_moves and (i, j) in available_moves:
                if current_player == 'B':
                    print('●', end='  | ')
                else:
                    print('○', end='  | ')
            else:
                print(' ', end='  | ')
        print("\n +------------------------------------------+")

def is_valid_move(board, row, col, player):
    if not (0 <= row < 8 and 0 <= col < 8):
        return False
    if board[row][col] != ' ':
        return False
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] != ' ' and board[r][c] != player:
            while 0 <= r < 8 and 0 <= c < 8 and board[r][c] != ' ':
                if board[r][c] == player:
                    return True
                r += dr
                c += dc
    return False

def get_available_moves(board, player):
    available_moves = []
    opponent = 'B' if player == 'W' else 'W'
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Only horizontal and vertical directions
    for i in range(8):
        for j in range(8):
            if board[i][j] == ' ':
                for dr, dc in directions:
                    r, c = i + dr, j + dc
                    if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
                        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
                            r += dr
                            c += dc
                        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                            available_moves.append((i, j))
                            break
    return available_moves


def make_move(board, row, col, player):
    if not is_valid_move(board, row, col, player):
        return False
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Only horizontal and vertical directions
    board[row][col] = player
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] != ' ' and board[r][c] != player:
            while 0 <= r < 8 and 0 <= c < 8 and board[r][c] != ' ':
                if board[r][c] == player:
                    r -= dr
                    c -= dc
                    while (r, c) != (row, col):
                        board[r][c] = player
                        r -= dr
                        c -= dc
                    break
                r += dr
                c += dc
    return True

def count_score(board):
    black_count = sum(row.count('B') for row in board)
    white_count = sum(row.count('W') for row in board)
    return black_count, white_count

def is_game_over(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def winner(board):
    black_count, white_count = count_score(board)
    if black_count > white_count:
        return 'Black'
    elif white_count > black_count:
        return 'White'
    else:
        return 'Draw'

# Example usage:
board = initialize_board()
current_player = 'B'
print_board(board, get_available_moves(board, current_player), current_player)

no_moves_count = 0  # Count consecutive turns with no available moves
while not is_game_over(board):
    available_moves = get_available_moves(board, current_player)
    if not available_moves:
        print(f"No available moves for {current_player}. Skipping turn.")
        no_moves_count += 1
        if no_moves_count == 2:  # Both players have no available moves
            break
        current_player = 'W' if current_player == 'B' else 'B'
        continue
    else:
        no_moves_count = 0  # Reset count if there are available moves

    print(f"Available moves for {current_player}: {available_moves}")
    row = int(input("Enter row: "))
    col = int(input("Enter col: "))
    if make_move(board, row, col, current_player):
        current_player = 'W' if current_player == 'B' else 'B'
        available_moves_black = get_available_moves(board, 'B')
        available_moves_white = get_available_moves(board, 'W')
        print_board(board, available_moves_black if current_player == 'B' else available_moves_white, current_player)
        print(f"Black: {count_score(board)[0]}, White: {count_score(board)[1]}")
    else:
        print("Invalid move, try again.")

if no_moves_count == 2 or is_game_over(board):  # Game over due to no available moves or full board
    print("Game over!")
    print("Winner:", winner(board))


