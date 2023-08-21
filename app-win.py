import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from fb_view import createFBWidget

class MainWindow(QMainWindow):
 def __init__(self):
  super().__init__()
  self.setWindowTitle("Fartenbuch")
  self.setCentralWidget(createFBWidget(self))

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()