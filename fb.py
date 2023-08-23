from pathlib import Path
import os

class Driver():
  ''' Driver class holds a drivers name'''
  def __init__(self, name = ''): self.name = name
  def __str__(self): return str(self.name)
  def __eq__(self, other): return self.name == other.name
  def valid(self): return len(self.name) > 0
  def write(self): return str(self.name)
 
class Trip():
  ''' Trip class holds trip data [start,end] of a driver'''
  def __init__(self, start=0, end=0, driver='' ): self.start = int(start); self.end=int(end); self.driver = Driver(driver);
  def __str__(self): return f'Driver {self.driver}: from {self.start} to {self.end}'
  def valid(self): return self.end > self.end and self.driver.valid()
  def dist(self): return max(0,self.end - self.start)
  def write(self): return '\t'.join([str(self.start), str(self.end), str(self.driver)])
  def read(self, serial) : self = readTrip(serial); return self
 
def readTrip(serial) :
  s = '0'; e='0'; d='' 
  serial = serial.strip()
  if serial.count('\t') == 2: 
    s,e,d = serial.split('\t')
  return Trip(int(s),int(e), Driver(d))
 
class Bill():
  ''' Bill class holds bill data [amount] of a driver'''
  def __init__(self, amount=0, driver='' ): self.amount = float(amount); self.driver = Driver(driver);
  def __str__(self): return f'Driver {self.driver}: amount = {self.amount}€'
  def valid(self): return self.amount > 0 and self.driver.valid()
  def write(self): return '\t'.join([str(self.amount), str(self.driver)])
  def read(self, serial) : self = readBill(serial); return self

def readBill(serial) : 
  a = '0'; d='' 
  if serial.count('\t') == 1: 
    a,d = serial.strip().split('\t')
  return Bill(float(a), Driver(d))
  
class Billing():
  ''' Billing class holds bills and trips'''
  def __init__(self, name=''): self.name = name; self.bills = []; self.trips = []; self.insurance = 0.05;
  def __str__(self): return f'Billing "{self.name}"'
  def appendTrip(self, trip): self.trips.append(trip)  
  def appendBill(self, bill): self.bills.append(bill)  
  def clear(self) : self.trips=[]; self.bills= []
  def writeTrips(self): return '\n'.join(map(lambda t: t.write(), self.trips)) 
  def writeBills(self): return '\n'.join(map(lambda b: b.write(), self.bills)) 

  def load(self, dir):
    self.clear()
    loadFile(dir + '\\bills.txt',lambda s: self.appendBill(readBill(s)) )
    loadFile(dir + '\\trips.txt',lambda s: self.appendTrip(readTrip(s)) )
    self.name = Path(dir).name
    return self
 
  def store(self, dir):
    storeFile(dir + '/bills.txt',self.writeBills()) 
    storeFile(dir + '/trips.txt',self.writeTrips()) 

  def allDriver(self):
    result = []
    for trip in self.trips: 
      if not result.count(trip.driver) : result.append(trip.driver)
    for bill in self.bills: 
      if not result.count(bill.driver) : result.append(bill.driver)
    return result
  
  def dtrip(self, driver=None):
    result = 0
    all = driver is None
    for trip in self.trips: 
      if  all or driver == trip.driver : 
        result += trip.dist()
    return result
  
  def dbill(self, driver=None):
    result = 0
    all = driver is None
    for bill in self.bills: 
      if all or driver == bill.driver: 
        result += bill.amount
    return result
 
  def report(self):
    totalTrips = self.dtrip()
    totalBills = self.dbill()
    totalEnsure = totalTrips * 0.05
    total = totalEnsure+totalBills
    s = f'----------------- {self.name} -----------------------\n'
    s += f'Reisen gesamt:  {totalTrips}km\n'
    s += f'Tanken gesamt:  {totalBills}€\n'
    s += f'Versich. gesamt:  {totalEnsure}€\n'
    s += f'Kosten gesamt:  {total}€\n'
    s += f'Quote (R):  {round(100*totalBills/totalTrips,2)} ct/km\n'
    s += f'Quote (T):  {round(100*total/totalTrips,2)} ct/km\n'
    s += f'Vesicherung:  5.00 ct/km\n'
    for drv in self.allDriver():
      dBill = self.dbill(drv)
      dRatio = self.dtrip(drv)/totalTrips
      dTotal = dRatio*total
      s += f'-------------------------------\n'
      s += f'Fahrer: {str(drv)}\n'
      s += f'Quote = {round(dRatio,2)}\n'
      s += f'Anteil = {round(dTotal,2)}€\n'
      s += f'Bezahlt = {round(dBill,2)}€\n'
      s += f'Rest = {round(dTotal-dBill,2)}€\n'
    return s
 
def loadFile(fname, f):
  if os.path.exists(fname):
    for s in open(fname,'r') : f(s)

def storeFile(fname, data): open(fname,'w').write(data)

def getBillingPathes(path = './billing_db' ):
  p = Path(path)
  return [x for x in p.iterdir() if x.is_dir()]

  
