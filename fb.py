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
  def __init__(self, name = ''): self.name = name
  def __str__(self): return str(self.name)
  def __eq__(self, other): return str(self.name) == str(other.name)

  def valid(self): return len(self.name) > 0
  def write(self): return str(self.name)
 
class Trip():
  ''' Trip class manages trip data [start,end] of a driver'''
  def __init__(self, start=0, end=0, driver='' ): self.start = int(start); self.end=int(end); self.driver = Driver(driver);
  def __str__(self): return f'Driver {self.driver}: from {self.start} to {self.end}'
  def __eq__(self, other): return (self.start, self.end, self.driver) == (other.start, other.end, other.driver)

  def valid(self): return self.end > self.end and self.driver.valid()
  def dist(self): return max(0,self.end - self.start)
  def write(self): return '\t'.join([str(self.start), str(self.end), str(self.driver)])
  def read(self, serial) : self = readTrip(serial); return self
 
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
  def __init__(self, name=''): self.name = name; self.bills = []; self.trips = []; self.insurance = 0.05;
  def __str__(self): return f'Billing "{self.name}"'

  def appendTrip(self, trip): self.trips.append(trip)  
  def appendBill(self, bill): self.bills.append(bill)  
  def clear(self) : self.trips=[]; self.bills= []
  def writeTrips(self): return '\n'.join(map(lambda t: t.write(), self.trips)) 
  def writeBills(self): return '\n'.join(map(lambda b: b.write(), self.bills)) 

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
    ''' collects a driver from bills and trips'''
    r = []
    [r.append(x.driver) for x in self.trips if x.driver not in r ]
    [r.append(x.driver) for x in self.bills if x.driver not in r ]
    return r
 
  def report(self):
    ''' compiles a report to a string'''
    maintainRate = 0.07
    totalTrips = sum(x.dist() for x in self.trips) 
    totalBills = sum(x.amount for x in self.bills) 
    totalMaintain = totalTrips * maintainRate
    total = totalMaintain + totalBills
    s = f'----------------- {Path(self.name).name} -----------------------\n'
    s += f'Reisen gesamt:  {totalTrips}km\n'
    s += f'Tanken gesamt:  {totalBills}€\n'
    s += f'Nebenkosten  :  {round(totalMaintain,2)}€\n'
    s += f'Kosten gesamt:  {round(total,2)}€\n'
    if totalTrips ==0: return s
    s += f'Quote (R):  {round(100*totalBills/totalTrips,2)} ct/km\n'
    s += f'Quote (T):  {round(100*total/totalTrips,2)} ct/km\n'
    s += f'Nebenkosten:  {round(maintainRate,2)} €/km\n'
    for drv in self.allDriver():
      dBill = sum(x.amount for x in self.bills if x.driver==drv) 
      dRatio = sum(x.dist() for x in self.trips if x.driver==drv)/totalTrips
      dTotal = dRatio*total
      s += f'-------------------------------\n'
      s += f'Fahrer: {str(drv)}\n'
      s += f'Strecke = {round(dRatio*totalTrips,2)} km\n'
      s += f'Quote = {round(dRatio,2)}\n'
      s += f'Anteil = {round(dTotal,2)}€\n'
      s += f'Bezahlt = {round(dBill,2)}€\n'
      s += f'Rest = {round(dTotal-dBill,2)}€\n'
    return s
