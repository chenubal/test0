from functools import reduce

class Driver():
 def __init__(self, name = ''): self.name = name
 def __str__(self): return str(self.name)
 def __eq__(self, other): return self.name == other.name
 def valid(self): return len(self.name) > 0
 def write(self): return str(self.name)
 
class Trip():
 def __init__(self, start, end, driver ): self.start = start; self.end=end; self.driver = driver;
 def __str__(self): return f'Driver {self.driver}: from {self.start} to {self.end}'
 def valid(self): return self.end > self.end and self.driver.valid()
 def dist(self): return max(0,self.end - self.end)
 def write(self): return f'{self.start}\t{self.end}\t{self.driver}' 
 
class Bill():
 def __init__(self, amount, driver ): self.amount = amount; self.driver = driver;
 def __str__(self): return f'Driver {self.driver}: amount = {self.amount}€'
 def valid(self): return self.amount > 0 and self.driver.valid()
 def write(self): return f'{self.amount}\t{self.driver}'
 
class Billing():
 def __init__(self, name=''): self.name = name; self.bills = []; self.trips = []; self.insurance = 0.05;
 def __str__(self): return f'Billing "{self.name}"'
 def appendTrip(self, trip): self.trips.append(trip)  
 def appendBill(self, bill): self.bills.append(bill)  
 def valid(self): return true;
 def writeTrips(self): return reduce(lambda s,x: str(s) + x.write()+'\n', self.trips,'').strip() 
 def writeBills(self): return reduce(lambda s,x: str(s) + x.write()+'\n', self.bills,'').strip() 

