import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from fb_view import createFBWidget
from fb import loadDatabase, Billing

class Model():
 def __init__(self):
  self.database = loadDatabase()
  self.billing = Billing()

 def loadBilling(self, i):
   self.billing.load(str(self.database[i].absolute()))
   print(self.billing.writeTrips())
  

class MainWindow(QMainWindow):
 def __init__(self):
  super().__init__()
  self.setMinimumSize(800, 500)
  self.model = Model()
  self.setWindowTitle("Fartenbuch")
  self.setCentralWidget(createFBWidget(self,self.model))

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()