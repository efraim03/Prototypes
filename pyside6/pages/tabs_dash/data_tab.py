from qt_core import *
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class DataTab(QWidget):
    def __init__(self):
        super().__init__()
    
    # --- Atributos ---
        # --- Conteúdo da Aba de Dados ---
        self.dash_layout = QHBoxLayout()
        self.setLayout(self.dash_layout)

    # --- Criação dos layouts ---
        self.table_layout = QVBoxLayout()
        self.table_layout.setSpacing(20)

        self.scatter_layout = QVBoxLayout()
        self.scatter_layout.setSpacing(20)

    # Criação da tabela para exibir os dados
        self.table = QTableWidget()
        self.table.hide()
        self.table.setStyleSheet("background-color: #1a2e24; color: #e0eee0; border-radius: 10px; font-size: 10px")
        self.table.verticalHeader().setVisible(False)   # esconde os números das linhas

        self.table_layout.addWidget(self.table)

    # Criação do gráfico de dispersão
        self.fig_scatter = Figure(facecolor="#0f1f17")
        self.canvas_scatter = FigureCanvas(self.fig_scatter)
        self.canvas_scatter.hide()

    # Ferramenta de navegação do gráfico (zoom, pan, home)
        self.toolbar = NavigationToolbar(self.canvas_scatter, self)
        self.toolbar.hide()
        self.toolbar.setStyleSheet("""
            QToolBar {
                background-color: #0f1f17;
                border: none;
            }
            QToolButton {
                background-color: transparent;
                color: #cdeccd;
                border: none;}
            QToolButton:hover {
                background-color: #2e5a40;
                color: #e0eee0;
                border-radius: 5px;}
            """)
        
    # Lógica para mostrar somente os 3 botões
        allowed = {"Home", "Pan", "Zoom"}

        for action in self.toolbar.actions():
            if action.text() not in allowed:
                action.setVisible(False)

        # Lógica para mudar o cursor ao passar sobre os botões
            widget = self.toolbar.widgetForAction(action)
            if widget:
                widget.setCursor(Qt.PointingHandCursor)

        self.scatter_layout.addWidget(self.toolbar)
        self.scatter_layout.addWidget(self.canvas_scatter)

        # Divide ao meio: tabela à esquerda, gráfico à direita
        self.dash_layout.addLayout(self.table_layout, 1)
        self.dash_layout.addLayout(self.scatter_layout, 1)

