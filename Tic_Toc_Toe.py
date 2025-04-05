"""
Tic-Tac-Toe Game with PyQt5

Authors: Hamed Gharghi , RezaGooner
Date: 2025-04-1
Modified: 2024-07-31

Features:
- Larger X and O symbols with distinct colors (Pink for X, Blue for O)
- Dark theme with neon accents
- Keyboard navigation support
- Winner/draw alerts with matching colors
"""

from PyQt5 import QtCore, QtGui, QtWidgets

class TicTacToeGame(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.current_player = "X"
        self.board = [[None] * 3 for _ in range(3)]
        self.current_row = 0
        self.current_col = 0
        
    def setup_ui(self):
        # Main window configuration
        self.setObjectName("TicTacToe")
        self.resize(450, 500)
        self.setMinimumSize(450, 500)
        self.setMaximumSize(450, 500)
        
        # Set main window stylesheet
        self.setStyleSheet("""
            QDialog {
                background-color: #2F4F4F;
            }
            QLabel {
                color: #39FF14;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton#resetButton {
                background-color: #333333;
                color: #39FF14;
                font-size: 14px;
                border: 1px solid #39FF14;
                padding: 5px;
            }
            QPushButton#resetButton:hover {
                background-color: #444444;
            }
        """)

        # Create game board buttons
        self.buttons = []
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(10)
        
        for row in range(3):
            button_row = []
            for col in range(3):
                button = QtWidgets.QPushButton()
                button.setMinimumSize(100, 100)
                button.setProperty("x-player", False)
                button.setProperty("o-player", False)
                
                # Set button styles with distinct colors for X and O
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #333333;
                        color: #39FF14;
                        font-size: 48px;
                        font-weight: bold;
                        border: 2px solid #39FF14;
                    }
                    QPushButton[x-player="true"] {
                        color: #FF1493;  /* Pink for X */
                        border-color: #FF1493;
                    }
                    QPushButton[o-player="true"] {
                        color: #1E90FF;  /* Blue for O */
                        border-color: #1E90FF;
                    }
                    QPushButton:disabled {
                        background-color: #333333;
                        color: #8B8B8B;
                    }
                """)
                
                button.clicked.connect(lambda _, r=row, c=col: self.make_move(r, c))
                button.setFocusPolicy(QtCore.Qt.StrongFocus)
                self.gridLayout.addWidget(button, row, col)
                button_row.append(button)
            self.buttons.append(button_row)

        # Status label
        self.status_label = QtWidgets.QLabel("Player X's turn")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)

        # Reset button
        self.reset_button = QtWidgets.QPushButton("Reset Game")
        self.reset_button.setObjectName("resetButton")
        self.reset_button.clicked.connect(self.reset_game)

        # Main layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addLayout(self.gridLayout)
        layout.addWidget(self.reset_button)
        self.setLayout(layout)

        # Set initial focus
        self.buttons[0][0].setFocus()

    def make_move(self, row, col):
        button = self.buttons[row][col]
        
        if button.text() == "" and not self.check_winner() and not self.check_draw():
            # Apply appropriate color based on current player
            if self.current_player == "X":
                button.setProperty("x-player", True)
                button.setProperty("o-player", False)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #333333;
                        color: #FF1493;
                        font-size: 48px;
                        font-weight: bold;
                        border: 2px solid #FF1493;
                    }
                """)
            else:
                button.setProperty("o-player", True)
                button.setProperty("x-player", False)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #333333;
                        color: #1E90FF;
                        font-size: 48px;
                        font-weight: bold;
                        border: 2px solid #1E90FF;
                    }
                """)
                
            button.setText(self.current_player)
            self.board[row][col] = self.current_player

            if self.check_winner():
                self.show_game_result(f"Player {self.current_player} wins!")
                self.status_label.setText(f"Player {self.current_player} wins!")
                # Set color matching the winner
                if self.current_player == "X":
                    self.status_label.setStyleSheet("color: #FF1493; font-size: 18px;")
                else:
                    self.status_label.setStyleSheet("color: #1E90FF; font-size: 18px;")
                self.disable_buttons()
            elif self.check_draw():
                self.show_game_result("It's a draw!")
                self.status_label.setText("It's a draw!")
                self.status_label.setStyleSheet("color: #39FF14; font-size: 18px;")
                self.disable_buttons()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_label.setText(f"Player {self.current_player}'s turn")
                self.status_label.setStyleSheet("color: #39FF14; font-size: 18px;")

    def show_game_result(self, message):
        # Create and show result alert
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Game Over")
        msg.setText(message)
        
        # Set alert color based on result
        if "X wins" in message:
            msg.setStyleSheet("QLabel { color: #FF1493; font-weight: bold; }")
        elif "O wins" in message:
            msg.setStyleSheet("QLabel { color: #1E90FF; font-weight: bold; }")
        else:  # Draw
            msg.setStyleSheet("QLabel { color: #39FF14; font-weight: bold; }")
        
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def check_winner(self):
        # Check rows for winner
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] is not None:
                return True
        
        # Check columns for winner
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] is not None:
                return True
        
        # Check diagonals for winner
        if self.board[0][0] == self.board[1][1] == self.board[2][2] is not None:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] is not None:
            return True
        
        return False

    def check_draw(self):
        # Check if all cells are filled
        for row in self.board:
            if None in row:
                return False
        return True

    def reset_game(self):
        # Reset all game elements
        for row in range(3):
            for col in range(3):
                button = self.buttons[row][col]
                button.setText("")
                button.setProperty("x-player", False)
                button.setProperty("o-player", False)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #333333;
                        color: #39FF14;
                        font-size: 48px;
                        font-weight: bold;
                        border: 2px solid #39FF14;
                    }
                """)
                button.setEnabled(True)
                self.board[row][col] = None
        
        # Reset game state
        self.current_player = "X"
        self.status_label.setText("Player X's turn")
        self.status_label.setStyleSheet("color: #39FF14; font-size: 18px;")
        self.current_row = 0
        self.current_col = 0
        self.buttons[0][0].setFocus()

    def disable_buttons(self):
        # Disable all buttons after game ends
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)

    def keyPressEvent(self, event):
        # Handle keyboard navigation
        key = event.key()
        
        if key == QtCore.Qt.Key_Left:
            self.current_col = (self.current_col - 1) % 3
        elif key == QtCore.Qt.Key_Right:
            self.current_col = (self.current_col + 1) % 3
        elif key == QtCore.Qt.Key_Up:
            self.current_row = (self.current_row - 1) % 3
        elif key == QtCore.Qt.Key_Down:
            self.current_row = (self.current_row + 1) % 3
        elif key in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Space):
            if self.buttons[self.current_row][self.current_col].text() == "":
                self.make_move(self.current_row, self.current_col)
            return
        else:
            super().keyPressEvent(event)
            return
            
        self.buttons[self.current_row][self.current_col].setFocus()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    game = TicTacToeGame()
    game.setWindowTitle("Tic-Tac-Toe")
    game.show()
    sys.exit(app.exec_())
