import validation
from major_minor  import *
from configparser import *


FILENAME = "config.ini"

class Section(Major):
    def __init__(self, name):
        super().__init__(name)
        self.keys = self._minors

    def addKey(self, key):
        self._addMinor(key)

    def addNewKey(self, name, value, valid=validation.DEFAULT, description=""):
        self.addKey(Key(name, value, valid, description))

    @classmethod
    def stackKey(cls, key):
        cls._stackMinor(key)

    @classmethod
    def stackNewKey(cls, name, value, valid=validation.DEFAULT, description=""):
        cls.stackKey(Key(name, value, valid, description))


class Key(Minor):
    def __init__(self, name, value, valid=validation.DEFAULT, description=""):
        super().__init__(name, valid)
        self.sections = self._majors

        self.value = value
        self.description = description

    def attachToSection(self, key):
        _attachToMajor(key)
        
    
#   --- FILE SECTION ---  #
Section('FILE')
Section.stackNewKey('FolderPath', "Record",   validation.PATH,
                    "folderpath key description")
Section.stackNewKey('FolderName', "dir",      validation.PATH,
                    "foldername key description")
Section.stackNewKey('ImageName',  "image",    validation.PATH,
                    "imagename key description")

#   --- TIME SECTION ---  #
Section('TIME')
Section.stackNewKey('Start',  '00:00:00',     validation.TIME,
                    "intervalstart key description")
Section.stackNewKey('Finish', '20:15:00',     validation.TIME,
                    "intervalfinish key description")
Section.stackNewKey('DeltaUnit',  'FPh',      validation.UNIT,
                    "deltatimeunit key description")
Section.stackNewKey('DeltaValue', '12',       validation.NUMBER,
                    "deltatimevalue key description")

#   --- CAMERA SECTION ---  #
Section('CAMERA')
Section.stackNewKey('StartIndex',    '0',     validation.NUMBER,
                    "startcameraindex key description")
Section.stackNewKey('IndexPriority', '1 2 3', validation.TUPLE,
                    "indeciesprioritylist key description")
Section.stackNewKey('ForceIndex',    'NO',    validation.BOOL,
                    "forcestartfromindex key description")
Section.stackNewKey('IndexIfLost',   'YES',   validation.BOOL,
                    "changecameraindexiflostconnection key description")
Section.stackNewKey('LostWait',      '10',    validation.NUMBER,
                    "connectionlostwait key description")

#   --- DEBUG SECTION ---  #
Section('DEBUG')
Section.stackNewKey('Mode', 'ON',             validation.BOOL,
                    "debugmode key description")
