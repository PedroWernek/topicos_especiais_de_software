import sys
import os
import json
from pathlib import Path
import time

# IMPORTANDO DA BIBLIOTECA OFICIAL (PYSIDE6)
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton, QSlider, QLabel,
                               QListWidget, QFileDialog, QDialog, QLineEdit,
                               QFormLayout, QMessageBox, QCheckBox)
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

# ==========================================
# MONITOR GLOBAL DE TECLADO E MOUSE
# ==========================================
from pynput import keyboard, mouse


class MonitorDeAtividade:
    def __init__(self):
        self.nivel_atividade = 0.0

        self.ganho_tecla = 8.0
        self.ganho_mouse = 5.0
        self.fator_decaimento = 0.94

        self.listener_teclado = keyboard.Listener(on_press=self.registrar_acao)
        self.listener_mouse = mouse.Listener(on_click=self.registrar_clique)

        self.listener_teclado.start()
        self.listener_mouse.start()

    def registrar_acao(self, key):
        self.nivel_atividade = min(100.0, self.nivel_atividade + self.ganho_tecla)

    def registrar_clique(self, x, y, button, pressed):
        if pressed:
            self.nivel_atividade = min(100.0, self.nivel_atividade + self.ganho_mouse)

    def decair(self):
        self.nivel_atividade *= self.fator_decaimento
        if self.nivel_atividade < 0.1:
            self.nivel_atividade = 0.0

    def encerrar(self):
        self.listener_teclado.stop()
        self.listener_mouse.stop()


# ==========================================
# ESTÉTICA MODERNA
# ==========================================
ESTILO_MODERNO = """
    QMainWindow { background-color: #121212; }
    QWidget { font-family: "Segoe UI", sans-serif; font-size: 13px; }
    QLabel { color: #B3B3B3; font-weight: 500; }

    QLabel#lcd {
        background-color: #1E1E1E; color: #1DB954;
        font-family: "Consolas", monospace; font-size: 14px;
        font-weight: bold; border-radius: 8px; padding: 10px;
    }
    QLabel#thumb { background-color: #1E1E1E; border-radius: 12px; }

    QPushButton {
        background-color: #282828; color: #FFFFFF;
        border: 1px solid #3E3E3E; border-radius: 6px; 
        padding: 8px; font-weight: bold;
    }
    QPushButton:hover { background-color: #3E3E3E; }
    QPushButton:pressed { background-color: #1DB954; color: #000000; border: none; }

    QListWidget {
        background-color: #181818; color: #FFFFFF; border: none; 
        border-radius: 8px; padding: 5px; outline: none;
    }
    QListWidget::item { padding: 8px; border-radius: 4px; }
    QListWidget::item:selected { background-color: #282828; color: #1DB954; font-weight: bold; }
    QListWidget::item:hover:!selected { background-color: #333333; }

    QSlider::groove:horizontal { background: #3E3E3E; height: 6px; border-radius: 3px; }
    QSlider::sub-page:horizontal { background: #1DB954; border-radius: 3px; }
    QSlider::handle:horizontal { background: #FFFFFF; width: 14px; margin: -4px 0; border-radius: 7px; }
    QSlider::handle:horizontal:hover { background: #1DB954; }

    QCheckBox { color: #FFFFFF; font-weight: bold; }
    QCheckBox::indicator { width: 18px; height: 18px; border-radius: 4px; border: 2px solid #3E3E3E; background: #181818; }
    QCheckBox::indicator:checked { background: #1DB954; border-color: #1DB954; }

    QLineEdit { background-color: #282828; color: #FFFFFF; border: 1px solid #3E3E3E; border-radius: 6px; padding: 6px; }
"""

ARQUIVO_BIBLIOTECA = "biblioteca_mashups.json"


