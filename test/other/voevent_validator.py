from lxml import etree




f1 = "/home/ros/voevent/voeventex.xml"
f2 = "/home/ros/voevent/one.xml"

xsd_filename = "/home/ros/voevent/VOEvent-v2.0.xsd"



def validate(xmlparser, xmlfilename):
    try:
        with open(xmlfilename, 'r') as f:
            etree.fromstring(f.read(), xmlparser) 
        return True
    except:
        return False

with open(xsd_filename, 'r') as f:
    schema_root = etree.XML(f.read())

schema1 = etree.XMLSchema(schema_root)
xmlparser = etree.XMLParser(schema=schema1)

filenames = [f1, f2]
for filename in filenames:
    if validate(xmlparser, filename):
        print "%s validates" % filename
    else:
        print "%s doesn't validate" % filename