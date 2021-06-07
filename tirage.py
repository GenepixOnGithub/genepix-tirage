# -*- coding: utf-8 -*-
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt,QTimer
import json
import random
from time import sleep

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.runs = 0
        self.setWindowTitle("Genepix tirage au sort")
        # self.setGeometry(0, 0, 1920, 1080)
        self.setStyleSheet("background-color: #222")
        self.init_widgets()
        self.showMaximized()
        self.run()

    def init_widgets(self):
        # creation du layout
        self.lay_main = QVBoxLayout()
        self.lay_main.setAlignment(Qt.AlignCenter)
        self.lay_grid = QGridLayout()
        self.lay_main.addLayout(self.lay_grid)
        # assignation du layout a la fenetre
        self.setLayout(self.lay_main)

    def run(self):
        self.runs = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tirage)
        self.timer.setInterval(200)
        self.timer.start()

    def tirage(self):
        self.runs += 1
        # Opening JSON file
        f = open('winners.json', encoding="utf8")
        raw_finishers = json.load(f)

        finishers = [f for f in raw_finishers if f['pseudo'] != '']
        row = 0
        col = 0
        random_index = random.randint(0, len(finishers))
        for i, finisher in enumerate(finishers):
            # creation du label
            lbl_pseudo = QLabel()
            lbl_pseudo.setAlignment(Qt.AlignCenter)
            if i == random_index:
                bgcolor = "#ff3c00"
                addcss = ""
            else:
                r = random.randint(0, 155)
                bgcolor = f"rgb({r}, 207, 0)"
                addcss = ""
            lbl_pseudo.setStyleSheet(f"background-color: {bgcolor}; padding-top: 22px; padding-bottom: 22px; width: 146px; font-weight: bold; font-size: 22px; color: #fff; {addcss}")
            lbl_pseudo.setText(finisher['pseudo'][:12])
            # ajout du label dans le layout
            self.lay_grid.addWidget(lbl_pseudo, row, col)
            col += 1
            if col == 22:
                col = 0
                row += 1
        self.repaint()
        f.close()     
        if self.runs == 15:
            self.timer.stop()   


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    # Run the main Qt loop
    sys.exit(app.exec())