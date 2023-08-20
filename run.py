#!/usr/bin/env python3
from fb import Billing

bb = Billing().load('../billing_db/Abrechnung am 05-07-2023')
print(bb.writeTrips()+'\n')
print(bb.writeBills()+'\n')
bb.store('../tmp')
