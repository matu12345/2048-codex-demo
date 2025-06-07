import tkinter as tk
from game import Game
from ai import SimpleAI

class GameUI:
    def __init__(self, root):
        self.root = root
        self.game = Game()
        self.tip_history = []
        self.load_tips()
        self.ai = SimpleAI(self.tip_history)
        self.ai_mode = False
        self.auto_job = None

        self.root.title("2048 with AI")
        self.cells = []
        for r in range(4):
            row = []
            for c in range(4):
                lbl = tk.Label(root, text='', width=4, height=2,
                               font=('Helvetica', 24), borderwidth=2, relief='solid')
                lbl.grid(row=r, column=c, padx=5, pady=5)
                row.append(lbl)
            self.cells.append(row)

        self.score_label = tk.Label(root, text='Score: 0')
        self.score_label.grid(row=4, column=0, columnspan=4)

        self.comment_label = tk.Label(root, text='', wraplength=300, justify='left')
        self.comment_label.grid(row=5, column=0, columnspan=4)
        if self.tip_history:
            preview = ' | '.join(self.tip_history[-3:])
            self.comment_label.config(text='最近の学習: {}'.format(preview))

        self.toggle_btn = tk.Button(root, text='Enable AI', command=self.toggle_ai)
        self.toggle_btn.grid(row=6, column=0, columnspan=1)
        self.auto_btn = tk.Button(root, text='Auto Play', command=self.start_auto)
        self.auto_btn.grid(row=6, column=1, columnspan=1)
        self.stop_btn = tk.Button(root, text='Stop AI', command=self.stop_auto)
        self.stop_btn.grid(row=6, column=2, columnspan=1)

        root.bind('<Key>', self.on_key)
        self.update_ui()

    def load_tips(self):
        try:
            with open('tips.txt', 'r', encoding='utf-8') as f:
                self.tip_history = [line.strip() for line in f if line.strip()]
        except IOError:
            self.tip_history = []

    def save_tip(self, text):
        if not text:
            return
        self.tip_history.append(text)
        with open('tips.txt', 'a', encoding='utf-8') as f:
            f.write(text + '\n')

    def generate_tip(self):
        corners = {
            'top-left': (0, 0),
            'top-right': (0, 3),
            'bottom-left': (3, 0),
            'bottom-right': (3, 3),
        }
        names_jp = {
            'top-left': '左上',
            'top-right': '右上',
            'bottom-left': '左下',
            'bottom-right': '右下',
        }
        max_tile = 0
        best_corner = None
        for name, (r, c) in corners.items():
            tile = self.game.board[r][c]
            if tile > max_tile:
                max_tile = tile
                best_corner = name
        if best_corner:
            tip = 'corner:{}'.format(best_corner)
            self.save_tip(tip)
            self.ai.update_preference(self.tip_history)
            return '今回学んだこと: 大きなタイルは{}に集まりやすいです。'.format(names_jp[best_corner])
        return None

    def on_key(self, event):
        if self.ai_mode:
            return
        direction_map = {'Up': 'Up', 'Down': 'Down', 'Left': 'Left', 'Right': 'Right'}
        if event.keysym in direction_map:
            moved, _ = self.game.move(direction_map[event.keysym])
            if moved:
                self.game.add_random_tile()
                self.update_ui()
                self.check_game_over()

    def toggle_ai(self):
        self.ai_mode = not self.ai_mode
        if self.ai_mode:
            self.toggle_btn.config(text='Disable AI')
        else:
            self.toggle_btn.config(text='Enable AI')
            self.stop_auto()
        self.comment_label.config(text='')

    def start_auto(self):
        if not self.ai_mode:
            self.comment_label.config(text='Enable AI mode first.')
            return
        if self.auto_job is None:
            self.auto_step()

    def auto_step(self):
        if not self.ai_mode:
            return
        self.ai_move()
        if self.game.can_move():
            self.auto_job = self.root.after(300, self.auto_step)
        else:
            self.auto_job = None

    def stop_auto(self):
        if self.auto_job:
            self.root.after_cancel(self.auto_job)
            self.auto_job = None
            self.comment_label.config(text='Auto play stopped.')

    def ai_move(self):
        direction, explanation = self.ai.choose_move(self.game)
        self.comment_label.config(text=explanation)
        if direction is None:
            return
        moved, _ = self.game.move(direction)
        if moved:
            self.game.add_random_tile()
            self.update_ui()
            self.check_game_over()

    def update_ui(self):
        for r in range(4):
            for c in range(4):
                value = self.game.board[r][c]
                self.cells[r][c]['text'] = str(value) if value else ''
        self.score_label.config(text='Score: {}'.format(self.game.score))

    def check_game_over(self):
        if not self.game.can_move():
            self.stop_auto()
            msg = self.generate_tip()
            if msg:
                self.comment_label.config(text='Game Over! ' + msg)
            else:
                self.comment_label.config(text='Game Over!')

if __name__ == '__main__':
    root = tk.Tk()
    ui = GameUI(root)
    root.mainloop()
