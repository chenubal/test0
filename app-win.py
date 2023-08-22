import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from fb_view import BillingDB_Widget
from fb import getBillingPathes, Billing

class BillingDB():
  def __init__(self):
    self.pathes = getBillingPathes()
    self.selected = -1

  def select(self, i) : self.selected = i; self.load()
  
  def load(self):
    i = self.selected
    if i >= 0:
      b = Billing().load(str(self.pathes[i].absolute()))
      print(b.writeTrips())
      return b
  

class BillingDB_View(QMainWindow):
  def __init__(self, billingDB):
    super().__init__()
    self.setMinimumSize(800, 500)
    self.model = billingDB
    self.setWindowTitle("Fartenbuch")
    self.setCentralWidget(BillingDB_Widget(self.model))

app = QApplication(sys.argv)
database = BillingDB()
window = BillingDB_View(database)
window.show()
app.exec()