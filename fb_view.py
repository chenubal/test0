import PySide6.QtWidgets as W
import os
from fb import Billing ,Trip, Driver, getBillingPathes, getDBPath 
from datetime import datetime 
from pathlib import Path
import shutil

def makeSpinBox(data,i):
  spinbox = W.QSpinBox()
  spinbox.setRange(0,10000000)
  spinbox.setValue(data[i])
  def g(n): data[i]=n
  spinbox.valueChanged.connect(g)
  return spinbox

def makeComboBox(data,i,labels):
  comboBox = W.QComboBox()
  comboBox.addItems(labels) 
  comboBox.setCurrentIndex(data[i])
  def g(n): data[i]=n
  comboBox.currentIndexChanged.connect(g)
  return comboBox

def tripEditor(trip):
  users = ['Jannis','Luis','Josef']
  userIndex = users.index(str(trip.driver))
  data = [trip.start, trip.end, max(0,userIndex)]

  btn = W.QPushButton('Ok')

  hbox = W.QHBoxLayout()
  hbox.addWidget(makeSpinBox(data,0))
  hbox.addWidget(makeSpinBox(data,1))
  hbox.addWidget(makeComboBox(data,2,users))
  hbox.addWidget(btn)

  dialog = W.QDialog()
  dialog.setMinimumSize(300,30)
  dialog.setModal(True)
  dialog.setLayout(hbox)
  btn.clicked.connect(dialog.accept)

  if dialog.exec()==1:
    trip.start = data[0]
    trip.end = data[1]
    trip.driver = Driver(users[data[2]])
    return True
  return False

class Pathes_Widget(W.QWidget):
  def __init__(self, follower):
    super().__init__()
    self.pathes = getBillingPathes()
    self.lw = self.makePathWidgets(follower)
  
    vbox = W.QVBoxLayout()
    vbox.addWidget(W.QLabel('Abrechnungen:'))
    vbox.addWidget(self.lw) 
    vbox.addLayout(self.makeButtonBox())
    self.setLayout(vbox)
 
    self.update()

  def makeButtonBox(self):
    addButton = W.QPushButton('Neu')
    def addBilling():
      path = getDBPath()
      if path.is_dir():
        now = datetime.now().strftime('%d-%m-%Y')
        pathStr = str(path.absolute()) +f'/Abrechnung am {now}'
        if not Path(pathStr).exists(): 
          os.mkdir(pathStr) 
          Billing().store(pathStr)
          self.pathes = getBillingPathes()
          self.update()
    addButton.clicked.connect(addBilling)
   
    delButton = W.QPushButton('Löschen')
    def delBilling():
      row = self.lw.currentRow()
      if 0 <= row < len(self.pathes):
        msgBox = W.QMessageBox
        if msgBox.question(self,'', "Wirklich löschen?", msgBox.Yes | msgBox.No)== msgBox.Yes:
          path = self.pathes[row]
          shutil.rmtree(str(path.absolute()), ignore_errors=True)
          self.pathes = getBillingPathes()
          self.update()
    delButton.clicked.connect(delBilling)
   
    hbox = W.QHBoxLayout()
    hbox.addWidget(addButton)
    hbox.addWidget(delButton)
    return hbox
   
  def makePathWidgets(self,follower):
    listWidget = W.QListWidget()
    sendPath = lambda i: follower.update(str(self.pathes[i].absolute()))
    listWidget.currentRowChanged.connect(sendPath)
    return listWidget
 
  def update(self):
     self.lw.clear()
     for p in self.pathes: self.lw.addItem(p.name)
     n = len(self.pathes)
     if n > 0: self.lw.setCurrentRow(n-1)
 
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
    vbox.addWidget(W.QLabel("Rechnungen:"))
    vbox.addWidget(self.billTable)
    vbox.addWidget(W.QLabel("Fahrten:"))
    vbox.addWidget(self.tripTable)
    vbox.addLayout(self.makeTripButtonBox())
    self.setLayout(vbox)

  def updateTripTable(self):
    rB = self.billing
    numTrips = len(rB.trips)
    rT = self.tripTable
    rT.clearContents()
    rT.setRowCount(numTrips)
    setCellWidget = lambda i,j,s: rT.setCellWidget(i,j, W.QLabel(s))
    for index,trip in zip(range(numTrips),rB.trips):
      setCellWidget(index,0, f'{trip.start}')
      setCellWidget(index,1, f'{trip.end}')
      setCellWidget(index,2, f'{trip.driver}')
    rT.horizontalHeader().setSectionResizeMode(W.QHeaderView.Stretch)
    self.follower.update(rB)
  
  def makeTripButtonBox(self):
    hbox = W.QHBoxLayout()
    addButton = W.QPushButton('Neue Fahrt')
    def addTrip() :
      rB = self.billing
      trip = Trip(0,20,'Josef')
      if len(rB.trips) > 0:
        trip0 = rB.trips[-1]
        trip = Trip(trip0.end, trip0.start+15,trip0.driver)
      if tripEditor(trip):
        rB.trips.append(trip)
        self.updateTripTable()
        rB.store(rB.name)
    addButton.clicked.connect(addTrip)
    delButton = W.QPushButton('Letzte löschen')
    def delTrip():
      refB = self.billing
      if len(refB.trips) > 0:  
        refB.trips.pop()
        self.updateTripTable()
        refB.store(refB.name)
    delButton.clicked.connect(delTrip)
    hbox.addWidget(addButton)
    hbox.addWidget(delButton)
    return hbox

  def updateBillTable(self):
    rB = self.billing
    rT = self.billTable
    numBills = len(rB.bills)
    rT.clearContents()
    rT.setRowCount(numBills)
    setCellWidget = lambda n,m,s: rT.setCellWidget(n,m, W.QLabel(s))
    for index,bill in zip(range(numBills), rB.bills):
      setCellWidget(index,0, f'{bill.amount}€')
      setCellWidget(index,1, f'{bill.driver}')
    rT.horizontalHeader().setSectionResizeMode(W.QHeaderView.Stretch)

  def update(self, path):
    rB = self.billing
    rB.load(path)
    self.updateBillTable()
    self.updateTripTable()
    rB.name = str(path)
    self.follower.update(rB)

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
  def __init__(self):
    super().__init__()
    reportWidget = ReportWidget()
    billingWidget = Billing_Widget(reportWidget)
    pathesWidget = Pathes_Widget(billingWidget)
    hbox = W.QHBoxLayout()
    hbox.addWidget(pathesWidget)
    hbox.addWidget(billingWidget)
    hbox.addWidget(reportWidget)
    hbox.addStretch()
    self.setLayout(hbox)
 