class Driver():
 def __init__(self, name = ''): self.name = name
 def __str__(self): return str(self.name)
 def __eq__(self, other): return self.name == other.name
 def valid(self): return len(self.name) > 0
 
class Trip():
 def __init__(self, start, end, driver ): self.start = start; self.end=end; self.driver = driver;
 def __str__(self): return f'Driver {self.driver}: from {self.start} to {self.end}'
 def valid(self): return self.end > self.end and self.driver.valid()
 def dist(self): return max(0,self.end - self.end)
 
class Bill():
 def __init__(self, amount, driver ): self.amount = amount; self.driver = driver;
 def __str__(self): return f'Driver {self.driver}: amount = {self.amount}€'
 def valid(self): return self.amount > 0 and self.driver.valid()
 