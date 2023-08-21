import PyQt5.QtWidgets as W

def layoutBillingList(database):
 lw = W.QListWidget()
 lw.setMaximumSize(300, 800)
 for x in database: 
  lw.addItem(x.name)
 lw.currentRowChanged.connect(lambda x: print(f'item {x}'))
 
 layout = W.QVBoxLayout()
 layout.addWidget(W.QLabel('Anrechnungen:'))
 layout.addWidget(lw)
 return layout

def layoutBilling():
 layout = W.QVBoxLayout()
 button = W.QPushButton("Mid!")
 button.setCheckable(True)
 button.clicked.connect(lambda : print("Mid!"))
 layout.addWidget(button)
 return layout
 
def layoutResult():
 layout = W.QVBoxLayout()
 button = W.QPushButton("Right!")
 button.setCheckable(True)
 button.clicked.connect(lambda : print("Right!"))
 layout.addWidget(button)
 return layout
 
def createFBWidget(parent) :
 layout = W.QHBoxLayout()
 layout.addLayout(layoutBillingList(parent.database))
 layout.addLayout(layoutBilling())
 layout.addLayout(layoutResult())

 mainW = W.QWidget(parent)
 mainW.setLayout(layout)
 return mainW