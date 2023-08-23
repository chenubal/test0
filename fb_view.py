import PySide6 .QtWidgets as W

class Pathes_Widget(W.QWidget):
  def __init__(self, model):
    super().__init__()
    self.m = model
    self.lw = self.makeWidgets(self.m)
    self.fillList()
 
    vbox = W.QVBoxLayout()
    vbox.addWidget(W.QLabel('Abrechnungen:'))
    vbox.addWidget(self.lw) 
    self.setLayout(vbox)
    
  def makeWidgets(self,model):
    lw = W.QListWidget()
    lw.setMaximumSize(300, 800)
    lw.currentRowChanged.connect(model.select)
    return lw
 
  def fillList(self):
     self.lw.clear()
     for p in self.m.pathes: self.lw.addItem(p.name)
     if len(self.m.pathes) > 0: self.lw.setCurrentRow(0)
 
def layoutBilling():
  button = W.QPushButton("Mid!")
  button.setCheckable(True)
  button.clicked.connect(lambda : print("Mid!"))

  vbox = W.QVBoxLayout()
  vbox.addWidget(button)
  return vbox
 
def layoutResult():
  button = W.QPushButton("Right!")
  button.setCheckable(True)
  button.clicked.connect(lambda : print("Right!"))

  vbox = W.QVBoxLayout()
  vbox.addWidget(button)
  return vbox
 
class BillingDB_Widget(W.QWidget):
  def __init__(self, model):
    super().__init__()
    hbox = W.QHBoxLayout()
    hbox.addWidget(Pathes_Widget(model))
    hbox.addLayout(layoutBilling())
    hbox.addLayout(layoutResult())
    self.setLayout(hbox)
 