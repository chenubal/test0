import PySide6 .QtWidgets as W
from PySide6.QtCore import QObject, Signal, Slot    

class Pathes_Widget(W.QWidget):
  def __init__(self, pathes, other):
    super().__init__()
    self.pathes = pathes
    self.lw = self.makeWidgets()
    self.makeConnection(other)
    self.fillList()
 
    vbox = W.QVBoxLayout()
    vbox.addWidget(W.QLabel('Abrechnungen:'))
    vbox.addWidget(self.lw) 
    self.setLayout(vbox)
    
  def makeConnection(self,other):
    sendPath = lambda i: other.update(str(self.pathes[i].absolute()))
    self.lw.currentRowChanged.connect(sendPath)
    
  def makeWidgets(self):
    lw = W.QListWidget()
    lw.setMaximumSize(300, 800)
    return lw
 
  def fillList(self):
     self.lw.clear()
     for p in self.pathes:
       self.lw.addItem(p.name)
     if len(self.pathes) > 0: 
       self.lw.setCurrentRow(0)
 
class Billing_Widget(W.QWidget):
  def __init__(self):
    super().__init__()
    button = W.QPushButton("Mid!")
    button.setCheckable(True)
    button.clicked.connect(lambda : print("Mid!"))

    vbox = W.QVBoxLayout()
    vbox.addWidget(button)
    self.setLayout(vbox)

  def update(self, path):
    print(path)
 
class MasterWidget(W.QWidget):
   def __init__(self, pathes):
    super().__init__()
    billingWidget = Billing_Widget()
    pathesWidget = Pathes_Widget(pathes,billingWidget)
 

    hbox = W.QHBoxLayout()
    hbox.addWidget(pathesWidget)
    hbox.addWidget(billingWidget)
    self.setLayout(hbox)
 