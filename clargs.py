import sys
import validation


class Command:
    DICT = dict()
    LAST = None
    
    def __init__(self, name, defaultHelpOption=True):
        if name in Command.DICT:
            errmsg = f"{name} is an already used command"
            raise Exception(errmsg)

        Command.LAST = Command.DICT[name] = self
        
        self.name = name
        self.options = dict()

        if defaultHelpOption:
            self.addNewOption('help', 'h')

    def __del__(self):
        Command.DICT.pop(self.name)

    def addOption(self, option):
        option.attachToCommand(self)

    def addNewOption(self, longname, shortname=''):
        self.addOption(Option(longname, shortname))

    def stackOption(option):
        option.attachToCommand(Command.LAST)

    def stackNewOption(longname, shortname=''):
        Command.stackOption(Option(longname, shortname))

    def Get(name):
        #   if name not in Command.DICT:
        #       return Command(name)
        return Command.DICT.get(name, None)
        

class Option:
    def __init__(self, longname, shortname='', valid=validation.DEFAULT):
        self.commands = set()
        
        self.lname = longname
        self.sname = shortname

    def __del__(self):
        for command in self.commands:
            command.options.pop(self.lname)
            if self.sname:
                command.options.pop(self.sname)

    def isNameInCommand(name, command):
        if name in command.options:
            errmsg = f"{name} is an already used option in {command.name}"
            raise Exception(errmsg)

    def attachToCommand(self, command):
        Option.isNameInCommand(self.lname, command)
        if self.sname:
            Option.isNameInCommand(self.sname, command)
            command.options[self.sname] = self
        
        command.options[self.lname] = self

        self.commands.add(command)


def initCommandDict():
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



if __name__ == "__main__":
    initCommandDict()
