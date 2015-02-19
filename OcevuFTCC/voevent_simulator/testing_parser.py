


fi = 'D:\\shared\\voevents_received\\saved\\aburlacu_aburlacu#grb.xml'

from lxml import etree

import voeventparse


tree=etree.parse(fi)

    
root = tree.getroot()

for child in tree.iter():
    print(child.tag , child.attrib, child.text)
    


