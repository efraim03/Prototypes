from qt_core import *
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class AnalysisTab(QWidget):
    def __init__(self):
        super().__init__()

        self.df = None

# --- Atributos ---
    # --- Layout principal ---
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setSpacing(15)

    # --- Tabela de estatísticas ---
        self.stats_table = QTableWidget()
        self.stats_table.setMinimumWidth(320)
        self.stats_table.setMaximumWidth(400)
        self.stats_table.setMaximumHeight(150)  # pequena por design
        self.stats_table.setStyleSheet("""
            background-color: #1a2e24;
            color: #e0eee0;
            border-radius: 8px;
            font-size: 10px;
        """)
    
    # Ajustar o tamanho das colunas e linhas para caber o conteúdo
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.stats_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
    # Impedir tabela de crescer desnecessariamente
        self.stats_table.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)

        header = self.stats_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.stats_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # --- Seleção de variável para análise ---
        self.left_controls = QVBoxLayout()

        self.col_selector = QComboBox()
        self.col_selector.setCursor(Qt.PointingHandCursor)

        self.view_selector = QComboBox()
        self.view_selector.addItems(["Histograma", "Correlação", "Bioatividade"])

        self.col_selector.setMinimumWidth(140)
        self.view_selector.setMinimumWidth(140)

        var_layout = QHBoxLayout()

        label_style = """
            font-size: 12px;
            color: #a8cfa8;
        """

        combo_style = """
            QComboBox {
                font-size: 12px;
                color: #e0eee0;
                background-color: #1a2e24;
                border: 1px solid #2e5a40;
                border-radius: 6px;
                padding: 4px 8px;
            }

            QComboBox:hover {
                border: 1px solid #3d7a55;
            }

            QComboBox::drop-down {
                border: none;
            }

            QComboBox QAbstractItemView {
                background-color: #1a2e24;
                color: #e0eee0;
                selection-background-color: #2e5a40;
                selection-color: #ffffff;
                font-size: 12px;
            }
        """

        var_label = QLabel("Variável:")

        var_layout.addWidget(var_label)
        var_layout.addWidget(self.col_selector)

        self.left_controls.addLayout(var_layout)

        view_layout = QHBoxLayout()

        view_label = QLabel("Visualização:")

        var_label.setStyleSheet(label_style)
        self.col_selector.setStyleSheet(combo_style)

        view_label.setStyleSheet(label_style)
        self.view_selector.setStyleSheet(combo_style)

        view_layout.addWidget(view_label)
        view_layout.addWidget(self.view_selector)

        self.left_controls.addLayout(view_layout)

        self.left_controls.addStretch()

        self.left_panel = QVBoxLayout()
        self.left_panel.addWidget(self.stats_table)
        self.left_panel.addLayout(self.left_controls)

        self.main_layout.addLayout(self.left_panel, 1)

    # --- Área de visualização (gráficos, etc) ---
        self.stack = QStackedWidget()

        # Placeholder inicial
        self.empty_label = QLabel("Carregue um dataset para começar")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("color: #88aa88;")

        self.stack.addWidget(self.empty_label)

    # --- Histograma ---
        self.hist_widget = QWidget()
        self.hist_layout = QVBoxLayout(self.hist_widget)

        self.fig_hist = Figure(facecolor="#0f1f17")
        self.canvas_hist = FigureCanvas(self.fig_hist)

        self.hist_layout.addWidget(self.canvas_hist)

        self.stack.addWidget(self.hist_widget)

        self.col_selector.currentTextChanged.connect(self.refresh_view)

    # --- Heatmap ---
        self.heatmap_widget = QWidget()
        self.heatmap_layout = QVBoxLayout(self.heatmap_widget)

        self.fig_heatmap = Figure(facecolor="#0f1f17")
        self.canvas_heatmap = FigureCanvas(self.fig_heatmap)

        self.heatmap_layout.addWidget(self.canvas_heatmap)

        self.stack.addWidget(self.heatmap_widget)

    # --- Bioatividade ---
        self.bio_widget = QWidget()
        self.bio_layout = QVBoxLayout(self.bio_widget)

        self.fig_bio = Figure(facecolor="#0f1f17")
        self.canvas_bio = FigureCanvas(self.fig_bio)

        self.bio_layout.addWidget(self.canvas_bio)

        self.stack.addWidget(self.bio_widget)

        self.canvas_bio.mpl_connect("motion_notify_event", self.on_hover_box)

        # adiciona a pilha de visualização à interface
        self.main_layout.addWidget(self.stack, 4)

        # conexão
        self.col_selector.currentTextChanged.connect(self.update_stats)
        self.view_selector.currentIndexChanged.connect(self.handle_view_change)

