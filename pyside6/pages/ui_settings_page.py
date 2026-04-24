from qt_core import *
from .tabs_dash.data_tab import DataTab
from .analysis_tab import AnalysisTab
import pandas as pd

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

# --- Atributos ---
        # --- Layout Principal ---
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # --- Cabeçalho ---
        self.header_container = QVBoxLayout()
        self.header_container.setAlignment(Qt.AlignCenter)
        self.title = QLabel("Dashboard de Prospecção")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; color: #e0eee0; margin-bottom: 10px;")

        self.upload_layout = QHBoxLayout()
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
        self.upload_btn.clicked.connect(self.handle_upload)

        self.hide_btn = QPushButton("Ocultar Dados")
        self.hide_btn.setCursor(Qt.PointingHandCursor)
        self.hide_btn.setStyleSheet(style_btn)
        self.hide_btn.clicked.connect(self.handle_hide)
        self.hide_btn.hide()   # só aparece depois do upload

        self.upload_layout.addWidget(self.upload_btn)
        self.upload_layout.addWidget(self.hide_btn)
        self.header_container.addWidget(self.title)
        self.header_container.addWidget(self.upload_msg)
        self.header_container.addLayout(self.upload_layout)

        self.main_layout.addLayout(self.header_container)

        # Criação das abas do dashboard
        self.tabs = QTabWidget()
        self.tabs.setContentsMargins(0, 0, 0, 0)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
            }

            /* Aba normal */
            QTabBar::tab {
                background: transparent;
                color: #88aa88;
                padding: 6px 12px;
                margin-right: 10px;
                border: none;
                font-size: 11px;
            }

            /* Hover */
            QTabBar::tab:hover {
                color: #cdeccd;
            }

            /* Aba selecionada */
            QTabBar::tab:selected {
                color: #e0eee0;
                border-bottom: 2px solid #3d7a55;
            }

            /* Remove aquele "offset" feio */
            QTabBar::tab:!selected {
            margin-top: 2px;
            }
        """)
        
    # --- Aba de Dados ---
        # Importando a classe DataTab
        self.tab_data = DataTab()
        self.tab_data.setStyleSheet("background-color: transparent;")

        self.tabs.addTab(self.tab_data, "Dados")

        self.tab_analysis = AnalysisTab()
        self.tab_analysis.setStyleSheet("background-color: transparent;")

        self.tabs.addTab(self.tab_analysis, "Análise")

        # Adiciona as abas ao layout principal
        self.main_layout.addWidget(self.tabs)

# --- Métodos ---
    # --- Manipulação do upload e exibição dos dados ---
    def handle_upload(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar CSV",
            "",
            "CSV Files (*.csv)"
        )

        if file_path:
            df = pd.read_csv(file_path)

            self.df = df

            # envia os dados para as abas
            self.tab_data.display_data(self.df)
            self.tab_data.display_scatter(self.df)
            self.tab_analysis.load_data(self.df)

            self.hide_btn.show()

    # --- Manipulação da ocultação dos dados ---
    def handle_hide(self):
        self.tab_data.hide_data()
        self.hide_btn.hide()
        
        
    