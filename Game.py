import tkinter as tk
from tkinter import simpledialog, messagebox
import math

def utility(board):
    (b, w) = count_score(board)
    return w - b

def find_best_move(board, available_moves, level):
    if level == 1:
        depth = 1
    elif level == 2:
        depth = 3
    else:
        depth = 5
    _, i, j = minimax(board, 0, True, -math.inf, math.inf, depth, available_moves)
    return i, j
def minimax(board, depth, is_maximizing, alpha, beta, max_depth, available_moves):
    if depth == max_depth or not available_moves:
        return utility(board), None, None  # Return None for row and column
    temp_board = [row[:] for row in board]   # Create a copy of the board
    best = -math.inf if is_maximizing else math.inf
    best_row, best_col = available_moves[0]  # Initialize with some arbitrary values
    for (i, j) in available_moves:
        make_move(temp_board, i, j, 'W' if is_maximizing else 'B')
        temp_available_moves = get_available_moves(temp_board, 'B' if is_maximizing else 'W')
        if temp_available_moves:
            val, _, _ = minimax(temp_board, depth + 1, not is_maximizing, alpha, beta, max_depth, temp_available_moves)
        else:
            val = utility(temp_board)
        if is_maximizing:
            if val > best:
                best = val
                best_row, best_col = i, j
            elif val == best:  # Update if the score is the same
                best_row, best_col = i, j
            alpha = max(alpha, val)
        else:
            if val < best:
                best = val
                best_row, best_col = i, j
            elif val == best:  # Update if the score is the same
                best_row, best_col = i, j
            beta = min(beta, val)
        temp_board = [row[:] for row in board]   # Undo
        if beta <= alpha:  # Alpha-beta pruning
            break
    #print("Move:", (best_row, best_col), "Score:", best)  # Debugging line
    return best, best_row, best_col
def initialize_board():
    board = [[' ' for _ in range(8)] for _ in range(8)]
    board[3][3] = 'W'
    board[3][4] = 'B'
    board[4][3] = 'B'
    board[4][4] = 'W'
    return board


score_label = None  # Global variable to hold the score label
player_turn_label = None  # Global variable to hold the player turn label
current_player = 'B'  # Global variable to keep track of the current player
def print_board(board, available_moves=None, current_player=None):
    global score_label, player_turn_label

    black_count, white_count = count_score(board)  # Get the current score
    score_text = f"Black (B): {black_count}\nWhite (W): {white_count}"  # Score text

    if score_label:
        score_label.config(text=score_text)  # Update the text of the existing label
    else:
        score_label = tk.Label(root, text=score_text, font=('Arial', 14), bg="lightgray")
        score_label.pack(padx=20, pady=10, side="top", fill="x")

    # Display player's turn
    if player_turn_label:
        player_turn_label.config(text=f"Current Turn: {current_player}")
    else:
        player_turn_label = tk.Label(root, text=f"Current Turn: {current_player}", font=('Arial', 14), bg="lightgray")
        player_turn_label.pack(padx=20, pady=5, side="top", fill="x")

    for widget in board_frame.winfo_children():
        widget.destroy()  # Clear existing buttons before updating

    for i in range(8):
        for j in range(8):
            color = 'lime green'

            if board[i][j] == 'W':
                color = 'white'
            elif board[i][j] == 'B':
                color = 'black'

            if available_moves and (i, j) in available_moves:
                color = 'forest green'

            cell_button = tk.Button(board_frame, width=4, height=2, bg=color,command=lambda i=i, j=j: make_move_gui(i, j))
            cell_button.grid(row=i, column=j)

def make_move_gui(row, col):
    global current_player, board, mode, level
    if is_game_over(board):
        winner(board)
        return

    available_moves = get_available_moves(board, current_player)

    if mode == "PvP" or (mode == "PvC" and current_player == 'B'):
        if (row, col) in available_moves:
            make_move_and_check(board, row, col)
        else:
            messagebox.showerror("Invalid Move", "Please select a valid move.")
        # Computer plays in PvC mode
        if mode == "PvC" and current_player == 'W':
            computer_play()