def carregar_biblioteca():
    if not os.path.exists(ARQUIVO_BIBLIOTECA): return []
    with open(ARQUIVO_BIBLIOTECA, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []


def salvar_biblioteca(dados):
    with open(ARQUIVO_BIBLIOTECA, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


# ==========================================
# DIÁLOGO DE MASHUP
# ==========================================
class DialogNovoMashup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adicionar Novo Mashup")
        self.resize(500, 300)
        self.setStyleSheet(ESTILO_MODERNO)

        self.dados = {}
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.input_titulo = QLineEdit()
        self.input_titulo.setPlaceholderText("Ex: Tema Épico Batalha")
        layout.addRow("Título:", self.input_titulo)

        self.path_calma, self.path_agitada, self.path_thumb = "", "", ""

        self.lbl_calma = QLabel("Nenhum arquivo")
        btn_calma = QPushButton("Procurar...")
        btn_calma.clicked.connect(lambda: self.buscar_arquivo(self.lbl_calma, "calma"))
        box_c = QHBoxLayout();
        box_c.addWidget(self.lbl_calma);
        box_c.addWidget(btn_calma)
        layout.addRow("Faixa Calma:", box_c)

        self.lbl_agitada = QLabel("Nenhum arquivo")
        btn_agitada = QPushButton("Procurar...")
        btn_agitada.clicked.connect(lambda: self.buscar_arquivo(self.lbl_agitada, "agitada"))
        box_a = QHBoxLayout();
        box_a.addWidget(self.lbl_agitada);
        box_a.addWidget(btn_agitada)
        layout.addRow("Faixa Agitada:", box_a)

        self.lbl_thumb = QLabel("Nenhuma imagem")
        btn_thumb = QPushButton("Procurar...")
        btn_thumb.clicked.connect(lambda: self.buscar_arquivo(self.lbl_thumb, "thumb", True))
        box_t = QHBoxLayout();
        box_t.addWidget(self.lbl_thumb);
        box_t.addWidget(btn_thumb)
        layout.addRow("Capa (Opcional):", box_t)

        self.input_loop = QLineEdit("0.0")
        layout.addRow("Loop Customizado (segundos):", self.input_loop)

        btn_salvar = QPushButton("SALVAR MASHUP")
        btn_salvar.setStyleSheet("background-color: #1DB954; color: black; padding: 10px; margin-top: 10px;")
        btn_salvar.clicked.connect(self.salvar)
        layout.addRow("", btn_salvar)

    def buscar_arquivo(self, label, tipo, is_img=False):
        filtro = "Imagem (*.png *.jpg *.jpeg)" if is_img else "Áudio (*.mp3 *.wav *.ogg)"
        c, _ = QFileDialog.getOpenFileName(self, "Selecionar", "", filtro)
        if c:
            setattr(self, f"path_{tipo}", c)
            label.setText(Path(c).name)

    def salvar(self):
        if not self.input_titulo.text() or not self.path_calma or not self.path_agitada:
            QMessageBox.warning(self, "Erro", "Preencha o título e as duas faixas!")
            return
        try:
            loop_val = float(self.input_loop.text().replace(',', '.'))
        except ValueError:
            QMessageBox.warning(self, "Erro", "Tempo de loop deve ser um número!")
            return

        self.dados = {
            "titulo": self.input_titulo.text(),
            "calma": self.path_calma,
            "agitada": self.path_agitada,
            "thumb": self.path_thumb,
            "loop_tempo": max(0.0, loop_val)
        }
        self.accept()


# ==========================================
# PLAYER PRINCIPAL (PYSIDE6)
# ==========================================
class PlayerMashupModerno(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MashupAMP - Native Audio Engine")
        self.resize(900, 500)
        self.setStyleSheet(ESTILO_MODERNO)

        self.player_calma = QMediaPlayer()
        self.audio_calma = QAudioOutput()
        self.player_calma.setAudioOutput(self.audio_calma)

        self.player_agitada = QMediaPlayer()
        self.audio_agitada = QAudioOutput()
        self.player_agitada.setAudioOutput(self.audio_agitada)

        self.biblioteca = carregar_biblioteca()
        self.mashup_atual = None
        self.tocando = False
        self.loop_customizado = 0.0

        self.monitor_atividade = MonitorDeAtividade()

        self.iniciar_interface()
        self.atualizar_lista()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loop_principal)
        self.timer.start(50)

    def iniciar_interface(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout_principal = QHBoxLayout(central)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(20)

        painel_esq = QVBoxLayout()
        painel_esq.setSpacing(10)

        lbl_lista = QLabel("SUA BIBLIOTECA")
        lbl_lista.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        painel_esq.addWidget(lbl_lista)

        self.lista_ui = QListWidget()
        self.lista_ui.itemClicked.connect(self.selecionar_mashup_da_lista)
        painel_esq.addWidget(self.lista_ui)

        box_botoes = QHBoxLayout()
        btn_add = QPushButton("+ Adicionar")
        btn_add.clicked.connect(self.adicionar_mashup)
        btn_del = QPushButton("Remover")
        btn_del.clicked.connect(self.remover_mashup)
        box_botoes.addWidget(btn_add)
        box_botoes.addWidget(btn_del)
        painel_esq.addLayout(box_botoes)

        layout_principal.addLayout(painel_esq, stretch=1)

        painel_dir = QVBoxLayout()
        painel_dir.setSpacing(15)

        box_display = QHBoxLayout()
        box_display.setSpacing(20)

        self.img_thumb = QLabel("NO IMG")
        self.img_thumb.setObjectName("thumb")
        self.img_thumb.setFixedSize(120, 120)
        self.img_thumb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box_display.addWidget(self.img_thumb)

        box_lcd = QVBoxLayout()
        self.lcd_titulo = QLabel("Selecione uma faixa...")
        self.lcd_titulo.setObjectName("lcd")

        self.lcd_status = QLabel("[ PARADO ]")
        self.lcd_status.setObjectName("lcd")
        self.lcd_status.setStyleSheet("color: #B3B3B3; font-size: 12px; border: none; background: transparent;")

        box_lcd.addWidget(self.lcd_titulo)
        box_lcd.addWidget(self.lcd_status)
        box_lcd.addStretch()
        box_display.addLayout(box_lcd)
        painel_dir.addLayout(box_display)

        box_controles = QHBoxLayout()
        self.btn_play = QPushButton("▶ PLAY")
        self.btn_play.setStyleSheet("background-color: #1DB954; color: black; font-size: 14px; padding: 12px;")
        self.btn_play.clicked.connect(self.tocar_mashup)

        self.btn_stop = QPushButton("⏹ STOP")
        self.btn_stop.setStyleSheet("padding: 12px;")
        self.btn_stop.clicked.connect(self.parar_mashup)

        self.chk_loop = QCheckBox("🔂 Loop Automático")
        self.chk_loop.setChecked(True)
        self.chk_loop.clicked.connect(self.aplicar_regras_de_loop)

        box_controles.addWidget(self.btn_play)
        box_controles.addWidget(self.btn_stop)
        box_controles.addWidget(self.chk_loop)
        painel_dir.addLayout(box_controles)

        linha = QWidget()
        linha.setFixedHeight(1)
        linha.setStyleSheet("background-color: #3E3E3E; margin: 10px 0;")
        painel_dir.addWidget(linha)

        self.chk_automix = QCheckBox("Modo Auto-Mix (Intensidade baseada na digitação)")
        painel_dir.addWidget(self.chk_automix)

        box_config_mix = QHBoxLayout()

        box_sens = QVBoxLayout()
        self.lbl_sens = QLabel("Força da Tecla: 8.0")
        self.slider_sens = QSlider(Qt.Orientation.Horizontal)
        self.slider_sens.setRange(1, 40)
        self.slider_sens.setValue(8)
        self.slider_sens.valueChanged.connect(self.atualizar_configs_automix)
        box_sens.addWidget(self.lbl_sens)
        box_sens.addWidget(self.slider_sens)

        box_dec = QVBoxLayout()
        self.lbl_dec = QLabel("Queda p/ Calma: Normal")
        self.slider_dec = QSlider(Qt.Orientation.Horizontal)
        self.slider_dec.setRange(800, 1000)
        self.slider_dec.setValue(940)
        self.slider_dec.valueChanged.connect(self.atualizar_configs_automix)
        box_dec.addWidget(self.lbl_dec)
        box_dec.addWidget(self.slider_dec)

        box_config_mix.addLayout(box_sens)
        box_config_mix.addSpacing(20)
        box_config_mix.addLayout(box_dec)
        painel_dir.addLayout(box_config_mix)

        painel_dir.addSpacing(10)
        lbl_mixer = QLabel("CROSSFADER MANUAL (Calma ➔ Agitada)")
        lbl_mixer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        painel_dir.addWidget(lbl_mixer)

        self.slider_mixer = QSlider(Qt.Orientation.Horizontal)
        self.slider_mixer.setRange(0, 100)
        self.slider_mixer.valueChanged.connect(self.atualizar_volume)
        painel_dir.addWidget(self.slider_mixer)

        layout_principal.addLayout(painel_dir, stretch=2)

    def atualizar_configs_automix(self):
        ganho = float(self.slider_sens.value())
        decaimento = float(self.slider_dec.value()) / 1000.0

        self.monitor_atividade.ganho_tecla = ganho
        self.monitor_atividade.ganho_mouse = ganho * 0.6
        self.monitor_atividade.fator_decaimento = decaimento

        self.lbl_sens.setText(f"Força da Tecla: {ganho}")

        if decaimento >= 1.0:
            texto_dec = "TRAVADA (Não cai)"
        elif decaimento >= 0.995:
            texto_dec = "Quase Parando (Máxima)"
        elif decaimento >= 0.980:
            texto_dec = "Muito Lenta"
        elif decaimento >= 0.940:
            texto_dec = "Normal"
        elif decaimento >= 0.880:
            texto_dec = "Rápida"
        else:
            texto_dec = "Extrema"
        self.lbl_dec.setText(f"Queda p/ Calma: {texto_dec}")

    def loop_principal(self):
        if self.chk_automix.isChecked():
            nivel_seguro = max(0.0, min(100.0, self.monitor_atividade.nivel_atividade))
            self.slider_mixer.setValue(int(nivel_seguro))
            self.monitor_atividade.decair()
        else:
            self.monitor_atividade.nivel_atividade = 0.0

        if self.tocando:
            if self.chk_loop.isChecked() and self.loop_customizado > 0:
                decorrido = self.player_calma.position() / 1000.0
                restante = max(0.0, self.loop_customizado - decorrido)
                self.lcd_status.setText(f"▶ TOCANDO | REINICIA EM: {restante:.1f}s")

                if decorrido >= self.loop_customizado:
                    self.player_calma.setPosition(0)
                    self.player_agitada.setPosition(0)
            else:
                loop_texto = "ON" if self.chk_loop.isChecked() else "OFF"
                self.lcd_status.setText(f"▶ TOCANDO | LOOP GLOBAL: {loop_texto}")

    def atualizar_lista(self):
        self.lista_ui.clear()
        for idx, item in enumerate(self.biblioteca):
            self.lista_ui.addItem(f"{idx + 1}. {item['titulo']}")

    def adicionar_mashup(self):
        dialogo = DialogNovoMashup(self)
        if dialogo.exec():
            self.biblioteca.append(dialogo.dados)
            salvar_biblioteca(self.biblioteca)
            self.atualizar_lista()

    def remover_mashup(self):
        linha = self.lista_ui.currentRow()
        if linha >= 0:
            del self.biblioteca[linha]
            salvar_biblioteca(self.biblioteca)
            self.atualizar_lista()
            self.parar_mashup()
            self.lcd_titulo.setText("Selecione uma faixa...")

    def selecionar_mashup_da_lista(self, item):
        linha = self.lista_ui.currentRow()
        self.mashup_atual = self.biblioteca[linha]
        self.loop_customizado = self.mashup_atual.get('loop_tempo', 0.0)

        self.lcd_titulo.setText(self.mashup_atual['titulo'].upper())

        caminho_img = self.mashup_atual.get('thumb', '')
        if caminho_img and os.path.exists(caminho_img):
            pixmap = QPixmap(caminho_img).scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
            self.img_thumb.setPixmap(pixmap)
        else:
            self.img_thumb.clear()
            self.img_thumb.setText("NO IMG")

        self.parar_mashup()

    def aplicar_regras_de_loop(self):
        if self.chk_loop.isChecked() and self.loop_customizado <= 0:
            self.player_calma.setLoops(-1)
            self.player_agitada.setLoops(-1)
        else:
            self.player_calma.setLoops(1)
            self.player_agitada.setLoops(1)

    def tocar_mashup(self):
        if not self.mashup_atual or self.tocando: return

        self.player_calma.setSource(QUrl.fromLocalFile(self.mashup_atual['calma']))
        self.player_agitada.setSource(QUrl.fromLocalFile(self.mashup_atual['agitada']))

        self.aplicar_regras_de_loop()

        self.player_calma.play()
        self.player_agitada.play()

        self.tocando = True
        self.atualizar_volume()

    def parar_mashup(self):
        self.player_calma.stop()
        self.player_agitada.stop()
        self.tocando = False
        self.lcd_status.setText("[ PARADO ]")

    def atualizar_volume(self):
        valor = self.slider_mixer.value() / 100.0
        vol_calma = max(0.0, min(1.0, 1.0 - valor))
        vol_agitada = max(0.0, min(1.0, valor))

        self.audio_calma.setVolume(vol_calma)
        self.audio_agitada.setVolume(vol_agitada)

    def closeEvent(self, event):
        self.monitor_atividade.encerrar()
        self.parar_mashup()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    janela = PlayerMashupModerno()
    janela.show()
    sys.exit(app.exec())