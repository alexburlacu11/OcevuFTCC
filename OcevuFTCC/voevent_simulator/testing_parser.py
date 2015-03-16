


fi = 'D:\\shared\\voevents_received\\saved\\nasa.gsfc.gcn_SWIFT#BAT_GRB_Pos_532871-729.xml'

from lxml import etree



tree=etree.parse(fi)

    
root = tree.getroot()

# print(data)

ivorn = root.xpath('//@ivorn')
role = root.xpath('//@role')
version = root.xpath('//@version')

authorIVORN = root.xpath('//Who/AuthorIVORN/text()')
date = root.xpath('//Who/Date/text()')
author = root.xpath('//Who/Author/*/text()')
description = root.xpath('//Who/Description/text()')

where_when_description = root.xpath('//WhereWhen/Description/text()')
observation_location_astroCoordSystem = root.xpath('//WhereWhen/ObsDataLocation/ObservationLocation/*/@*')
observation_location_astroCoords = root.xpath('//WhereWhen/ObsDataLocation/ObservationLocation/*/*/*/*/text()')
observatory_location_astroCoordSystem = root.xpath('//WhereWhen/ObsDataLocation/ObservatoryLocation/@*')
observatory_location_astroCoords = root.xpath('//WhereWhen/ObsDataLocation/ObservatoryLocation/*/*/*/*/text()')

why = root.xpath('//Why/*/*/text()')
how = root.xpath('//How/*/text()')
what = root.xpath('//What')

print(str(ivorn[0]))
print(str(role[0]))
print(str(version[0]))
print(str(authorIVORN[0]))
print(str(date[0]))
print(str(author))
print(str(description[0]))
print(str(where_when_description[0]))
print(str(observation_location_astroCoordSystem))
print(str(observation_location_astroCoords))
print(str(observatory_location_astroCoordSystem))
print(str(observatory_location_astroCoords))
print(str(why))
print(str(how))
print(str(what))

what = root.xpath('//What')[0]
info = ''      
for child in what.iter():
    info += str(child.tag) +": "+str(child.attrib)+": "+str(child.text)+"<br>"
    
print(info)
            
            
            
            








# for r in res:
#     print(r)
    
# for e in root.iterchildren():
#     data += "<b>"+e.tag +"</b><br>"
#     for i in e.getchildren():
#         print(etree.tostring(i))
    





# for child in tree.iter():
#     print(child.tag , child.attrib, child.text)
    


