import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QObject, Signal, Slot    
from fb_view import BillingDB_Widget
from fb import getBillingPathes, Billing

class BillingDB(QObject):
 
  selSignal = Signal(int)
 
  def __init__(self, parent=None):
    super().__init__(parent)
    self.pathes = getBillingPathes()
    self.selected = -1
    self.selSignal.connect(lambda i: self.load())
  
  def select(self, i) : 
    if 0 <= i < len(self.pathes):
      self.selected = i
      self.selSignal.emit(self.selected)
  
  def load(self):
    i = self.selected
    if 0 <= i < len(self.pathes):
      b = Billing().load(str(self.pathes[i].absolute()))
      print(b.writeTrips())
      return b  

class MainWindow(QMainWindow):
  def __init__(self, billingDB):
    super().__init__()
    self.setMinimumSize(800, 500)
    self.model = billingDB
    self.setWindowTitle("Fartenbuch")
    self.setCentralWidget(BillingDB_Widget(self.model))

app = QApplication(sys.argv)
window = MainWindow(BillingDB())
window.show()
app.exec()