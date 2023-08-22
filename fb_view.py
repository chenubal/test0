import PyQt5.QtWidgets as W

def layoutBillingList(model):
  listwidget = W.QListWidget()
  listwidget.setMaximumSize(300, 800)
  for x in model.pathes: 
    listwidget.addItem(x.name)
  listwidget.currentRowChanged.connect(model.select)
  if len(model.pathes) > 0: listwidget.setCurrentRow(0)
 
  vbox = W.QVBoxLayout()
  vbox.addWidget(W.QLabel('Anrechnungen:'))
  vbox.addWidget(listwidget)
  return vbox

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
    hbox.addLayout(layoutBillingList(model))
    hbox.addLayout(layoutBilling())
    hbox.addLayout(layoutResult())
    self.setLayout(hbox)
 