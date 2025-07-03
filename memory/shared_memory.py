class SharedMemory:
    """
    Shared memory for agents to remember past moves and visited states.
    """
    def __init__(self):
        self.moves = []              # List of (from_peg, to_peg) or (heap_index, num_removed)
        self.visited_states = set()  # Set of game states as strings

    """
    Update memory with a new move and resulting state.

    Args:
        move (tuple): The move that was made.
        state (object): The current game state (must have a .pegs or .heaps attribute).
    """
    def update(self, move, state):
        self.moves.append(move)
        self.visited_states.add(str(state.pegs if hasattr(state, "pegs") else state.heaps))

    """
    Get the most recent moves.

    Args:
        n (int): Number of recent moves to return.

    Returns:
        list: A list of recent moves.
    """
    def get_recent(self, n=5):
        return self.moves[-n:]

    """
    Check if a state has been seen before.

    Args:
        state (object): The current game state.

    Returns:
        bool: True if the state has been visited, False otherwise.
    """
    def has_seen(self, state):
        return str(state.pegs if hasattr(state, "pegs") else state.heaps) in self.visited_states