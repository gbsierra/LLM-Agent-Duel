class HanoiState:
    """
        Initialize the Tower of Hanoi state.

        Args:
            num_disks (int): The number of disks in the puzzle.
    """
    def __init__(self, num_disks):
        self.num_disks = num_disks
        # Initialize pegs: all disks are on the first peg in descending order
        self.pegs = [[i for i in range(num_disks, 0, -1)], [], []]
        # History of moves made (as tuples of (from_peg, to_peg))
        self.history = []

    """
        Attempt to move the top disk from one peg to another.

        Args:
            from_peg (int): Index of the source peg (0-2).
            to_peg (int): Index of the destination peg (0-2).

        Returns:
            bool: True if the move was successful, False otherwise.
    """
    def move(self, from_peg, to_peg):
        if self.pegs[from_peg] and (not self.pegs[to_peg] or self.pegs[from_peg][-1] < self.pegs[to_peg][-1]):
            disk = self.pegs[from_peg].pop()
            self.pegs[to_peg].append(disk)
            self.history.append((from_peg, to_peg))
            return True
        return False
    
    """
        Check if the puzzle is solved (all disks moved to the third peg).

        Returns:
            bool: True if solved, False otherwise.
    """
    def is_solved(self):
        return len(self.pegs[2]) == sum(len(peg) for peg in self.pegs)

    """
        Generate a list of all legal moves from the current state.

        Returns:
            list of tuple: Each tuple is a legal move (from_peg, to_peg).
    """
    def get_legal_moves(self):
        moves = []
        for from_peg in range(3):
            if not self.pegs[from_peg]:
                continue  # Skip empty pegs
            for to_peg in range(3):
                if from_peg == to_peg:
                    continue  # Skip moves to the same peg
                if not self.pegs[to_peg] or self.pegs[from_peg][-1] < self.pegs[to_peg][-1]:
                    moves.append((from_peg, to_peg))
        return moves

    """
        Return a string representation of the current peg states.

        Returns:
            str: String showing the contents of each peg.
    """
    def __str__(self):
        return str(self.pegs)

    """
        Display a visual representation of the current Tower of Hanoi state.
    """
    def display(self):
        max_height = self.num_disks
        peg_width = self.num_disks * 2 + 1
        spacing = ' '

        def render_disk(size):
            """
            Render a single disk or empty space.

            Args:
                size (int): Size of the disk (0 for empty).

            Returns:
                str: A string representing the disk.
            """
            if size == 0:
                return ' ' * peg_width
            else:
                pad = self.num_disks - size
                disk = '=' * (size * 2 - 1)
                return ' ' * pad + disk + ' ' * pad

        # Pad each peg to the full height with zeros (representing empty slots)
        padded_pegs = []
        for peg in self.pegs:
            padded = peg[:] + [0] * (max_height - len(peg))
            padded_pegs.append(padded)

        # Print each level of the pegs from top to bottom
        for level in reversed(range(max_height)):
            row = spacing.join(render_disk(padded_pegs[peg][level]) for peg in range(3))
            print(row)

        # Print the base and peg labels
        total_width = (peg_width + len(spacing)) * 3 - len(spacing)
        print('-' * total_width)
        label_row = spacing.join(str(i).center(peg_width) for i in range(3))
        print(label_row)
        print()