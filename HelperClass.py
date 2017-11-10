
import xml.dom.minidom

import Badges as bdg
import Comments as cmts
import PostHistory as phist
import PostLinks as plink
import Posts as posts
import Tags as tags
import Users as users
import Votes as votes



class HelperClass:

    def __init__(self):
        self.Badges = None
        self.Comments = None
        self.PostHistory = None
        self.PostLinks = None
        self.Posts = None
        self.Tags = None
        self.Users = None
        self.Votes = None

        self.documentDict = {}



    def getHCAttribute(self, name):
        return getattr(self,name)

    def setHCAttribute(self, name, value):
        setattr(self, name, value)

    def ParseFile(self, filename, className):

        f = open(filename,'r', encoding='utf8')
        doc = f.read()
        f.close()

        xmlDocument =  xml.dom.minidom.parseString(doc)

        mainChildNode = xmlDocument._get_firstChild()
        className = mainChildNode.localName

        #initialize the dictionary for the corresponding document
        self.documentDict[className] = []

        for node in mainChildNode.childNodes:
            if node.localName == 'row':                 #some nodes are None

                if className == 'badges':
                    badges = bdg.Badges()
                    badges.parse(node)
                    self.documentDict[className].append(badges)

                    pass
                elif className == 'comments':
                    comments = cmts.Comments()
                    comments.parse(node)
                    self.documentDict[className].append(comments)

                    pass
                elif className == 'posthistory':
                    postHistory = phist.PostHistory()
                    postHistory.parse(node)
                    self.documentDict[className].append(postHistory)
                    pass
                elif className == 'postlinks':
                    postLinks = plink.PostLinks()
                    postLinks.parse(node)
                    self.documentDict[className].append(postLinks)
                    pass
                elif className == 'posts':
                    post = posts.Posts()
                    post.parse(node)
                    self.documentDict[className].append(post)
                    pass
                elif className == 'tags':
                    tag = tags.Tags()
                    tag.parse(node)
                    self.documentDict[className].append(tag)
                    pass
                elif className == 'users':
                    user = users.Users()
                    user.parse(node)
                    self.documentDict[className].append(user)
                    pass
                elif className == 'votes':
                    vote = votes.Votes()
                    vote.parse(node)
                    self.documentDict[className].append(vote)
                    pass
                else:
                    raise "Error"