def make_move_and_check(board, row, col):
    global current_player
    make_move(board, row, col, current_player)
    current_player = 'W' if current_player == 'B' else 'B'  # Switch players
    available_moves = get_available_moves(board, current_player)
    print_board(board, available_moves=available_moves, current_player=current_player)

    # Check if the next player has no available moves
    if not available_moves:
        messagebox.showinfo("No Available Moves", f"{current_player} has no available moves.")
        current_player = 'W' if current_player == 'B' else 'B'  # Switch to the other player's turn
        available_moves = get_available_moves(board, current_player)
        print_board(board, available_moves=available_moves, current_player=current_player)


def computer_play():
    global current_player, board
    available_moves = get_available_moves(board, current_player)
    (row, col) = find_best_move(board, available_moves, level)

    if is_game_over(board):
        winner(board)
        return

    make_move_and_check(board, row, col)

    # if B has no Available moves
    if current_player == 'W':
        computer_play()


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

def count_score(board):
    black_count = sum(row.count('B') for row in board)
    white_count = sum(row.count('W') for row in board)
    return black_count, white_count

def winner(board):
    black_count, white_count = count_score(board)
    if black_count > white_count:
        messagebox.showinfo("Game Over", "Black wins!")
    elif white_count > black_count:
        messagebox.showinfo("Game Over", "White wins!")
    else:
        messagebox.showinfo("Game Over", "It's a draw!")



def is_game_over(board):
    if not any(get_available_moves(board, player) for player in ['B', 'W']):
        messagebox.showinfo("No Available Moves", "Neither player (B or W) has any available moves.")
        return True
    return all(' ' not in row for row in board)

def show_board(game_mode, difficulty_level=1):
    global board, current_player, mode, level
    mode = game_mode
    board = initialize_board()
    current_player = 'B'
    available_moves = get_available_moves(board, current_player)
    print_board(board, available_moves=available_moves, current_player=current_player)
    level = difficulty_level  # Set the difficulty level

def show_difficulty_options():
    global level
    level = simpledialog.askstring("Difficulty Level", "Please enter the Difficulty level:                "
                                                       "\n1) Easy\n2) Medium\n3) Hard")
    if level is None:
        return  # Exit the function if dialog was closed
    if level and level.isdigit() and int(level) in [1, 2, 3]:
        print("Selected difficulty:", level)
        show_board(game_mode="PvC", difficulty_level=int(level))
    else:
        messagebox.showwarning("Invalid Input", "Please enter a number between 1 and 3.")

# Title Label
def create_title():
    title_label = tk.Label(root, text="Welcome To Othello!", font=('Arial', 24), bg='black', fg='white')
    title_label.pack(pady=20)
# Game Mode Buttons
def create_game_mode_buttons():
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    button_pvp = tk.Button(button_frame, text="Player vs Player", font=('Arial', 18),
                           command=lambda: show_board(game_mode="PvP"), background='black', fg='white')
    button_pvp.pack(side="left")

    button_pvc = tk.Button(button_frame, text="Player vs Computer", font=('Arial', 18), command=show_difficulty_options,
                           background='black', fg='white')
    button_pvc.pack(side="right")

def create_info_frame():
    global score_label, player_turn_label
    info_frame = tk.Frame(root)
    info_frame.pack(pady=10)

    score_label = tk.Label(info_frame, text="Score: -", font=('Arial', 16))
    score_label.pack(side="left", padx=20)

    player_turn_label = tk.Label(info_frame, text="Current Turn: -", font=('Arial', 16))
    player_turn_label.pack(side="right", padx=20)

# Board Frame
def create_board_frame():
    global board_frame
    board_frame = tk.Frame(root, bg="lightgray", width=0, height=0, highlightbackground="gray", highlightthickness=2)
    board_frame.pack()

def main():
    global root
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Othello Board Game")
    background_image = tk.PhotoImage(file="wooden.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    create_title()
    create_game_mode_buttons()
    create_info_frame()
    create_board_frame()

    root.mainloop()

if __name__ == "__main__":
    main()