# --- Métodos ---
    # Método para receber o DataFrame
    def load_data(self, df):
        self.df = df

        numeric_cols = df.select_dtypes(include="number").columns

        self.col_selector.clear()
        self.col_selector.addItems(numeric_cols)

        self.populate_stats_table()

        if len(numeric_cols) > 0:
            self.col_selector.setCurrentIndex(0)

            # 🔥 ORDEM IMPORTA
            self.update_histogram()  # gera o gráfico
            self.stack.setCurrentIndex(1)  # mostra histograma direto
    
    # Método para criar a tabela de estatísticas
    def populate_stats_table(self):
        df = self.df.select_dtypes(include="number")

        stats_df = pd.DataFrame({
            "Média": df.mean(),
            "Mediana": df.median(),
            "Desvio": df.std(),
            "Mín": df.min(),
            "Máx": df.max()
        }).T # Transposta para ter as estatísticas como linhas

        self.stats_table.setRowCount(len(stats_df.index))
        self.stats_table.setColumnCount(len(stats_df.columns))

        self.stats_table.setHorizontalHeaderLabels(stats_df.columns)
        self.stats_table.setVerticalHeaderLabels(stats_df.index)

        for i in range(len(stats_df.index)):
            for j in range(len(stats_df.columns)):
                value = stats_df.iloc[i, j]
                item = QTableWidgetItem(f"{value:.2f}")
                self.stats_table.setItem(i, j, item)

    # Atualiza gráficos com base na coluna selecionada
    def update_stats(self):
        col = self.col_selector.currentText()

        if not col or self.df is None:
            return

        series = pd.to_numeric(self.df[col], errors="coerce").dropna()

        # Aqui depois vamos ligar com histograma, etc.
        print(f"Selecionado: {col}")

    def change_view(self, index):
        if self.df is None:
            self.stack.setCurrentIndex(0)  # placeholder
        else:
            self.stack.setCurrentIndex(index + 1)  # +1 porque o index 0 é o placeholder

    def update_histogram(self):
        if self.df is None:
            return
        
        col = self.col_selector.currentText()
        if not col:
            return

        data = pd.to_numeric(self.df[col], errors="coerce").dropna()

        self.fig_hist.clear()
        ax = self.fig_hist.add_subplot(111)

        ax.set_facecolor("#0f1f17")

        ax.hist(
            data,
            bins=20,
            edgecolor="white",
            color="#4fa3ff",
            alpha=0.8
        )

        ax.set_title(f"Distribuição de {col}", color="#cdeccd")
        ax.set_xlabel(col, color="#cdeccd")
        ax.set_ylabel("Frequência", color="#cdeccd")

        # estilo igual ao scatter
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#88aa88")
        ax.spines["bottom"].set_color("#88aa88")
        ax.tick_params(colors="#cdeccd")

        counts, bins, patches = ax.hist(data, bins=20, edgecolor="white")

        self.hist_bins = bins
        self.hist_counts = counts
        self.hist_patches = patches
        self.ax_hist = ax

        self.annot = ax.annotate(
        "",
        xy=(0, 0),
        xytext=(10, 10),
        textcoords="offset points",
        bbox=dict(boxstyle="round", fc="#1a2e24", ec="white"),
        color="white"
        )

        self.annot.set_visible(False)

        self.canvas_hist.mpl_connect("motion_notify_event", self.hover_hist)

        self.canvas_hist.draw()

    def hover_hist(self, event):
        if event.inaxes != self.ax_hist:
            if self.annot.get_visible():
                self.annot.set_visible(False)
                self.canvas_hist.draw_idle()
            return

        for i, patch in enumerate(self.hist_patches):
            contains, _ = patch.contains(event)

            if contains:
                bin_start = self.hist_bins[i]
                bin_end = self.hist_bins[i+1]
                count = self.hist_counts[i]

                self.annot.xy = (event.xdata, event.ydata)
                self.annot.set_text(
                    f"{bin_start:.2f} - {bin_end:.2f}\nFreq: {int(count)}"
                )
                self.annot.set_visible(True)
                self.canvas_hist.draw_idle()
                return

        if self.annot.get_visible():
            self.annot.set_visible(False)
            self.canvas_hist.draw_idle()

    def update_heatmap(self):
        if self.df is None:
            return

        df = self.df.select_dtypes(include="number")
        corr = df.corr()

        self.fig_heatmap.clear()

        # 🔥 figura maior e melhor distribuída
        self.fig_heatmap.set_size_inches(6, 5)

        ax = self.fig_heatmap.add_subplot(111)
        ax.set_facecolor("#0f1f17")

        # 🔥 heatmap mais bonito
        cax = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)

        # 🔥 ticks organizados
        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.columns)))

        ax.set_xticklabels(
            corr.columns,
            rotation=30,
            ha="right",
            fontsize=9,
            color="#cdeccd"
        )

        ax.set_yticklabels(
            corr.columns,
            fontsize=9,
            color="#cdeccd"
        )

        # 🔥 valores dentro dos blocos (com contraste automático)
        for i in range(len(corr.columns)):
            for j in range(len(corr.columns)):
                value = corr.iloc[i, j]

                color = "white" if abs(value) > 0.5 else "#0f1f17"

                ax.text(
                    j, i,
                    f"{value:.2f}",
                    ha="center",
                    va="center",
                    fontsize=8,
                    color=color
                )

        # 🔥 barra lateral bonita
        cbar = self.fig_heatmap.colorbar(cax, shrink=0.8)
        cbar.outline.set_visible(False)
        cbar.ax.tick_params(colors="#cdeccd")

        # 🔥 remove bordas feias
        for spine in ax.spines.values():
            spine.set_visible(False)

        self.fig_heatmap.tight_layout()
        self.canvas_heatmap.draw()

    def update_bioactivity(self):
        if self.df is None:
            return

        col = self.col_selector.currentText()

        if not col or col == "bioactivity":
            return

        data = self.df.copy()

        # separar grupos corretamente
        bio_0 = pd.to_numeric(
            data[data["bioactivity"] == 0][col],
            errors="coerce"
        ).dropna()

        bio_1 = pd.to_numeric(
            data[data["bioactivity"] == 1][col],
            errors="coerce"
        ).dropna()

        # limpa figura antes de desenhar
        self.fig_bio.clear()
        ax = self.fig_bio.add_subplot(111)

        ax.set_facecolor("#0f1f17")

        # boxplot
        box = ax.boxplot(
            [bio_0, bio_1],
            labels=["Não Bioativo", "Bioativo"],
            patch_artist=True
        )

        # cores
        colors = ["#ff4d4d", "#4fa3ff"]

        for patch, color in zip(box["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        # estilo linhas
        for element in ["whiskers", "caps", "medians"]:
            for item in box[element]:
                item.set_color("#e0eee0")

        # médias (agora no lugar certo)
        means = [bio_0.mean(), bio_1.mean()]
        ax.scatter([1, 2], means, color="yellow", zorder=3)

        # labels
        ax.set_title(f"{col} vs Bioatividade", color="#cdeccd")
        ax.set_xlabel("Grupo", color="#cdeccd")
        ax.set_ylabel(col, color="#cdeccd")
        ax.grid(alpha=0.1)

        ax.tick_params(colors="#cdeccd")

        # bordas
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#88aa88")
        ax.spines["bottom"].set_color("#88aa88")

        self.fig_bio.tight_layout()
        self.canvas_bio.draw()

    def handle_view_change(self, index):
        self.change_view(index)

        if index == 0:
            self.update_histogram()
        elif index == 1:
            self.update_heatmap()
        elif index == 2:
            self.update_bioactivity()

    def refresh_view(self):
        index = self.view_selector.currentIndex()

        if index == 0:
            self.update_histogram()
        elif index == 1:
            self.update_heatmap()
        elif index == 2:
            self.update_bioactivity()

    def on_hover_box(self, event):
        if event.inaxes is None:
            return

        ax = event.inaxes
        x = event.xdata

        if x is None:
            return

        if x < 1.5:
            label = "Não Bioativo"
        else:
            label = "Bioativo"

        self.canvas_bio.setToolTip(f"Grupo: {label}")