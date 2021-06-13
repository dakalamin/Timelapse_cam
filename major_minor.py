import validation

class Major:
    DICT = dict()
    LAST = None
    
    def __init__(self, name):
        cls = type(self)

        if not cls.DICT:
            cls.DICT = dict()
        elif name in cls.DICT:
            raise Exception("ERROR")

        cls.LAST = cls.DICT[name] = self
        
        self.name = name
        self._minors = dict()

    def __del__(self):
        type(self).DICT.pop(self.name)

    def _addMinor(self, minor):
        minor.attachToMajor(self)

    @classmethod
    def _stackMinor(cls, minor):
        minor._attachToMajor(cls.LAST)


class Minor:
    def __init__(self, name, valid=validation.DEFAULT):
        self._majors = set()

        self.name  = name
        self.valid = valid

    def __del__(self):
        for major in self._majors:
            major._minors.pop(self.name)

    def _assertNameInMajor(name, major):
        if name in major._minors:
            raise Exception("ERROR")

    def _attachToMajor(self, major):
        type(self)._assertNameInMajor(self.name, major)
        major._minors[self.name] = self

        self._majors.add(major)
