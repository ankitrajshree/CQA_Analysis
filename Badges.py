

class Badges:

    def __init__(self):
        self.Id = None
        self.UserId = None
        self.Name = None
        self.Date = None
        self.Class = None
        self.TagBased = None

    def parse(self, node):
        for attribute in node.attributes._attrs.keys():
            try:
                self.__setattr__(attribute, node.attributes._attrs[attribute]._value)
            except:
                print(str(attribute + " Not found"))


