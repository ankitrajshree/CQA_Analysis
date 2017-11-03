
class Posts:

    def __init__(self):
        self.Id = None
        self.PostId = None
        self.AcceptedAnswerId = None
        self.CreationDate = None
        self.Score = None
        self.ViewCount = None
        self.Body = None
        self.OwnerUserId = None
        self.LastEditorUserId = None
        self.LastEditDate = None
        self.LastActivityDate = None
        self.Title = None
        self.Tags = None
        self.AnswerCount = None
        self.CommentCount = None

        #Additional Attributes. To be added



    def parse(self, node):
        for attribute in node.attributes._attrs.keys():
            try:
                self.__setattr__(attribute, node.attributes._attrs[attribute]._value)
            except:
                print(str(attribute + " Not found"))

