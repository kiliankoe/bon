import matplotlib.pyplot as plt

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
