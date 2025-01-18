from fastapi import APIRouter
from pydantic import BaseModel, Field
from printer import printer as p
from sudoku import Sudoku
import os
import random
import matplotlib.pyplot as plt

router = APIRouter()

class SudokuRequest(BaseModel):
    difficulty: float = Field(0.4, ge=0.0, le=1.0)

@router.post("/sudoku")
async def sudoku(data: SudokuRequest):
    """
    Print a sudoku puzzle with the given difficulty.
    """
    puzzle = Sudoku(3, seed=random.randint(0, 1000000)).difficulty(data.difficulty)
    if os.path.exists("sudoku.png"):
        os.remove("sudoku.png")
    render_sudoku(puzzle.board)
    p.image("sudoku.png")
    p.ln(2)
    p.cut()
    return {"message": "Printed sudoku", "difficulty": data.difficulty}

def render_sudoku(grid, filename='sudoku.png'):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_aspect('equal')

    for i in range(10):
        # Thicker lines for 3x3 blocks
        linewidth = 4 if i % 3 == 0 else 2
        ax.plot([0, 9], [i, i], color='black', linewidth=linewidth)
        ax.plot([i, i], [0, 9], color='black', linewidth=linewidth)

    for r in range(9):
        for c in range(9):
            if grid[r][c] not in [0, None]:
                ax.text(c + 0.5,
                        8.5 - r,
                        str(grid[r][c]),
                        fontsize=26,
                        fontweight='bold',
                        ha='center',
                        va='center')

    ax.axis('off')
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', dpi=100, pad_inches=0)
    plt.close()
