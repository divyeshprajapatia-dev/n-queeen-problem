class NQueenSolver:
    def __init__(self, n, first_row_col=None):
        self.n = n
        self.board = [-1] * n  # board[row] = col
        self.first_row_col = first_row_col
        self.steps = self.solve_step_by_step(0)

    def is_safe(self, row, col):
        """Check if it's safe to place a queen at board[row] = col"""
        for r in range(row):
            c = self.board[r]
            if c == col or abs(c - col) == abs(r - row):
                return False, r, c  # Return conflict details
        return True, -1, -1

    def solve_step_by_step(self, row):
        """Generator that yields the state of the board at each step."""
        if row == self.n:
            yield "FOUND_SOLUTION", list(self.board), "Solution Found!", None
            return True

        # If this is the first row and a column is locked, only try that column
        if row == 0 and self.first_row_col is not None:
            cols_to_try = [self.first_row_col]
        else:
            cols_to_try = range(self.n)

        for col in cols_to_try:
            # Place queen tentatively
            self.board[row] = col
            yield "PLACING", list(self.board), f"Checking Row {row}, Col {col}...", (row, col)

            safe, conf_r, conf_c = self.is_safe(row, col)
            
            if safe:
                yield "SAFE", list(self.board), f"Safe at ({row}, {col}). Proceeding...", (row, col)
                # Recursively solve for next row
                # We yield from the recursive call to propagate steps up
                found = yield from self.solve_step_by_step(row + 1)
                
                if found:
                    return True # Stop after finding first solution? Or keep going? 
                                # Requirement says "One valid solution OR Number of solutions". 
                                # Stopping at one is simpler for visualization first.
            else:
                yield "CONFLICT", list(self.board), f"Conflict with ({conf_r}, {conf_c})!", (row, col, conf_r, conf_c)

            # Backtrack
            yield "BACKTRACKING", list(self.board), f"Backtracking from ({row}, {col})...", (row, col)
            self.board[row] = -1  # Remove queen

        return False
