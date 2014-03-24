#! /usr/bin/python                                                              
# -*- coding: utf-8 -*-                                                         
#                                                                               
# Simple XML validator done while learning the use of lxml library.             
#   -- Juhamatti Niemelä <iiska AT iki DOT fi>                                  
                                                                                
import lxml                                                                     
from lxml import etree                                                          
                                                                                
if __name__ == "__main__":                                                      
    import sys, os        
    
    v11 = "/home/ros/voevent/v11.xml"
    v11_2 = "/home/ros/voevent/v11_2.xml"
    v20 = "/home/ros/voevent/v20.xml"
    simple_xml_valid = "/home/ros/voevent/simple_xml_valid.xml"
    simple_xml_invalid = "/home/ros/voevent/simple_xml_invalid.xml"
    
    xsd_11 = "/home/ros/voevent/VOEvent-v1.1.xsd"
    xsd_20 = "/home/ros/voevent/VOEvent-v2.0.xsd"
    simple_xsd = "/home/ros/voevent/simple_xsd.xsd"                                                  
                                                                  
                                                                                
    with open(xsd_20) as f:                                                
        doc = etree.parse(f)                                                    
                                                                                
    print "Validating schema ... "                                              
    try:                                                                        
        schema = etree.XMLSchema(doc)                                           
    except lxml.etree.XMLSchemaParseError as e:                                 
        print e                                                                 
        exit(1)                                                                 
                                                                                
    print "Schema OK"                                                           
                                                                                
    with open(v20) as f:                                                
        doc = etree.parse(f)                                                    
                                                                                
    print "Validating document ..."                                             
    try:                                                                        
        schema.assertValid(v20)                                                 
    except lxml.etree.DocumentInvalid as e:                                     
        print e                                                                 
        exit(1)                                                                 
                                                                                
    print "Document OK"
    
  