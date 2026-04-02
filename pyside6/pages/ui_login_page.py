from qt_core import *

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # Label (Olá...)
        self.label = QLabel("Olá...")
        self.label.setStyleSheet("font-size: 18px; color: hsl(145, 10%, 92%);")

        # Input
        self.input = QLineEdit()
        self.input.setPlaceholderText("Escreva o seu nome")
        self.input.setFixedWidth(250)
        self.input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border-radius: 8px;
                background-color: hsl(145, 20%, 14%);
                color: hsl(145, 10%, 92%);
                border: 1px solid hsl(145, 15%, 25%);
            }
            QLineEdit:focus {
                border: 1px solid hsl(145, 30%, 40%);
            }
        """)

        # Botão
        self.button = QPushButton("Alterar Texto")
        self.button.setFixedWidth(120)
        self.button.setCursor(Qt.PointingHandCursor)
        self.button.clicked.connect(self.update_text)
        self.button.setStyleSheet("""
            QPushButton {
                padding: 10px 16px;
                border-radius: 8px;
                background-color: hsl(145, 35%, 28%);
                color: hsl(145, 10%, 95%);
            }

            QPushButton:hover {
                background-color: hsl(145, 40%, 35%);
            }

            QPushButton:pressed {
                background-color: hsl(145, 45%, 22%);
            }
        """)

        # Layout horizontal (input + botão)
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.button)

        # Adiciona tudo
        main_layout.addWidget(self.label)
        main_layout.addLayout(input_layout)

    def update_text(self):
        nome = self.input.text()

        if nome:
            self.label.setText(f"Olá, {nome}")
        else:
            self.label.setText("Olá...")

        

       