"""
Copyright: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import SimpleDao
import xml.sax
import os.path
import new
import xml.sax.saxutils

class XmlStorageDao(SimpleDao.SimpleDao):

    """
    DAO implemented in XML files.
    """

    def __init__(self, directory, encoding, logStream = None):

        """
        directory: where to put XML files
        encofing: encoding used for XML files
        logStream: output of logging messages.
        """

        SimpleDao.SimpleDao.__init__(self, logStream)
        self.directory = directory
        self.encoding = encoding
        assert self.encoding,\
            "encoding must be specified, for instance: 'utf-8'"
        self.classNameToList = {}
        self.dirtyClasses = {}

    def _newId(self, className):

        fileName = os.path.join(self.directory, className + "-id.txt")
        if os.path.exists(fileName):
            f = file(fileName)
            number = int(f.read())
            f.close()
        else:
            number = 1
        result = number
        number += 1

        f = open(fileName, "wt")
        f.write(str(number))
        f.close()

        return result

    def _getWholeList(self, clazz):

        className = clazz.__name__
        if self.classNameToList.has_key(className):
            return self.classNameToList[className]

        fileName = os.path.join(self.directory, className + ".xml")
        if os.path.exists(fileName):
            f = file(fileName)
            dh = _DataHandler(clazz)
            xml.sax.parse(f, dh)
            f.close()
            objectList = dh.objectList
        else:
            objectList = []

        self.classNameToList[className] = objectList
        return objectList

    def _replaceWholeList(self, clazz, lst):

        className = clazz.__name__
        self.classNameToList[className] = lst
        self.dirtyClasses[className] = 1
    
    def sync(self):

        for className in self.dirtyClasses.keys():
            self._saveList(
                className, self.classNameToList[className])

    def _saveList(self, className, lst):

        fileName = os.path.join(self.directory, className + ".xml")
        fileNameBackup = fileName + ".bak"
        self.classNameToList[className] = lst

        f = file(fileNameBackup, "wt")
        f.write(
        '<?xml version="1.0" encoding="%s" standalone="yes"?>'\
            % self.encoding)
        f.write("<xml>\n")
        for ob in lst:
            f.write("  <object>\n")
            for name, value in ob.__dict__.items():
                if name[0] != "_" and value != None:
                    if isinstance(value, int):
                        typeName = "int"
                        value = str(value)
                    elif isinstance(value, float):
                        typeName = "float"
                        value = str(value)
                    else:
                        typeName = "str"
                    f.write("    <attribute name=\"" \
                        + name + "\" value=\""\
                        + xml.sax.saxutils.escape(
                            value.encode(self.encoding))\
                        + "\" type=\"" + typeName + "\"/>\n")
            f.write("  </object>\n")
        f.write("</xml>\n")
        f.close()

        os.rename(fileNameBackup, fileName)

class _DataHandler(xml.sax.ContentHandler):

    def __init__(self, clazz):

        self.clazz = clazz
        self.objectList = []
        self.attributes = {}
        xml.sax.handler.ContentHandler.__init__(self)

    # SAX hooks
    def startElement(self, name, attrs):

        if name == "object":
            self.attributes = {}

        elif name == "attribute":
            name = attrs["name"]
            value = attrs["value"]
            typeName = attrs["type"]

            if typeName == "int":
                self.attributes[name] = int(value)
            elif typeName == "float":
                self.attributes[name] = float(value)
            elif typeName == "str":
                self.attributes[name] = value
            else:
                raise Exception, "unknown type: " + `type`
    

    def endElement(self, name):

        if name == "object":

            obj = new.instance(self.clazz)
            obj.__init__()
            for name in obj.__dict__.keys():
                if self.attributes.has_key(name):
                    obj.__dict__[name] = self.attributes[name]
            self.objectList.append(obj)


