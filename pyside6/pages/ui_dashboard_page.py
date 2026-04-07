from qt_core import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        
        # --- Configuração dos Gráficos --- Uso de Figure para criar os gráficos e FigureCanvas para integrá-los ao PySide6
        # Gráfico 1: Barras
        self.fig_bar = Figure(facecolor="#0f1f17") # Define a cor de fundo do gráfico para combinar com o tema escuro da interface
        self.canvas_bar = FigureCanvas(self.fig_bar)
        
        # Gráfico 2: Scatter (Bolinhas)
        self.fig_scatter = Figure(facecolor="#0f1f17")
        self.canvas_scatter = FigureCanvas(self.fig_scatter)
        
        self.canvas_bar.hide()
        self.canvas_scatter.hide()

        # --- Layout Principal ---
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # --- Cabeçalho ---
        self.header_container = QVBoxLayout()
        self.header_container.setAlignment(Qt.AlignCenter)

        self.title = QLabel("Dashboard de Prospecção")
        self.title.setStyleSheet("font-size: 26px; font-weight: bold; color: #e0eee0; margin-bottom: 10px;") 
        
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(15)
        
        style_btn = """
            QPushButton { padding: 12px 24px; border-radius: 8px; background-color: #2e5a40; color: white; font-weight: bold; }
            QPushButton:hover { background-color: #3d7a55; }
        """
        self.btn_gen = QPushButton("Gerar Dados")
        self.btn_gen.setStyleSheet(style_btn)
        self.btn_gen.clicked.connect(self.generate_data)
        self.btn_gen.setCursor(Qt.PointingHandCursor)

        self.btn_hide = QPushButton("Ocultar Dados")
        self.btn_hide.setStyleSheet(style_btn)
        self.btn_hide.clicked.connect(self.hide_data)
        self.btn_hide.setCursor(Qt.PointingHandCursor)

        self.buttons_layout.addWidget(self.btn_gen)
        self.buttons_layout.addWidget(self.btn_hide)
        self.header_container.addWidget(self.title)
        self.header_container.addLayout(self.buttons_layout)

        # --- Corpo do Dashboard (Layout Horizontal) ---
        self.content_layout = QHBoxLayout()

        # Coluna da Esquerda: Tabela + Scatter Plot
        self.left_column = QVBoxLayout()
        self.left_column.setSpacing(20)

        self.table = QTableWidget()
        self.table.hide()
        self.table.setStyleSheet("background-color: #1a2e24; color: #e0eee0; border-radius: 10px;")
        
        self.left_column.addWidget(self.table, 2) # Peso 2 para a tabela
        self.left_column.addWidget(self.canvas_scatter, 3) # Peso 3 para o scatter

        # Coluna da Direita: Gráfico de Barras
        self.content_layout.addLayout(self.left_column, 1) 
        self.content_layout.addWidget(self.canvas_bar, 1)   
        
        self.main_layout.addLayout(self.header_container)
        self.main_layout.addLayout(self.content_layout)
        self.main_layout.addStretch() 

    def generate_data(self):
        dados = [("Mol1", "Bioativo"), ("Mol2", "Não Bioativo"), ("Mol3", "Bioativo"), ("Mol4", "Não Bioativo"), ("Mol5", "Bioativo")]
        
        # 1. Atualizar Tabela
        self.table.setRowCount(len(dados)) # Seta o número de linhas da tabela para o número de dados gerados
        self.table.setColumnCount(2) # Seta o número de colunas da tabela para 2 (Molécula e Classificação)
        self.table.setHorizontalHeaderLabels(["Molécula", "Classificação"])
        for row, (mol, classe) in enumerate(dados): 
            self.table.setItem(row, 0, QTableWidgetItem(mol))
            self.table.setItem(row, 1, QTableWidgetItem(classe))
        self.table.show()

        # 2. Gráfico de Barras
        self.fig_bar.clear() # Limpa o gráfico anterior para evitar sobreposição de dados
        ax_bar = self.fig_bar.add_subplot(111) # Gráfico único (1 linha, 1 coluna, posição 1)
        ax_bar.set_facecolor("#0f1f17") # Define a cor de fundo do gráfico para combinar com o tema escuro da interface

        # Soma o número de bioativos e não bioativos
        bio = sum(1 for _, c in dados if c == "Bioativo") 
        nbio = sum(1 for _, c in dados if c == "Não Bioativo") 
        
        # Define o eixo x com as categorias e o eixo y com os valores
        ax_bar.bar(["Bioativos", "Não Bioativos"], [bio, nbio], color=["#3fa34d", "#2b7a2b"], width=0.6)
        self.style_axes(ax_bar)
        self.canvas_bar.draw()
        self.canvas_bar.show()

        # 3. Gráfico de Bolinhas 
        self.fig_scatter.clear()
        ax_scatter = self.fig_scatter.add_subplot(111)
        ax_scatter.set_facecolor("#0f1f17")
        
        x = [random.uniform(0, 10) for _ in dados]
        y = [random.uniform(0, 10) for _ in dados]
        colors = ["#3fa34d" if c == "Bioativo" else "#2b7a2b" for _, c in dados]
        
        # Define eixos, cores, tamanhos e bordas das bolinhas, além de uma leve transparência para um visual mais moderno
        ax_scatter.scatter(x, y, c=colors, s=150, edgecolors="white", alpha=0.8)

        self.style_axes(ax_scatter)
        self.canvas_scatter.draw()
        self.canvas_scatter.show()

    def style_axes(self, ax): 
        """Padroniza o visual dos eixos"""
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#88aa88")
        ax.spines["bottom"].set_color("#88aa88")
        ax.tick_params(colors="#cdeccd", labelsize=9)

    def hide_data(self):
        self.table.hide()
        self.canvas_bar.hide()
        self.canvas_scatter.hide()