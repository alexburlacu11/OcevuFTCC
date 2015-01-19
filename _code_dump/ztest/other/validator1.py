from lxml import etree




v11 = "/home/ros/voevent/v11.xml"
v20 = "/home/ros/voevent/v20.xml"


xsd_11 = "/home/ros/voevent/VOEvent-v1.1.xsd"
xsd_20 = "/home/ros/voevent/VOEvent-v2.0.xsd"


def validate(xmlparser, xmlfilename):
    try:
        with open(xmlfilename, 'r') as f:
            etree.fromstring(f.read(), xmlparser) 
        return True
    except etree.DocumentInvalid as e:                                     
        print e                                                                 
        return False

with open(xsd_11, 'r') as f:
    schema_root = etree.XML(f.read())

schema1 = etree.XMLSchema(schema_root)
xmlparser = etree.XMLParser(schema=schema1)

filenames = [v11]
for filename in filenames:
    if validate(xmlparser, filename):
        print "%s validates" % filename
    else:
        print "%s doesn't validate" % filename