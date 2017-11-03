
class Tags:

    def __init__(self):
        self.Id = None
        self.TagName = None
        self.Count = None

        #Optional
        self.ExcerptPostId = None
        self.WikiPostId = None

    def parse(self, node):
        for attribute in node.attributes._attrs.keys():
            try:
                self.__setattr__(attribute, node.attributes._attrs[attribute]._value)
            except:
                print(str(attribute + " Not found"))

