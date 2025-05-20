from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ColorProperty
from kivy.animation import Animation
from kivy.core.window import Window

# Definindo as cores
COR_FUNDO = "#f7f7ff"
COR_TITULO = "#22223b"
COR_LABEL = "#22223b"
COR_ENTRADA = "#ffffff"
COR_BOTAO = "#5f6cff"
COR_BOTAO_HOVER = "#3a47a8"
COR_ERRO = "#e63946"
COR_ANIMACOES = {
    "baixo_peso": "#00b4d8",   # azul
    "normal": "#43aa8b",       # verde
    "sobrepeso": "#f9c74f",    # amarelo
    "obesidade": "#f3722c"     # laranja
}

KV = '''
#:import hex kivy.utils.get_color_from_hex

<AnimButton@Button>:
    background_normal: ''
    background_color: hex("5f6cff")
    color: 1, 1, 1, 1
    font_size: '17sp'
    font_name: 'Roboto'
    bold: True
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [18]
    on_press:
        self.background_color = hex("3a47a8")
    on_release:
        self.background_color = hex("5f6cff")

BoxLayout:
    orientation: 'vertical'
    padding: [22, 20, 22, 20]
    spacing: 14
    canvas.before:
        Color:
            rgba: hex("f7f7ff")
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "Calculadora de IMC"
        font_size: '28sp'
        font_name: 'Roboto'
        color: hex("22223b")
        bold: True
        size_hint_y: None
        height: dp(52)
        opacity: 0
        id: titulo
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
        spacing: 4

        Label:
            text: "Peso (kg):"
            font_size: '16sp'
            color: hex("22223b")
            size_hint_y: None
            height: dp(26)
            font_name: 'Roboto'
        TextInput:
            id: peso_input
            hint_text: "Ex: 70"
            font_size: '16sp'
            background_color: hex("ffffff")
            foreground_color: hex("22223b")
            cursor_color: hex("5f6cff")
            multiline: False
            padding: [10, 10]
            size_hint_y: None
            height: dp(38)
            halign: 'center'
            font_name: 'Roboto'

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
        spacing: 4

        Label:
            text: "Altura (m):"
            font_size: '16sp'
            color: hex("22223b")
            size_hint_y: None
            height: dp(26)
            font_name: 'Roboto'
        TextInput:
            id: altura_input
            hint_text: "Ex: 1.75"
            font_size: '16sp'
            background_color: hex("ffffff")
            foreground_color: hex("22223b")
            cursor_color: hex("5f6cff")
            multiline: False
            padding: [10, 10]
            size_hint_y: None
            height: dp(38)
            halign: 'center'
            font_name: 'Roboto'

    Widget:
        size_hint_y: None
        height: dp(8)

    AnimButton:
        id: calcular_btn
        text: "Calcular IMC"
        size_hint_y: None
        height: dp(45)
        font_size: '17sp'
        on_release: app.calcular_imc()

    Widget:
        size_hint_y: None
        height: dp(6)

    Label:
        id: resultado
        text: app.resultado_text
        font_size: '20sp'
        font_name: 'Roboto'
        color: app.resultado_cor
        halign: 'center'
        valign: 'middle'
        size_hint_y: None
        height: dp(56)
        bold: True
'''

class IMCApp(App):
    resultado_text = StringProperty("")
    resultado_cor = ColorProperty([0.13, 0.13, 0.23, 1])  # Default: COR_TITULO

    def build(self):
        Window.clearcolor = self.hex_to_rgb(COR_FUNDO)
        root = Builder.load_string(KV)
        # Animação de entrada para o título
        self.animar_entrada(root.ids.titulo)
        return root

    def animar_entrada(self, widget):
        widget.opacity = 0
        anim = Animation(opacity=1, d=0.7, t='out_cubic')
        anim.start(widget)

    def animar_resultado(self, cor_final):
        anim = Animation(resultado_cor=self.hex_to_rgb(cor_final), d=0.32, t="out_quad")
        anim.start(self)

    def pulse_resultado(self):
        label = self.root.ids.resultado
        anim_up = Animation(font_size=26, d=0.12, t='out_quad')
        anim_down = Animation(font_size=20, d=0.12, t='out_quad')
        anim = anim_up + anim_down
        anim.start(label)

    def calcular_imc(self):
        peso_txt = self.root.ids.peso_input.text.strip().replace(",", ".")
        altura_txt = self.root.ids.altura_input.text.strip().replace(",", ".")
        try:
            peso = float(peso_txt)
            altura = float(altura_txt)
            if peso <= 0 or altura <= 0:
                raise ValueError
            imc = peso / (altura ** 2)
            if imc < 18.5:
                texto = f"Seu IMC é: {imc:.2f} (Baixo peso)"
                cor = COR_ANIMACOES["baixo_peso"]
            elif imc < 25:
                texto = f"Seu IMC é: {imc:.2f} (Normal)"
                cor = COR_ANIMACOES["normal"]
            elif imc < 30:
                texto = f"Seu IMC é: {imc:.2f} (Sobrepeso)"
                cor = COR_ANIMACOES["sobrepeso"]
            else:
                texto = f"Seu IMC é: {imc:.2f} (Obesidade)"
                cor = COR_ANIMACOES["obesidade"]
            self.resultado_text = texto
            self.resultado_cor = self.hex_to_rgb(COR_TITULO)
            self.animar_resultado(cor)
            self.pulse_resultado()
        except Exception:
            self.resultado_text = "Entrada inválida! Use números válidos."
            self.resultado_cor = self.hex_to_rgb(COR_ERRO)
            self.pulse_resultado()

    @staticmethod
    def hex_to_rgb(hex_color):
        """Converte cor hexadecimal para tupla RGBA normalizada"""
        hex_color = hex_color.lstrip("#")
        lv = len(hex_color)
        rgb = tuple(int(hex_color[i:i+2], 16)/255. for i in (0, 2, 4))
        return rgb + (1,)

if __name__ == "__main__":
    IMCApp().run()