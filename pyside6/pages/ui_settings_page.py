from qt_core import *
import pandas as pd

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        # --- Layout Principal ---
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # --- Cabeçalho ---
        self.header_container = QVBoxLayout()
        self.header_container.setAlignment(Qt.AlignCenter)
        self.title = QLabel("Dashboard de Prospecção")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; color: #e0eee0; margin-bottom: 10px;")

        self.upload_layout = QVBoxLayout()
        self.upload_layout.setAlignment(Qt.AlignCenter)
        self.upload_layout.setSpacing(15)

        self.upload_msg = QLabel("Faça upload do arquivo CSV com os dados de prospecção:")
        self.upload_msg.setStyleSheet("color: #e0eee0; margin-bottom: 10px;")

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.setCursor(Qt.PointingHandCursor)

        style_btn = """
            QPushButton { padding: 12px 24px; border-radius: 8px; background-color: #2e5a40; color: white; font-weight: bold; }
            QPushButton:hover { background-color: #3d7a55; }
        """
        self.upload_btn.setStyleSheet(style_btn)
        self.upload_btn.clicked.connect(self.upload_csv)

        self.upload_layout.addWidget(self.upload_msg)
        self.upload_layout.addWidget(self.upload_btn)
        self.header_container.addWidget(self.title)
        self.header_container.addLayout(self.upload_layout)

        # Conteúdo do Dashboard
        self.dash_layout = QHBoxLayout()

        self.table_layout = QVBoxLayout()
        self.table_layout.setSpacing(20)

        self.table = QTableWidget()
        self.table.hide()
        self.table.setStyleSheet("background-color: #1a2e24; color: #e0eee0; border-radius: 10px;")

        self.table_layout.addWidget(self.table)
        self.dash_layout.addLayout(self.table_layout)

        self.main_layout.addLayout(self.header_container)
        self.main_layout.addLayout(self.dash_layout)

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar CSV",
            "",
            "CSV Files (*.csv)"
        )

        if file_path:
            df = pd.read_csv(file_path)
            self.display_data(df)

    def display_data(self, df):
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])

        self.table.setHorizontalHeaderLabels(df.columns)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                value = str(df.iat[row, col])
                self.table.setItem(row, col, QTableWidgetItem(value))

        self.table.show()