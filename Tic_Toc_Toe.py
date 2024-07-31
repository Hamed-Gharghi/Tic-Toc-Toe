"""
Tic-Tac-Toe Game with PyQt5

Author: Hamed Gharghi
Date: 2024-07-31

Description:
This is a simple Tic-Tac-Toe game implemented using PyQt5. The game features a dark theme with neon accents.
It includes a 3x3 grid of buttons for the game board, a status label to indicate the current player's turn,
and a reset button to restart the game. The game logic handles player moves, checks for a winner or draw,
and updates the UI accordingly.
"""

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(400, 450))
        Dialog.setMaximumSize(QtCore.QSize(400, 450))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        Dialog.setFont(font)

        # Set the main dialog background color to Dark Slate Gray
        Dialog.setStyleSheet("background-color: #2F4F4F;")  # Dark Slate Gray

        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 50, 380, 350))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridLayoutWidget.sizePolicy().hasHeightForWidth())
        self.gridLayoutWidget.setSizePolicy(sizePolicy)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        # Initialize buttons with Dark Gray background and Neon Green text
        self.buttons = [[None] * 3 for _ in range(3)]
        Dialog.setWindowIcon(QtGui.QIcon('icon.png'))

        button_positions = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]

        button_styles = "background-color: #333333; color: #39FF14;"  # Dark Gray with Neon Green text

        for index, pos in enumerate(button_positions):
            button = QtWidgets.QPushButton(self.gridLayoutWidget)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
            button.setSizePolicy(sizePolicy)
            button.setText("")
            button.setStyleSheet(button_styles)  # Apply button styles
            button.setObjectName(f"pushButton_{index+1}")
            self.gridLayout.addWidget(button, *pos)
            button.clicked.connect(lambda checked, b=button: self.buttonClicked(b))
            self.buttons[pos[0]][pos[1]] = button

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(130, 10, 150, 30))
        self.label.setObjectName("label")
        self.label.setStyleSheet("color: #39FF14;")  # Neon Green text color
        self.label.setAlignment(QtCore.Qt.AlignCenter)  # Center align the text

        self.pushButton_10 = QtWidgets.QPushButton(Dialog)
        self.pushButton_10.setGeometry(QtCore.QRect(140, 400, 120, 30))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_10.setStyleSheet("background-color: #333333; color: #39FF14;")  # Dark Gray with Neon Green text
        self.pushButton_10.clicked.connect(self.resetGame)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.resetGame()  # Initialize the game

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Tic-Toc-Toe"))
        self.label.setText(_translate("Dialog", "Player X’s turn"))
        self.pushButton_10.setText(_translate("Dialog", "Reset"))

    def __init__(self):
        self.current_player = "X"
        self.board = [[None] * 3 for _ in range(3)]
        self.buttons = []
        super().__init__()

    def buttonClicked(self, button):
        if button.text() == "" and not self.checkForWinner() and not self.checkForDraw():
            button.setText(self.current_player)
            button.setStyleSheet(f"background-color: #333333; color: #39FF14;")  # Dark Gray with Neon Green text
            pos = self.getButtonPosition(button)
            self.board[pos[0]][pos[1]] = self.current_player
            if self.checkForWinner():
                self.updateStatus(f"Player {self.current_player} wins!", winner=True)
            elif self.checkForDraw():
                self.updateStatus("It's a draw!", draw=True)
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.updateStatus(f"Player {self.current_player}’s turn")

    def getButtonPosition(self, button):
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j] == button:
                    return (i, j)
        return None

    def checkForWinner(self):
        for i in range(3):
            # Check rows
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != None:
                return True
            # Check columns
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != None:
                return True
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != None:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != None:
            return True
        return False

    def checkForDraw(self):
        for row in self.board:
            if None in row:
                return False
        return not self.checkForWinner()

    def resetGame(self):
        for row in self.buttons:
            for button in row:
                button.setText("")
                button.setStyleSheet("background-color: #333333; color: #39FF14;")  # Reset to Dark Gray with Neon Green text
        self.current_player = "X"
        self.board = [[None] * 3 for _ in range(3)]
        self.updateStatus("Player X’s turn")
        self.enableButtons()

    def updateStatus(self, message, winner=False, draw=False):
        self.label.setText(message)
        if winner:
            self.label.setStyleSheet("color: #FF6EC7;")  # Neon Pink for winner
            self.disableButtons()
            for row in self.buttons:
                for button in row:
                    if button.text() != "":
                        button.setStyleSheet("background-color: #333333; color: #8B8B8B;")  # Change to Sky Gray
        elif draw:
            self.label.setStyleSheet("color: #1F51FF;")  # Neon Blue for draw
            self.disableButtons()
            for row in self.buttons:
                for button in row:
                    if button.text() != "":
                        button.setStyleSheet("background-color: #333333; color: #8B8B8B;")  # Change to Sky Gray
        else:
            self.label.setStyleSheet("color: #39FF14;")  # Neon Green for ongoing play

    def disableButtons(self):
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)

    def enableButtons(self):
        for row in self.buttons:
            for button in row:
                button.setEnabled(True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    app.setStyle("Fusion")
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
