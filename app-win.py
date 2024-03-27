#!/usr/bin/env python3
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from fb_view import MasterWidget
from fb import getSubDirs

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setMinimumSize(1000, 600)
    self.setWindowTitle("Fahrtenbuch")
    masterWidget = MasterWidget()
    self.setCentralWidget(masterWidget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()