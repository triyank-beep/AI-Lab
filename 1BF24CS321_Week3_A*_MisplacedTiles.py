import heapq

def calculate_misplaced_tiles(state, goal_state):
    """
    Counts how many tiles are not in their correct goal position.
    The blank space (0) is not counted as a misplaced tile.
    """
    count = 0
    for i in range(9):
        if state[i] != 0: # Ignore the blank space
            if state[i] != goal_state[i]:
                count += 1
    return count

def get_neighbors(state):
    neighbors = []
    zero_idx = state.index(0)
    r, c = divmod(zero_idx, 3)
    
    # Grid movements for the empty slot (0): Up, Down, Left, Right
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            n_idx = nr * 3 + nc
            new_state = list(state)
            new_state[zero_idx], new_state[n_idx] = new_state[n_idx], new_state[zero_idx]
            neighbors.append(tuple(new_state))
            
    return neighbors

def solve_8_puzzle_misplaced(start_state, goal_state):
    # open_list stores: (f_score, g_score, current_state, path_history)
    open_list = []
    h_init = calculate_misplaced_tiles(start_state, goal_state)
    heapq.heappush(open_list, (h_init, 0, start_state, [start_state]))
    
    g_scores = {start_state: 0}
    closed_set = set()
    
    print(f"\n--- Initial State Evaluation ---")
    print(f"Starting Board Layout: {start_state}")
    print(f"Goal Board Layout:     {goal_state}")
    print(f"Initial Misplaced Tiles (h): {h_init}\n")
    
    debug_counter = 0

    while open_list:
        f, g, current, path = heapq.heappop(open_list)
        
        if current == goal_state:
            return path
            
        if current in closed_set:
            continue
        closed_set.add(current)
        
        # Log the first 3 queue pops to visualize priority ranking
        if debug_counter < 3:
            print(f"[Queue Pop] Processing state with lowest f={f} (g={g}, h={f-g})")
            print(f"  Layout: {current[0:3]} | {current[3:6]} | {current[6:9]}")
            debug_counter += 1
        
        for neighbor in get_neighbors(current):
            if neighbor in closed_set:
                continue
                
            tentative_g = g + 1
            if tentative_g < g_scores.get(neighbor, float('inf')):
                g_scores[neighbor] = tentative_g
                h_score = calculate_misplaced_tiles(neighbor, goal_state)
                f_score = tentative_g + h_score
                heapq.heappush(open_list, (f_score, tentative_g, neighbor, path + [neighbor]))
                
    return None

def get_user_board_input(prompt_text):
    """Safely collects and processes a 9-digit sequence from user input."""
    while True:
        try:
            print(prompt_text)
            user_input = input("Numbers: ")
            # Parse space-separated or comma-separated digits
            cleaned_input = user_input.replace(",", " ").split()
            
            # Map elements to integers
            board_tuple = tuple(int(x) for x in cleaned_input)
            
            if len(board_tuple) != 9:
                print("Error: You must enter exactly 9 numbers (0 through 8).\n")
                continue
            if set(board_tuple) != set(range(9)):
                print("Error: Must contain unique numbers from 0 to 8 (where 0 is blank).\n")
                continue
                
            return board_tuple
        except ValueError:
            print("Error: Invalid numeric formatting. Please enter integers only.\n")

# --- Interactive Main Execution Loop ---
if __name__ == "__main__":
    print("=== Interactive A* 8-Puzzle Solver ===")
    print("Provide 9 digits separated by spaces. Example: 2 8 3 1 6 4 0 7 5\n")
    
    # Collect dynamic user configurations
    initial_board = get_user_board_input("Enter the INITIAL board configuration:")
    target_board = get_user_board_input("\nEnter the GOAL board configuration:")
    
    solution_path = solve_8_puzzle_misplaced(initial_board, target_board)

    print("\n--- Execution Search Complete ---")
    if solution_path:
        print(f"🎯 Solved Successfully! Total movements needed: {len(solution_path) - 1}\n")
        for step, board in enumerate(solution_path):
            print(f"Step {step}:")
            print(f"  {board[0:3]}")
            print(f"  {board[3:6]}")
            print(f"  {board[6:9]}")
            print("-" * 15)
    else:
        print("❌ No solution found. This layout translation is mathematically unreachable.")
