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
  def dist(self): return max(0,self.end - self.end)
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
  def appendBill(self, bill): 
    self.bills.append(bill)  
    print(bill)
  def clear(self) : self.trips=[]; self.bills= [];
  def writeTrips(self): return '\n'.join(map(lambda t: t.write(), self.trips)) 
  def writeBills(self): return '\n'.join(map(lambda b: b.write(), self.bills)) 
  def load(self, dir):
    self.clear()
    loadFile(dir + '\\bills.txt',lambda s: self.appendBill(readBill(s)) )
    loadFile(dir + '\\trips.txt',lambda s: self.appendTrip(readTrip(s)) )
    return self
 
  def store(self, dir):
    storeFile(dir + '/bills.txt',self.writeBills()) 
    storeFile(dir + '/trips.txt',self.writeTrips()) 
 
def loadFile(fname, f):
  if os.path.exists(fname):
    for s in open(fname,'r') : f(s)

def storeFile(fname, data): open(fname,'w').write(data)

def getBillingPathes(path = './billing_db' ):
  p = Path(path)
  return [x for x in p.iterdir() if x.is_dir()]

  
