import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from fb_view import MasterWidget
from fb import getBillingPathes

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setMinimumSize(800, 500)
    self.setWindowTitle("Fahrtenbuch")
    masterWidget = MasterWidget(getBillingPathes())
    self.setCentralWidget(masterWidget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()