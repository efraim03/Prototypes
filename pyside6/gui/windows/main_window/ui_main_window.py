# Importando o módulo qt_core para acessar as classes do PySide6
from qt_core import *

from widgets.py_pushbutton import PyPushButton
from pages.ui_login_page import LoginPage
from pages.ui_dashboard_page import DashboardPage


# Classe que irá receber todos os widgets da interface gráfica do MainWindow
class Ui_MainWindow(object):
    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName("MainWindow")
        
        # Define o tamanho da janela principal
        parent.resize(1200, 720)
        parent.setMinimumSize(960, 540)
        
        # Cria o widget pai da interface gráfica
        self.centralFrame = QFrame()

        # Cria o layout principal da interface gráfica
        self.main_layout = QHBoxLayout(self.centralFrame)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Menu lateral
        self.left_menu = QFrame()
        self.left_menu.setStyleSheet("background-color: hsl(145, 28%, 18%)")
        self.left_menu.setMaximumWidth(50)
        self.left_menu.setMinimumWidth(50)

        # Prepara o layout do menu lateral
        self.left_menu_layout = QVBoxLayout(self.left_menu)
        self.left_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.left_menu_layout.setSpacing(0)

        # Conteúdo da parte superior do menu lateral
        self.left_menu_top_frame = QFrame()
        self.left_menu_top_frame.setMinimumHeight(50)

        # Prepara o layout da parte superior do menu lateral, que irá conter os botões de navegação
        self.left_menu_top_layout = QVBoxLayout(self.left_menu_top_frame)
        self.left_menu_top_layout.setContentsMargins(0, 0, 0, 0)
        self.left_menu_top_layout.setSpacing(0)

        # Cria os botões de navegação da parte superior do menu lateral
        self.top_toggle_btn = PyPushButton("Ocultar Menu")
        self.top_btn1 = PyPushButton(
            text = "Página de Login",
            is_active = True
        )
        self.top_btn2 = PyPushButton("Dashboard")
        

        # Adiciona os botões de navegação ao layout da parte superior do menu lateral
        self.left_menu_top_layout.addWidget(self.top_toggle_btn)
        self.left_menu_top_layout.addWidget(self.top_btn1)
        self.left_menu_top_layout.addWidget(self.top_btn2)

        # Espaçador do menu lateral
        self.left_menu_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Conteúdo da parte inferior do menu lateral
        self.left_menu_bottom_frame = QFrame()
        self.left_menu_bottom_frame.setMinimumHeight(50)

        # Prepara o layout da parte inferior do menu lateral, que irá conter os botões de configuração e de logout
        self.left_menu_bottom_layout = QVBoxLayout(self.left_menu_bottom_frame)
        self.left_menu_bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.left_menu_bottom_layout.setSpacing(0)

        # Cria o botão de configurações da parte inferior do menu lateral
        self.bottom_btn = PyPushButton("Configurações")

        # Adiciona o botão de configurações ao layout da parte inferior do menu lateral
        self.left_menu_bottom_layout.addWidget(self.bottom_btn)

        # Label do menu lateral, que irá conter a versão da aplicação
        self.left_menu_label = QLabel("v1.0.0")
        self.left_menu_label.setAlignment(Qt.AlignCenter)
        self.left_menu_label.setMinimumHeight(30)
        self.left_menu_label.setMaximumHeight(30)
        self.left_menu_label.setStyleSheet("color: hsl(145, 10%, 92%)")

        # Adiciona os conteúdos criados ao layout do menu lateral
        self.left_menu_layout.addWidget(self.left_menu_top_frame)
        self.left_menu_layout.addItem(self.left_menu_spacer)
        self.left_menu_layout.addWidget(self.left_menu_bottom_frame)
        self.left_menu_layout.addWidget(self.left_menu_label)

        # Conteúdo do frame central da interface gráfica
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("background-color: hsl(145, 25%, 10%)")

        # Prepara o layout do conteúdo do frame central, que irá conter a barra superior, o conteúdo da página e a barra inferior
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # Barra superior
        self.top_bar = QFrame()
        self.top_bar.setMinimumHeight(30)
        self.top_bar.setMaximumHeight(30)
        self.top_bar.setStyleSheet("background-color: hsl(145, 20%, 6%); color: hsl(145, 15%, 72%)")

        # Prepara o layout da barra superior, que irá conter o texto à esquerda, um espaçador e o texto à direita
        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(10, 0, 10, 0)

        # Cria o texto à esquerda, o espaçador e o texto à direita da barra superior
        self.left_top_text = QLabel("Sistema de Prospecção de Bioativos")
        self.spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.right_top_text = QLabel("| PÁGINA INICIAL")
        self.right_top_text.setStyleSheet("font: 700 9pt 'Segoe UI'")

        # Adiciona o texto à esquerda, o espaçador e o texto à direita ao layout da barra superior
        self.top_bar_layout.addWidget(self.left_top_text)
        self.top_bar_layout.addItem(self.spacer)
        self.top_bar_layout.addWidget(self.right_top_text)

        #Conteúdo da página
        self.page_content = QStackedWidget()
        self.page_content.setStyleSheet("font-size: 16px; color: hsl(145, 10%, 92%)")

        # Cria a página de login usando a classe LoginPage, que é um widget personalizado criado no arquivo ui_login_page.py
        self.page1 = LoginPage()

        # Cria a página de dashboard usando a classe DashboardPage, que é um widget personalizado criado no arquivo ui_dashboard_page.py
        self.page2 = DashboardPage()

        # Cria a página de configurações, o layout da página, o texto da página e adiciona o texto ao layout da página
        self.page3 = QWidget()
        layout3 = QVBoxLayout(self.page3)
        self.page_config = QLabel("Configurações")
        layout3.addWidget(self.page_config)
        layout3.setAlignment(Qt.AlignCenter)

        # Adiciona as páginas de login, dashboard e configurações ao conteúdo da página
        self.page_content.addWidget(self.page1)
        self.page_content.addWidget(self.page2)
        self.page_content.addWidget(self.page3)

        # Altera a página atual
        self.page_content.setCurrentWidget(self.page1)

        # Barra inferior
        self.bottom_bar = QFrame()
        self.bottom_bar.setMinimumHeight(30)
        self.bottom_bar.setMaximumHeight(30)
        self.bottom_bar.setStyleSheet("background-color: hsl(145, 20%, 6%); color: hsl(145, 15%, 72%)")

        # Prepara o layout da barra inferior, que irá conter o texto à direita e um espaçador
        self.bottom_bar_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_bar_layout.setContentsMargins(10, 0, 10, 0)

        # Cria o texto à esquerda, o espaçador e o texto à direita da barra inferior
        self.left_bottom_text = QLabel("Criado por: Efraim R. Brito")
        self.spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.right_bottom_text = QLabel("© 2026")

        # Adiciona o texto à esquerda e o texto à direita ao layout da barra inferior
        self.bottom_bar_layout.addWidget(self.left_bottom_text)
        self.bottom_bar_layout.addItem(self.spacer)
        self.bottom_bar_layout.addWidget(self.right_bottom_text)

        # Adiciona a barra superior, o conteúdo da página e a barra inferior ao layout do conteúdo do frame central
        self.content_layout.addWidget(self.top_bar)
        self.content_layout.addWidget(self.page_content)
        self.content_layout.addWidget(self.bottom_bar)

        # Adiciona o menu lateral e o conteúdo do frame central ao layout principal
        self.main_layout.addWidget(self.left_menu)
        self.main_layout.addWidget(self.content_frame)

        # Set do widget pai da interface gráfica
        parent.setCentralWidget(self.centralFrame)