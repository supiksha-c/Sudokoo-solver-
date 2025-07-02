import tkinter as tk
from tkinter import messagebox

# --- Color Constants ---
SKY_BLUE = "#87CEEB"
BUTTON_BLUE = "#003366"
BUTTON_TEXT_COLOR = "white"
TEXT_COLOR = "black"
HIGHLIGHT_BG = "#fffacd"
ERROR_BG = "#ff6666"

def valid(board, num, pos):
    for i in range(9):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False

def show_rules_page(username):
    main_window.destroy()
    rules_window = tk.Tk()
    rules_window.title("Sudoku Rules")
    rules_window.configure(bg=SKY_BLUE)

    tk.Label(rules_window, text="What is Sudoku?", font=('Arial', 18, 'bold'),
             bg=SKY_BLUE, fg=TEXT_COLOR).pack(pady=10)

    what_is = ("Sudoku is a logic-based number placement puzzle. "
               "The objective is to fill a 9×9 grid with digits so that each column, "
               "each row, and each of the nine 3×3 subgrids contains all of the digits from 1 to 9.")
    tk.Label(rules_window, text=what_is, wraplength=500, font=('Arial', 12), justify='left',
             bg=SKY_BLUE, fg=TEXT_COLOR).pack(padx=20, pady=10)

    tk.Label(rules_window, text="Rules:", font=('Arial', 16, 'bold'),
             bg=SKY_BLUE, fg=TEXT_COLOR).pack(pady=5)

    rules = [
        "1. Sudoku grid is 9×9.",
        "2. Each row must have digits 1–9 with no repeats.",
        "3. Each column must have digits 1–9 with no repeats.",
        "4. Each 3×3 box must have digits 1–9 with no repeats.",
        "5. Use logic to solve, no guessing!",
        "6. You cannot place the same number in the same row, column, or 3×3 box."
    ]
    for rule in rules:
        tk.Label(rules_window, text=rule, font=('Arial', 12), anchor='w',
                 bg=SKY_BLUE, fg=TEXT_COLOR).pack(padx=30, anchor='w')

    def go_to_game():
        rules_window.destroy()
        start_sudoku_window(username)

    tk.Button(rules_window, text="Continue to Game", command=go_to_game,
              font=('Arial', 14), bg=BUTTON_BLUE, fg=BUTTON_TEXT_COLOR).pack(pady=20)

    rules_window.mainloop()

def start_sudoku_window(username):
    sudoku_window = tk.Tk()
    sudoku_window.title("Sudoku Solver")
    sudoku_window.configure(bg=SKY_BLUE)

    tk.Label(sudoku_window, text="Welcome, {}!".format(username), font=('Arial', 18, 'bold'),
             bg=SKY_BLUE, fg=TEXT_COLOR).grid(row=0, column=0, columnspan=9, pady=10)

    entries = []
    user_filled_positions = set()

    error_label = tk.Label(sudoku_window, text="", font=('Arial', 12),
                           bg=SKY_BLUE, fg="red")
    error_label.grid(row=10, column=0, columnspan=9)

    def is_duplicate_in_row_or_col(val, row, col):
        for j in range(9):
            if j != col and entries[row][j].get() == val:
                return True
        for i in range(9):
            if i != row and entries[i][col].get() == val:
                return True
        return False

    for i in range(9):
        row_entries = []
        for j in range(9):
            e = tk.Entry(sudoku_window, width=2, font=('Arial', 18), justify='center',
                         bg="white", fg=TEXT_COLOR, relief='ridge', borderwidth=2)

            def on_entry_change(event, entry=e, row=i, col=j):
                val = entry.get()
                if val in [str(x) for x in range(1, 10)]:
                    if is_duplicate_in_row_or_col(val, row, col):
                        entry.config(bg=ERROR_BG)
                        error_label.config(text="Invalid input at row {}, column {}: duplicate in row or column.".format(row+1, col+1))
                        sudoku_window.after(3000, lambda: error_label.config(text=""))
                    else:
                        entry.config(bg=HIGHLIGHT_BG)
                        error_label.config(text="")
                        user_filled_positions.add((row, col))
                else:
                    entry.config(bg="white")
                    error_label.config(text="")
                    if (row, col) in user_filled_positions:
                        user_filled_positions.remove((row, col))

            e.bind("<KeyRelease>", on_entry_change)
            e.grid(row=i+1, column=j, padx=2, pady=2)
            row_entries.append(e)
        entries.append(row_entries)

    def get_board():
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = entries[i][j].get()
                if val == '':
                    row.append(0)
                else:
                    try:
                        num = int(val)
                        if 0 <= num <= 9:
                            row.append(num)
                        else:
                            raise ValueError
                    except ValueError:
                        error_label.config(text="Invalid number at row {}, column {}".format(i+1, j+1))
                        return None
            board.append(row)
        return board

    def fill_solution(sol_board):
        for i in range(9):
            for j in range(9):
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, str(sol_board[i][j]))
                if (i, j) in user_filled_positions:
                    entries[i][j].config(bg=HIGHLIGHT_BG)
                else:
                    entries[i][j].config(bg="white")

    def solve_puzzle():
        board = get_board()
        if board:
            if solve(board):
                fill_solution(board)
                final_msg = tk.Label(sudoku_window,
                                     text="Here is your final output, {}!".format(username),
                                     font=('Arial', 16, 'bold'),
                                     fg=TEXT_COLOR, bg=SKY_BLUE)
                final_msg.grid(row=11, column=0, columnspan=9, pady=10)
            else:
                error_label.config(text="The Sudoku puzzle cannot be solved.")

    solve_button = tk.Button(sudoku_window, text="Solve", font=('Arial', 16, 'bold'), command=solve_puzzle,
                             bg=BUTTON_BLUE, fg=BUTTON_TEXT_COLOR, activebackground="#002244",
                             activeforeground=BUTTON_TEXT_COLOR, relief='raised', borderwidth=4, padx=10, pady=5)
    solve_button.grid(row=12, column=0, columnspan=9, pady=10)

    sudoku_window.mainloop()

# --- First Page ---
main_window = tk.Tk()
main_window.title("Sudoku Project")
main_window.configure(bg=SKY_BLUE)

tk.Label(main_window, text="Welcome to Sudoku Solver", font=('Arial', 16),
         bg=SKY_BLUE, fg=TEXT_COLOR).pack(pady=15)

tk.Label(main_window, text="Enter your name:", font=('Arial', 14),
         bg=SKY_BLUE, fg=TEXT_COLOR).pack(pady=5)

name_entry = tk.Entry(main_window, font=('Arial', 14), bg="white", fg=TEXT_COLOR, justify='center')
name_entry.pack(pady=5)

def on_start():
    username = name_entry.get().strip()
    if not username:
        messagebox.showerror("Input Error", "Please enter your name before starting.")
        return
    show_rules_page(username)

start_button = tk.Button(main_window, text="Start Sudoku", font=('Arial', 14), command=on_start,
                         bg=BUTTON_BLUE, fg=BUTTON_TEXT_COLOR, activebackground="#002244",
                         activeforeground=BUTTON_TEXT_COLOR)
start_button.pack(pady=15)

main_window.mainloop()
