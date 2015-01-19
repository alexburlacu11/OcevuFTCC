
import sys
import os

from request import REQUEST


r = REQUEST()

r.set_OWNER("alex")
a = r.get_OWNER()
print a

r.set_REQUEST_ID(1)
a = r.get_REQUEST_ID()
print a

outfilename = 'q.xml'
outfile = open(outfilename, 'w')

with open (outfilename, "w") as m:
    r.export(m, 1)

