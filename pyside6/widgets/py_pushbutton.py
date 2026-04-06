import os

from qt_core import *

class PyPushButton(QPushButton):

    # Define parâmetros personalizáveis para o botão, como texto, cores, tamanhos e estado ativo
    def __init__(
        self,
        text="",
        height=40,
        minimum_width=50,
        text_padding=55,
        text_color="hsl(145, 10%, 92%)",
        icon_path="",
        icon_color="hsl(145, 10%, 92%)",
        btn_color="hsl(145, 28%, 18%)",
        btn_hover="hsl(145, 28%, 22%)",
        btn_pressed="hsl(145, 28%, 26%)",
        is_active=False
    ):
        super().__init__()

        self.setText(text)
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)
        self.setCursor(Qt.PointingHandCursor)
        
        self.minimum_width = minimum_width
        self.text_padding = text_padding
        self.text_color = text_color
        self.icon_color = icon_color
        self.btn_color = btn_color
        self.btn_hover = btn_hover
        self.btn_pressed = btn_pressed
        self.is_active = is_active

        # Aplica o estilo inicial do botão com base nos parâmetros fornecidos
        self.set_style( 
            text_padding=self.text_padding,
            text_color=self.text_color,
            btn_color=self.btn_color,
            btn_hover=self.btn_hover,
            btn_pressed=self.btn_pressed,
            is_active=self.is_active
        )

    # Função para atualizar o estilo do botão com base no estado ativo
    def set_active(self, is_active_menu): 
        self.set_style(
            text_padding=self.text_padding,
            text_color=self.text_color,
            btn_color=self.btn_color,
            btn_hover=self.btn_hover,
            btn_pressed=self.btn_pressed,
            is_active=is_active_menu # Retorna true ou false
        )

    # Método que irá atualizar o estilo do botão com base no is_active
    def set_style(
        self,
        text_padding=55,
        text_color="hsl(145, 10%, 92%)",
        btn_color="hsl(145, 28%, 18%)",
        btn_hover="hsl(145, 28%, 22%)",
        btn_pressed="hsl(145, 28%, 26%)",
        is_active=False
    ):
        style = f"""
        QPushButton {{
            color: {text_color};
            background-color: {btn_color};
            padding-left: {text_padding}px;
            text-align: left;
            border: none;
        }}
        QPushButton:hover {{
            background-color: {btn_hover};
        }}
        QPushButton:pressed {{
            background-color: {btn_pressed};
        }}
        """
        active_style = f"""
        QPushButton {{
            background-color: {btn_pressed};
            border-right: 5px solid hsl(145, 25%, 10%);
        }}
        """
        
        if not is_active:
            self.setStyleSheet(style)
        else:
            self.setStyleSheet(style + active_style) 