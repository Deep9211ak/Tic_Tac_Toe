from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Line

class GameBoard(GridLayout):
    def __init__(self, **kwargs):
        super(GameBoard, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.padding = 10
        self.spacing = 10
        self.buttons = [[Button(font_size=40) for _ in range(3)] for _ in range(3)]

        for row in self.buttons:
            for button in row:
                button.bind(on_release=self.on_button_press)
                self.add_widget(button)

    def on_button_press(self, button):
        app = App.get_running_app()
        row, col = [(r, c) for r, row in enumerate(self.buttons) for c, btn in enumerate(row) if btn == button][0]

        if app.board[row][col] == '' and button.text == '':
            app.board[row][col] = app.current_player
            button.text = app.current_player

            if app.check_winner(app.current_player):
                app.highlight_winner(app.current_player)
                app.show_winner_popup(f"Player {app.current_player} wins!")
            elif all(cell != '' for row in app.board for cell in row):
                app.show_winner_popup("It's a draw!")
            else:
                app.switch_player()

class TicTacToeApp(App):
    def build(self):
        self.title = "Tic Tac Toe"
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        Window.clearcolor = (1, 1, 1, 1)  # Set background color to white

        # Create the main layout
        layout = BoxLayout(orientation='vertical', padding=0, spacing=20)

        # Create the game board layout
        self.game_board = GameBoard()
        layout.add_widget(self.game_board)

        # Create the status label
        self.status_label = Label(text="Player X's turn", font_size=24, size_hint=(1, 0.2))
        layout.add_widget(self.status_label)

        return layout

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.status_label.text = f"Player {self.current_player}'s turn"

    def check_winner(self, player):
        # Check rows, columns, and diagonals
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def highlight_winner(self, player):
        with self.game_board.canvas:
            Color(0, 1, 0, 0.5)  # Green color with transparency
            for row in range(3):
                if all(self.board[row][col] == player for col in range(3)):
                    self.draw_line(row, 0, row, 2)
            for col in range(3):
                if all(self.board[row][col] == player for row in range(3)):
                    self.draw_line(0, col, 2, col)
            if all(self.board[i][i] == player for i in range(3)):
                self.draw_line(0, 0, 2, 2)
            if all(self.board[i][2 - i] == player for i in range(3)):
                self.draw_line(0, 2, 2, 0)

    def draw_line(self, start_row, start_col, end_row, end_col):
        start_button = self.game_board.buttons[start_row][start_col]
        end_button = self.game_board.buttons[end_row][end_col]
        with self.game_board.canvas:
            Line(points=[
                start_button.center_x, start_button.center_y,
                end_button.center_x, end_button.center_y
            ], width=2)

    def show_winner_popup(self, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        button = Button(text='Play Again')
        button.bind(on_release=self.reset_game)

        content.add_widget(button)
        popup = Popup(title='Game Over', content=content, size_hint=(0.5, 0.5))
        popup.open()

    def reset_game(self, instance):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        for row in self.game_board.buttons:
            for button in row:
                button.text = ''
        self.status_label.text = "Player X's turn"
        self.game_board.canvas.clear()

if __name__ == '__main__':
    TicTacToeApp().run()
