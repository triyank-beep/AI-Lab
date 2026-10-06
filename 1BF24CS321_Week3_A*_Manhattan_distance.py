import heapq

def manhattan_distance(state, goal_state):
    """
    Calculates the sum of absolute horizontal and vertical distances 
    of each tile from its correct goal position.
    """
    distance = 0
    for i in range(9):
        val = state[i]
        if val != 0:
            goal_idx = goal_state.index(val)
            curr_r, curr_c = divmod(i, 3)
            goal_r, goal_c = divmod(goal_idx, 3)
            distance += abs(curr_r - goal_r) + abs(curr_c - goal_c)
    return distance

def get_neighbors(state):
    neighbors = []
    zero_idx = state.index(0)
    r, c = divmod(zero_idx, 3)
    
    # Possible movements for the empty tile (0): up, down, left, right
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            n_idx = nr * 3 + nc
            new_state = list(state)
            new_state[zero_idx], new_state[n_idx] = new_state[n_idx], new_state[zero_idx]
            neighbors.append(tuple(new_state))
            
    return neighbors

def solve_8_puzzle(start_state, goal_state):
    # Priority queue stores tuples: (f_score, g_score, state, path)
    open_list = []
    h_init = manhattan_distance(start_state, goal_state)
    heapq.heappush(open_list, (h_init, 0, start_state, [start_state]))
    
    g_scores = {start_state: 0}
    closed_set = set()
    
    while open_list:
        f, g, current, path = heapq.heappop(open_list)
        
        if current == goal_state:
            return path
            
        if current in closed_set:
            continue
        closed_set.add(current)
        
        for neighbor in get_neighbors(current):
            if neighbor in closed_set:
                continue
                
            tentative_g = g + 1
            if tentative_g < g_scores.get(neighbor, float('inf')):
                g_scores[neighbor] = tentative_g
                f_score = tentative_g + manhattan_distance(neighbor, goal_state)
                heapq.heappush(open_list, (f_score, tentative_g, neighbor, path + [neighbor]))
                
    return None

def get_user_board_input(prompt_text):
    """Safely collects and processes a 9-digit sequence from user input."""
    while True:
        try:
            print(prompt_text)
            user_input = input("Numbers: ")
            # Clean and split elements by spaces or commas
            cleaned_input = user_input.replace(",", " ").split()
            
            # Map strings to integers
            board_tuple = tuple(int(x) for x in cleaned_input)
            
            if len(board_tuple) != 9:
                print("Error: You must enter exactly 9 numbers (0 through 8).\n")
                continue
            if set(board_tuple) != set(range(9)):
                print("Error: Must contain unique numbers from 0 to 8 (where 0 is blank).\n")
                continue
                
            return board_tuple
        except ValueError:
            print("Error: Please input valid integers only.\n")

# --- Interactive Main Loop ---
if __name__ == "__main__":
    print("=== Interactive A* 8-Puzzle Solver (Manhattan Distance) ===")
    print("Provide 9 digits separated by spaces. Example: 2 8 3 1 6 4 0 7 5\n")
    
    # Accept dynamic inputs from terminal
    initial_board = get_user_board_input("Enter the INITIAL board configuration:")
    target_board = get_user_board_input("\nEnter the GOAL board configuration:")
    
    solution_path = solve_8_puzzle(initial_board, target_board)

    print("\n--- Output Summary ---")
    if solution_path:
        print(f"🎯 Solved Successfully! Total steps to solve: {len(solution_path) - 1}\n")
        for step, board in enumerate(solution_path):
            print(f"Step {step}:")
            print(f"  {board[0:3]}")
            print(f"  {board[3:6]}")
            print(f"  {board[6:9]}")
            print("-" * 15)
    else:
        print("❌ No solution found. This layout configuration is unreachable.")
