import PySide6 .QtWidgets as W
from PySide6.QtCore import QObject, Signal, Slot  
from fb import Billing  

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
    return lw
 
  def fillList(self):
     self.lw.clear()
     for p in self.pathes: self.lw.addItem(p.name)
     if len(self.pathes) > 0: self.lw.setCurrentRow(0)
 
class Billing_Widget(W.QWidget):
  def __init__(self, follower):
    super().__init__()
    self.setMinimumWidth(500)
    self.billing = Billing()
    self.follower = follower
 
    self.billTable = W.QTableWidget()
    self.billTable.setColumnCount(2)
    self.billTable.setHorizontalHeaderLabels(['Summe','Fahrer' ])

    self.tripTable = W.QTableWidget()
    self.tripTable.setColumnCount(3)
    self.tripTable.setHorizontalHeaderLabels(['Start','Ende','Fahrer'])

    vbox = W.QVBoxLayout()
    vbox.addWidget( W.QLabel("Rechnungen:"))
    vbox.addWidget( self.billTable)
    vbox.addWidget( W.QLabel("Fahrten:"))
    vbox.addWidget( self.tripTable)
    self.setLayout(vbox)

  def makeTripTable(self):
    self.tripTable.clearContents()
    self.tripTable.setRowCount(len(self.billing.trips))
    i = 0
    for x in self.billing.trips:
      self.tripTable.setCellWidget(i,0, W.QLabel(f'km {x.start}'))
      self.tripTable.setCellWidget(i,1, W.QLabel(f'km {x.end}'))
      self.tripTable.setCellWidget(i,2, W.QLabel(f'{x.driver}'))
      i = i+1
    self.tripTable.horizontalHeader().setSectionResizeMode(W.QHeaderView.Stretch)

  def makeBillTable(self):
    self.billTable.clearContents()
    self.billTable.setRowCount(len(self.billing.bills))
    i = 0
    for x in self.billing.bills:
      self.billTable.setCellWidget(i,0, W.QLabel(f'{x.amount}€'))
      self.billTable.setCellWidget(i,1, W.QLabel(f'{x.driver}'))
      i = i+1
    self.billTable.horizontalHeader().setSectionResizeMode(W.QHeaderView.Stretch)

  def update(self, path):
    self.billing.load(path)
    self.makeBillTable()
    self.makeTripTable()
    self.follower.update(self.billing)

class ReportWidget(W.QWidget):
  def __init__(self):
    super().__init__()
    self.setMinimumWidth(500)
    vbox = W.QVBoxLayout()
    vbox.addWidget( W.QLabel("Zusammenfassung:"))
    self.textEdit = W.QTextEdit()
    vbox.addWidget( self.textEdit)
    self.setLayout(vbox)

  def update(self, billing):
    self.textEdit.setText(billing.report())


class MasterWidget(W.QWidget):
  def __init__(self, pathes):
    super().__init__()
    reportWidget = ReportWidget()
    billingWidget = Billing_Widget(reportWidget)
    pathesWidget = Pathes_Widget(pathes,billingWidget)
    hbox = W.QHBoxLayout()
    hbox.addWidget(pathesWidget)
    hbox.addWidget(billingWidget)
    hbox.addWidget(reportWidget)
    hbox.addStretch()
    self.setLayout(hbox)
 