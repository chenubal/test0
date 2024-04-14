from pathlib import Path
import os

def loadFile(fname, f):
  if os.path.exists(fname): 
    for s in open(fname,'r') : f(s)

def storeFile(fname, data): 
  open(fname,'w').write(data)

def getDBPath(): 
  return Path('./billing_db')

def getSubDirs(path = getDBPath() ):
  return [x for x in Path(path).iterdir() if x.is_dir()]

class Driver():
  ''' Driver class modles a driver'''
  def __init__(self, name = ''): 
    self.name = name
  def __str__(self): 
    return str(self.name)
  def __eq__(self, other): 
    return str(self.name) == str(other.name)
  def __hash__(self):
    return hash(str(self))

  def valid(self): 
    return len(self.name) > 0
  def write(self): 
    return str(self.name)
 
class Trip():
  ''' Trip class manages trip data [start,end] of a driver'''
  def __init__(self, start=0, end=0, driver='' ): 
    self.start = int(start) 
    self.end=int(end)
    self.driver = Driver(driver)
  def __str__(self): 
    return f'Driver {self.driver}: from {self.start} to {self.end}'
  def __eq__(self, other): 
    return (self.start, self.end, self.driver) == (other.start, other.end, other.driver)
  def valid(self): 
    return self.end > self.end and self.driver.valid()
  def dist(self): 
    return max(0,self.end - self.start)
  def write(self): 
    return '\t'.join([str(self.start), str(self.end), str(self.driver)])
  def read(self, serial) : 
    self = readTrip(serial); 
    return self
 
def readTrip(serial) :
  ''' returns a Trip object from a serial string'''
  s = '0'; e='0'; d='' 
  serial = serial.strip()
  if serial.count('\t') == 2: 
    s,e,d = serial.split('\t')
  return Trip(int(s),int(e), Driver(d))
 
class Bill():
  ''' Bill class manages bill data [amount] of a driver'''
  def __init__(self, amount=0, driver='' ): self.amount = float(amount); self.driver = Driver(driver);
  def __str__(self): return f'Driver {self.driver}: amount = {self.amount}€'
  def __eq__(self, other): return (self.amount, self.driver) == (other.amount, other.driver)

  def valid(self): return self.amount > 0 and self.driver.valid()
  def write(self): return '\t'.join([str(self.amount), str(self.driver)])
  def read(self, serial) : self = readBill(serial); return self

def readBill(serial) : 
  ''' returns a Bill object from a serial string'''
  a = '0'; d='' 
  if serial.count('\t') == 1: 
    a,d = serial.strip().split('\t')
  return Bill(float(a), Driver(d))
  
class Billing():
  ''' Billing class manages bills and trips and gives an report'''
  def __init__(self, name=''): 
    self.name = name 
    self.bills = [] 
    self.trips = []
    self.opRate = 0.05 # operating cost €/km
  def __str__(self): return f'Billing "{self.name}"'

  def appendTrip(self, trip): self.trips.append(trip)  
  def appendBill(self, bill): self.bills.append(bill)  
  def clear(self) : self.trips=[]; self.bills= []
  def writeTrips(self): 
    return '\n'.join(map(lambda t: t.write(), self.trips)) 
  def writeBills(self): 
    return '\n'.join(map(lambda b: b.write(), self.bills)) 

  def load(self, dir):
    ''' load billing data from a folder'''
    self.clear()
    loadFile(dir + '\\bills.txt',lambda s: self.appendBill(readBill(s)) )
    loadFile(dir + '\\trips.txt',lambda s: self.appendTrip(readTrip(s)) )
    self.name = Path(dir).name
    return self
 
  def store(self, dir):
    ''' stores billing data to a folder'''
    storeFile(dir + '/bills.txt',self.writeBills()) 
    storeFile(dir + '/trips.txt',self.writeTrips()) 

  def allDriver(self):
    ''' collects all driver from bills and trips'''
    return {x.driver for x in self.trips} | {x.driver for x in self.bills}
 
  def report(self):
    ''' compiles a report to a string'''
    rnd = lambda n :f"{n:.2f}"
    maintainRate = 0.07
    totalTrips = sum(x.dist() for x in self.trips) 
    totalBills = sum(x.amount for x in self.bills) 
    totalMaintain = totalTrips * maintainRate
    totalAmount = totalMaintain + totalBills
    s = f'----------------- {Path(self.name).name} -----------------------\n'
    s += f'Reisen gesamt:  {totalTrips} km\n'
    s += f'Tanken gesamt:  {rnd(totalBills)}€\n'
    s += f'Nebenkosten  :  {rnd(totalMaintain)}€\n'
    s += f'Kosten gesamt:  {rnd(totalAmount)}€\n'
    if totalTrips ==0: return s
    s += f'Quote (R):  {rnd(100*totalBills/totalTrips)} ct/km\n'
    s += f'Quote (T):  {rnd(100*totalAmount/totalTrips)} ct/km\n'
    s += f'Nebenkosten:  {rnd(maintainRate)} €/km\n'
    for drv in self.allDriver():
      drvBill = sum(x.amount for x in self.bills if x.driver==drv) 
      drvRatio = sum(x.dist() for x in self.trips if x.driver==drv)/totalTrips
      drvAmount = drvRatio*totalAmount
      s += f'-------------------------------\n'
      s += f'Fahrer = {str(drv)}\n'
      s += f'Strecke = {round(drvRatio*totalTrips)} km\n'
      s += f'Quote = {rnd(drvRatio)}\n'
      s += f'Anteil = {rnd(drvAmount)}€\n'
      s += f'Bezahlt = {rnd(drvBill)}€\n'
      s += f'Rest = {rnd(drvAmount-drvBill)}€\n'
    return s
