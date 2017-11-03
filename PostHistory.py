

class PostHistory:

    def __init__(self):
        self.Id = None
        self.PostHistoryTypeId = None
        self.PostId = None
        self.RevisionGUID = None
        self.CreationDate = None
        self.UserId = None
        self.Text = None


    def parse(self, node):
        for attribute in node.attributes._attrs.keys():
            try:
                self.__setattr__(attribute, node.attributes._attrs[attribute]._value)
            except:
                print(str(attribute + " Not found"))