# --- Métodos ---  
    # --- Exibição dos dados na tabela ---
    def display_data(self, df): 

        # shape é uma tupla (linhas, colunas)
        self.table.setRowCount(df.shape[0])    # define o número de linhas da tabela com base no número de linhas do DataFrame
        self.table.setColumnCount(df.shape[1]) # define o número de colunas da tabela com base no número de colunas do DataFrame

        self.table.setHorizontalHeaderLabels(df.columns)

        # percorre todas as linhas e colunas e insere o valor na tabela
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                value = str(df.iat[row, col])
                self.table.setItem(row, col, QTableWidgetItem(value))

        self.table.show()

    # --- Exibição do gráfico de dispersão ---
    def display_scatter(self, df):
        
        self.fig_scatter.clear()
        ax = self.fig_scatter.add_subplot(111)   # um único gráfico
        ax.set_facecolor("#0f1f17")

        # --- Garantir que os dados são numéricos --- dados que não forem, serão marcados como NaN 
        df["molecular_weight"] = pd.to_numeric(df["molecular_weight"], errors="coerce")
        df["logP"] = pd.to_numeric(df["logP"], errors="coerce")

        # Remove valores inválidos - NaN (Not a Number)
        df = df.dropna(subset=["molecular_weight", "logP"])

        # --- Separação por bioatividade ---
        bioactive = df[df["bioactivity"] == 1]
        non_bioactive = df[df["bioactivity"] == 0]

        self.style_axes(ax)

        # Armazena dados em atributos para usar na interação do hover
        self.ax = ax
        self.bioactive = bioactive.reset_index(drop=True)
        self.non_bioactive = non_bioactive.reset_index(drop=True)

        # --- Plot ---
        self.scatter_bio = ax.scatter(
            self.bioactive["molecular_weight"],
            self.bioactive["logP"],
            label="Bioativo",
            alpha=0.7,
            s=150,
            edgecolors="white",
            c="blue"
        )

        self.scatter_non = ax.scatter(
            self.non_bioactive["molecular_weight"],
            self.non_bioactive["logP"],
            label="Não Bioativo",
            alpha=0.7,
            s=150,
            edgecolors="white",
            c="red"
        )

        # --- Labels ---
        ax.set_xlabel("Peso Molecular", color="#cdeccd")
        ax.set_ylabel("logP", color="#cdeccd")
        ax.set_title("Distribuição: logP vs Peso Molecular", color="#cdeccd")

        self.canvas_scatter.draw()
        self.canvas_scatter.show()
        self.toolbar.show()

        self.points_data = pd.concat([bioactive, non_bioactive])   # junta os dados para facilitar a busca no hover

        # Crio a caixa de exibição
        self.annot = ax.annotate(
            "",
            xy=(0, 0),   # posição base
            xytext=(10, 10),    # deslocamento da caixa em relação a posição
            textcoords="offset points",   # deslocamento em pixels
            bbox=dict(boxstyle="round", fc="#1a2e24", ec="white"),   # estilo da caixa
            color="white"
        )
        self.annot.set_visible(False)   # só irá para True quando houver um hover

        self.canvas_scatter.mpl_connect("motion_notify_event", self.hover) # toda vez que o mouse se mexer, verifico a função hover

    # --- Atualização do tooltip ---
    def update_annot(self, ind, data):   # recebe o índice e o dataset como parâmetros
        index = ind["ind"][0]   # atualiza o índice

        x = data.iloc[index]["molecular_weight"]
        y = data.iloc[index]["logP"]
        mol_id = data.iloc[index].get("molecule_id", index)

        self.annot.xy = (x, y)

        # --- limites do gráfico ---
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()

        # --- lógica de reposicionamento ---
        offset_x = 10
        offset_y = 10

        # 🔹 Se estiver muito à direita → joga tooltip pra esquerda
        if x > x_max * 0.8:
            offset_x = -80

        # 🔹 Se estiver muito no topo → joga tooltip pra baixo
        if y > y_max * 0.8:
            offset_y = -20

        self.annot.set_position((offset_x, offset_y))

        self.annot.set_text(f"ID: {mol_id}\nMW: {x:.2f}\nlogP: {y:.2f}")
        self.annot.set_visible(True)

    # --- Método hover ---
    def hover(self, event):   # event armazena dados como a posição do mouse e o eixo onde está

        # se o mouse estiver fora do gráfico, não exibo minha caixa (evitar bugs)
        if event.inaxes != self.ax:
            if self.annot.get_visible():
                self.annot.set_visible(False)
                self.canvas_scatter.draw_idle()
            return

        # Bioativos
        cont, ind = self.scatter_bio.contains(event)
        if cont:
            self.update_annot(ind, self.bioactive)
            self.canvas_scatter.draw_idle()
            return

        # Não bioativos
        cont, ind = self.scatter_non.contains(event)
        if cont:
            self.update_annot(ind, self.non_bioactive)
            self.canvas_scatter.draw_idle()
            return

        # Se não estiver sobre nenhum ponto
        if self.annot.get_visible():
            self.annot.set_visible(False)
            self.canvas_scatter.draw_idle()

    def style_axes(self, ax): 
        """Padroniza o visual dos eixos"""
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#88aa88")
        ax.spines["bottom"].set_color("#88aa88")
        ax.tick_params(colors="#cdeccd", labelsize=9)

    def hide_data(self):
        """Esconde a tabela e o gráfico, mantendo apenas o cabeçalho visível"""
        self.table.hide()
        self.canvas_scatter.hide()
        self.toolbar.hide()