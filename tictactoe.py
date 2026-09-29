# Tic Tac Toe: Human (X) vs Agent (O) using Minimax

board = [" "] * 9

def show():
    print()
    for i in range(0, 9, 3):
        print(" " + board[i] + " | " + board[i+1] + " | " + board[i+2])
        if i < 6:
            print("---+---+---")
    print()

def winner():
    lines = [(0,1,2),(3,4,5),(6,7,8),
             (0,3,6),(1,4,7),(2,5,8),
             (0,4,8),(2,4,6)]
    for a, b, c in lines:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None

def full():
    return " " not in board

# Minimax: agent (O) maximizes, human (X) minimizes
def minimax(is_agent_turn):
    w = winner()
    if w == "O":
        return 1
    if w == "X":
        return -1
    if full():
        return 0

    if is_agent_turn:
        best = -2
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                best = max(best, minimax(False))
                board[i] = " "
        return best
    else:
        best = 2
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                best = min(best, minimax(True))
                board[i] = " "
        return best

def agent_move():
    best_score = -2
    best_pos = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_pos = i
    board[best_pos] = "O"

def human_move():
    while True:
        try:
            pos = int(input("Your move (1-9): ")) - 1
            if 0 <= pos <= 8 and board[pos] == " ":
                board[pos] = "X"
                return
            print("Invalid or taken cell, try again.")
        except ValueError:
            print("Enter a number 1-9.")

print("You are X, Agent is O. Cells are numbered 1-9 (left to right, top to bottom).")
show()

while True:
    human_move()
    show()
    if winner() or full():
        break
    print("Agent's move:")
    agent_move()
    show()
    if winner() or full():
        break

w = winner()
if w == "X":
    print("You win!")
elif w == "O":
    print("Agent wins!")
else:
    print("It's a draw!")
