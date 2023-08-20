#!/usr/bin/env python3
from fb import Driver, Trip, Bill, Billing

print(Driver('Josef'));
print('cmp drivers: ' + str(Driver('Josef')==Driver('Josef2')))
print('cmp drivers: ' + str(Driver('Heers')==Driver('Heers')))
print('validate default: ' + str(Driver().valid()))
print('validate empty: ' + str(Driver('').valid()))
print('validate not empty: ' + str(Driver('a').valid()))
print(Trip(10,100,Driver('Jannis')).write())
print(Bill(33.44,Driver('Jannis')).write())
b = Billing('Test') 
b.appendTrip(Trip(0,100,Driver('Josef')))
b.appendTrip(Trip(100,110,Driver('Janns')))
print(b.writeTrips())