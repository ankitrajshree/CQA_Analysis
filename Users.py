
class Users:

    def __init__(self):
        self.Id = None
        self.Reputation = None
        self.CreationDate = None
        self.DisplayName = None
        self.LastAccessDate = None
        self.Location = None
        self.AboutMe = None
        self.Views = None
        self.UpVotes = None
        self.DownVotes = None
        self.Age = None
        self.AccountId = None

    def parse(self, node):
        for attribute in node.attributes._attrs.keys():
            try:
                self.__setattr__(attribute, node.attributes._attrs[attribute]._value)
            except:
                print(str(attribute + " Not found"))
