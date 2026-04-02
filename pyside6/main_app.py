import sys
import os

# Importando o módulo qt_core para acessar as classes do PySide6
from qt_core import *

# Importando a interface gráfica do MainWindow
from gui.windows.main_window.ui_main_window import *

# Classe principal da aplicação, onde a interface gráfica do MainWindow é carregada
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Define o título da janela principal
        self.setWindowTitle("BioSensIA")

        # Carrega a interface gráfica do MainWindow usando o método setup_ui da classe Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setup_ui(self)

        # Conecta o clique do botão de toggle do menu lateral à função toggle_btn para mostrar ou ocultar o menu lateral
        self.ui.top_toggle_btn.clicked.connect(self.toggle_btn)

        # Conecta os cliques dos botôes de navegação às suas paginas correspondentes
        self.ui.top_btn1.clicked.connect(self.show_page1)
        self.ui.top_btn2.clicked.connect(self.show_page2)
        self.ui.bottom_btn.clicked.connect(self.show_page3)

    # Funções para mostrar as páginas correspondentes aos botões de navegação
    def show_page1(self):
        self.ui.page_content.setCurrentWidget(self.ui.page1)
        self.ui.top_btn1.set_active(True)
        self.ui.top_btn2.set_active(False)
        self.ui.bottom_btn.set_active(False)
    
    def show_page2(self):
        self.ui.page_content.setCurrentWidget(self.ui.page2)
        self.ui.top_btn2.set_active(True)
        self.ui.top_btn1.set_active(False)
        self.ui.bottom_btn.set_active(False)

    def show_page3(self):
        self.ui.page_content.setCurrentWidget(self.ui.page3)
        self.ui.bottom_btn.set_active(True)
        self.ui.top_btn1.set_active(False)
        self.ui.top_btn2.set_active(False)

        # Exibe a janela principal
        self.show()

    # Função para mostrar ou ocultar o menu lateral com uma animação suave
    def toggle_btn(self):
        menu_width = self.ui.left_menu.width()
        if menu_width == 50:
            width = 240
        else:
            width = 50    

        self.animation = QPropertyAnimation(self.ui.left_menu, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(menu_width)
        self.animation.setEndValue(width)
        self.animation.setEasingCurve(QEasingCurve.InOutCirc)
        self.animation.start()    

# Garante que a interface gráfica seja carregada somente quando o arquivo for executado diretamente
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())