class NimState:
    """
    Initialize the Nim game state.

    Args:
        heaps (list of int): A list representing the number of objects in each heap.
    """
    def __init__(self, heaps):
        self.heaps = heaps[:]  # Copy to avoid mutation
        self.history = []  # List of moves as (heap_index, num_removed)

    """
    Attempt to remove objects from a heap.

    Args:
        heap_index (int): Index of the heap to remove from.
        num_removed (int): Number of objects to remove.

    Returns:
        bool: True if the move was successful, False otherwise.
    """
    def move(self, heap_index, num_removed):
        if 0 <= heap_index < len(self.heaps) and 1 <= num_removed <= self.heaps[heap_index]:
            self.heaps[heap_index] -= num_removed
            self.history.append((heap_index, num_removed))
            return True
        return False

    """
    Check if the game is over (all heaps are empty).

    Returns:
        bool: True if game is over, False otherwise.
    """
    def is_game_over(self):
        return all(heap == 0 for heap in self.heaps)

    """
    Generate a list of all legal moves from the current state.

    Returns:
        list of tuple: Each tuple is a legal move (heap_index, num_removed).
    """
    def get_legal_moves(self):
        moves = []
        for i, count in enumerate(self.heaps):
            for remove in range(1, count + 1):
                moves.append((i, remove))
        return moves

    """
    Return a string representation of the current heap states.

    Returns:
        str: String showing the number of objects in each heap.
    """
    def __str__(self):
        return str(self.heaps)

    """
    Display a visual representation of the current Nim state.
    """
    def display(self):
        print("Current Heaps:")
        for i, count in enumerate(self.heaps):
            print(f"Heap {i}: {'●' * count} ({count})")
        print("-" * 30)