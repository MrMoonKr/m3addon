#!/usr/bin/python3
# -*- coding: utf-8 -*-

import struct
import sys
from generateM3Library import generateM3Library
generateM3Library()
from m3 import *

def byteDataToHex(byteData):
    s = "0x"
    for i in range(len(byteData)):
        hexValue = hex(byteData[i])[2:]
        if len(hexValue) <= 1:
            hexValue = "0"+hexValue
        s +=hexValue
    return s

def printXmlElement(indent, name, stringValue):
    print (("\t"*indent) + ("<%s>" % name) + stringValue + ("</%s>" % name))


def printObject(indent, name, objectToPrint):
    if type(objectToPrint) == int:
        printXmlElement(indent,name,hex(objectToPrint))
    elif type(objectToPrint) == bytearray or type(objectToPrint) == bytes:
        s = byteDataToHex(objectToPrint)
        printXmlElement(indent,name,s)
    elif hasattr(type(objectToPrint),"fields"):
        print (("\t"*indent) + "<%s>" % name)
        for fieldName in objectToPrint.fields:
            fieldValue = getattr(objectToPrint,fieldName)
            if fieldValue == None:
                print (("\t"*(indent+1)) + "<%s />" % fieldName)
            elif fieldValue.__class__ == list:
                print (("\t"*(indent+1)) + "<%s>" % fieldName)
                for entry in fieldValue:
                    printObject(indent+2,fieldName+"-element", entry)
                print (("\t"*(indent+1)) + "</%s>" % fieldName)
            else:
                printObject(indent+1,fieldName, fieldValue)
        print (("\t"*indent) + "</%s>" % name)
    else:
        printXmlElement(indent,name,str(objectToPrint))

if __name__ == "__main__":
    if len(sys.argv) -1 != 1:
        sys.stderr.write("""\
Require one argument!
Useage:
    printXml.py /path/to/m3/file.m3
Or:
    printXml.py /path/to/m3/file.m3 > /path/to/xml/file/to/create.xml
""")
        sys.exit(2)
    inputFile = sys.argv[1]
    model = loadModel(inputFile)
    printObject(0,"model",model)