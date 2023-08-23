import PySide6 .QtWidgets as W
from fb import Billing  

class Pathes_Widget(W.QWidget):
  def __init__(self, pathes, follower):
    super().__init__()
    self.pathes = pathes
    self.lw = self.makeWidgets()
    self.makeConnection(follower)
    self.fillList()
 
    vbox = W.QVBoxLayout()
    vbox.addWidget(W.QLabel('Abrechnungen:'))
    vbox.addWidget(self.lw) 
    self.setLayout(vbox)
    
  def makeConnection(self,follower):
    sendPath = lambda i: follower.update(str(self.pathes[i].absolute()))
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
    self.tripTable.setHorizontalHeaderLabels(['Start(km)','Ende(km)','Fahrer'])

    vbox = W.QVBoxLayout()
    vbox.addWidget( W.QLabel("Rechnungen:"))
    vbox.addWidget( self.billTable)
    vbox.addWidget( W.QLabel("Fahrten:"))
    vbox.addWidget( self.tripTable)
    self.setLayout(vbox)

  def makeTripTable(self):
    n = len(self.billing.trips)
    self.tripTable.clearContents()
    self.tripTable.setRowCount(n)
    setCellWidget = lambda n,m,s: self.tripTable.setCellWidget(n,m, W.QLabel(s))
    for [i,t] in zip(range(n),self.billing.trips):
      setCellWidget(i,0, f'{t.start}')
      setCellWidget(i,1, f'{t.end}')
      setCellWidget(i,2, f'{t.driver}')
    self.tripTable.horizontalHeader().setSectionResizeMode(W.QHeaderView.Stretch)

  def makeBillTable(self):
    n = len(self.billing.bills)
    self.billTable.clearContents()
    self.billTable.setRowCount(n)
    setCellWidget = lambda n,m,s: self.billTable.setCellWidget(n,m, W.QLabel(s))
    for [i,b] in zip(range(n), self.billing.bills):
      setCellWidget(i,0, f'{b.amount}€')
      setCellWidget(i,1, f'{b.driver}')
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
 