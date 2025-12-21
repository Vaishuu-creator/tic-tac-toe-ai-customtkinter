import customtkinter as ctk
import random

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.theme = "dark"
        self.mode = None
        self.difficulty = None
        self.current_player = "X"
        self.board = [None] * 9
        self.buttons = []

        self.create_menu()

    def create_menu(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root)
        frame.pack(padx=20, pady=20)

        title = ctk.CTkLabel(frame, text="Tic Tac Toe", font=("Arial", 32))
        title.pack(pady=10)

        theme_label = ctk.CTkLabel(frame, text="Select Theme:", font=("Arial", 16))
        theme_label.pack()

        theme_switch = ctk.CTkSegmentedButton(frame, values=["light", "dark"], command=self.set_theme)
        theme_switch.set(self.theme)
        theme_switch.pack(pady=5)

        mode_label = ctk.CTkLabel(frame, text="Play Mode:", font=("Arial", 16))
        mode_label.pack(pady=(20, 5))

        ai_btn = ctk.CTkButton(frame, text="Play vs AI", command=self.select_difficulty)
        ai_btn.pack(pady=5)

        pvp_btn = ctk.CTkButton(frame, text="Two Players", command=lambda: self.start_game("pvp"))
        pvp_btn.pack(pady=5)

    def set_theme(self, theme):
        self.theme = theme
        ctk.set_appearance_mode(theme)

    def select_difficulty(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root)
        frame.pack(padx=20, pady=20)

        label = ctk.CTkLabel(frame, text="Select Difficulty", font=("Arial", 24))
        label.pack(pady=10)

        for level in ["Easy", "Medium", "Hard"]:
            btn = ctk.CTkButton(frame, text=level, command=lambda l=level: self.start_game("ai", l.lower()))
            btn.pack(pady=5)

    def start_game(self, mode, difficulty=None):
        self.mode = mode
        self.difficulty = difficulty
        self.current_player = "X"
        self.board = [None] * 9
        self.clear_window()
        self.buttons = []

        game_frame = ctk.CTkFrame(self.root)
        game_frame.pack(pady=10)

        self.status_label = ctk.CTkLabel(game_frame, text="Player X's turn", font=("Arial", 18))
        self.status_label.grid(row=0, column=0, columnspan=3, pady=10)

        for i in range(9):
            btn = ctk.CTkButton(game_frame, text="", width=100, height=100, font=("Arial", 32),
                                 command=lambda i=i: self.handle_click(i))
            btn.grid(row=(i // 3) + 1, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        restart_btn = ctk.CTkButton(self.root, text="Back to Menu", command=self.create_menu)
        restart_btn.pack(pady=(10, 0))

    def handle_click(self, index):
        if self.board[index] or self.check_winner("X") or self.check_winner("O"):
            return

        if self.mode == "ai" and self.current_player == "O":
            return

        self.make_move(index)
        if self.mode == "ai" and not self.check_winner("X"):
            self.root.after(300, self.ai_move)

    def make_move(self, index):
        if self.board[index] is None:
            self.board[index] = self.current_player
            self.buttons[index].configure(text=self.current_player)

            winner = self.check_winner(self.current_player)
            if winner:
                self.highlight_winner(winner)
                self.status_label.configure(text=f"Player {self.current_player} wins!")
            elif None not in self.board:
                self.status_label.configure(text="It's a draw!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_label.configure(text=f"Player {self.current_player}'s turn")

    def ai_move(self):
        if self.difficulty == "easy":
            empty = [i for i, v in enumerate(self.board) if v is None]
            index = random.choice(empty)
        elif self.difficulty == "medium":
            index = self.medium_ai()
        else:
            _, index = self.minimax(self.board, True)

        self.make_move(index)

    def medium_ai(self):
        # Block win if possible, else random
        for i in range(9):
            if self.board[i] is None:
                self.board[i] = "O"
                if self.check_winner("O"):
                    self.board[i] = None
                    return i
                self.board[i] = None

        for i in range(9):
            if self.board[i] is None:
                self.board[i] = "X"
                if self.check_winner("X"):
                    self.board[i] = None
                    return i
                self.board[i] = None

        return random.choice([i for i, v in enumerate(self.board) if v is None])

    def minimax(self, board, is_max):
        winner = self.check_winner("O")
        if winner:
            return (1, None)
        winner = self.check_winner("X")
        if winner:
            return (-1, None)
        if None not in board:
            return (0, None)

        if is_max:
            best = (-float("inf"), None)
            for i in range(9):
                if board[i] is None:
                    board[i] = "O"
                    score = self.minimax(board, False)[0]
                    board[i] = None
                    best = max(best, (score, i))
            return best
        else:
            best = (float("inf"), None)
            for i in range(9):
                if board[i] is None:
                    board[i] = "X"
                    score = self.minimax(board, True)[0]
                    board[i] = None
                    best = min(best, (score, i))
            return best

    def check_winner(self, player):
        wins = [(0,1,2), (3,4,5), (6,7,8),
                (0,3,6), (1,4,7), (2,5,8),
                (0,4,8), (2,4,6)]
        for a,b,c in wins:
            if self.board[a] == self.board[b] == self.board[c] == player:
                return (a,b,c)
        return None

    def highlight_winner(self, win_indices):
        for i in win_indices:
            self.buttons[i].configure(fg_color=("green", "green"))

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # default theme
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = TicTacToeApp(root)
    root.mainloop()


