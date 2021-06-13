import sys
import validation
from major_minor import *


class Command(Major):
    def __init__(self, name, defaultHelpOption=True):
        super().__init__(name)
        self.options = self._minors

    def addOption(self, option):
        self._addMinor(option)

    def addNewOption(self, longname, shortname, valid=validation.DEFAULT):
        self.addOption(Option(longname, shortname, valid))

    @classmethod
    def stackOption(cls, option):
        cls._stackMinor(option)

    @classmethod
    def stackNewOption(cls, longname, shortname, valid=validation.DEFAULT):
        cls.stackOption(Option(longname, shortname, valid))

class Option(Minor):
    def __init__(self, longname, shortname='', valid=validation.DEFAULT):
        super().__init__(longname, valid)
        self.commands = self._majors

        self.shortname = shortname

    def __del__(self):
        for command in self.commands:
            if self.shortname:
                command.minors.pop(self.shortname)

    def _attachToMajor(self, command):
        super()._attachToMajor(command)
        
        if self.shortname:
            type(self)._assertNameInMajor(self.shortname, command)
            command.options[self.shortname] = self

    def attachToCommand(self, command):
        _attachToMajor(major)


Command('launch')
Command.stackNewOption('start',  's')
Command.stackNewOption('finish', 'f')
Command.stackNewOption('path',   'p')
Command('cameras')
Command.stackNewOption('list',   'l')
Command.stackNewOption('info',   'i')
Command('config')
Command.stackNewOption('list',   'l')
Command.stackNewOption('info',   'i')
Command.stackNewOption('check',  'c')
Command.stackNewOption('edit',   'e')
Command.stackNewOption('reset',  'r')
Command('help',  False)
Command('about', False)
