from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout

def layoutBillingList():
 layout = QVBoxLayout()
 button = QPushButton("Left!")
 button.setCheckable(True)
 button.clicked.connect(lambda : print("Left!"))
 layout.addWidget(button)
 return layout

def layoutBilling():
 layout = QVBoxLayout()
 button = QPushButton("Mid!")
 button.setCheckable(True)
 button.clicked.connect(lambda : print("Mid!"))
 layout.addWidget(button)
 return layout
 
def layoutResult():
 layout = QVBoxLayout()
 button = QPushButton("Right!")
 button.setCheckable(True)
 button.clicked.connect(lambda : print("Right!"))
 layout.addWidget(button)
 return layout
 
def createFBWidget(parent) :
 layout = QHBoxLayout()
 layout.addLayout(layoutBillingList())
 layout.addLayout(layoutBilling())
 layout.addLayout(layoutResult())

 mainW = QWidget(parent)
 mainW.setLayout(layout)
 return mainW