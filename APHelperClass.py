
import xml.dom.minidom

import Badges as bdg
import Comments as cmts
import PostHistory as phist
import PostLinks as plink
import Posts as posts
import Tags as tags
import Users as users
import Votes as votes

import APQuestionAnswer as QA

import APFeatures

import datetime
import operator


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
        self.QuestionAnswerPairs = None

        self.BADGES = 'badges'
        self.COMMENTS = 'comments'
        self.POSTHISTORY = 'posthistory'
        self.POSTLINKS = 'postlinks'
        self.POSTS = 'posts'
        self.TAGS = 'tags'
        self.USERS = 'users'
        self.VOTERS = 'votes'


    def getHCAttribute(self, name):
        return getattr(self,name)

    def ParseFile(self, filename, className):

        f = open(filename,'r',encoding='utf8')
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




    def PairCommentWithPosts(self):
        comments = self.documentDict[self.COMMENTS]
        for cmt in comments:
            postId = cmt.PostId
            for post in self.documentDict[self.POSTS]:
                if post.Id == postId:
                    try:
                        post.CommentsList.append(cmt)
                    except:
                        post.CommentsList = [cmt]

        pass


    def CreateQuestionAnswerPair(self):
        allPosts = self.documentDict[self.POSTS]
        allAnswers = []
        allQuestions = {}
        allPairs = {}

        for i, post in enumerate(allPosts):
            if post.PostTypeId == '2':
                #This is an answer
                allAnswers.append(post)
                answer = QA.Answer()
                answer.InitializeAnswer(post,allQuestions)

                #Add the question to Question/Answer Pair
                try:
                    allPairs[answer.Id] = answer
                except:
                    print("Answer Id is None")


                pass
            elif post.PostTypeId == '1':
                #This is a question

                ques = QA.Question()
                ques.InitializeQuestion(post)
#                isPaired = self.PairQuestionWithAnswer(allPairs, ans)

 #               if isPaired == False:
                    #Add answer to allAnswer dictionary
 #                   try:
 #               allQuestions[post.ParentId].append(post)
 #                   except:
 #                       allAnswers[post.ParentId] = [post]

                pass
        self.QuestionAnswerPairs = allPairs
        return self.QuestionAnswerPairs


    def SortByPostCreationTime(self, allPosts):

        postDict = {}
        for post in allPosts:
            date = post.CreationDate
            d = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
            postDict[d] = post
            a = 20

        sortedPostsKeys = sorted(postDict.keys())

        return [postDict, sortedPostsKeys]

        pass


    def GetAnswerersReputation(self):

        userList = self.documentDict[self.USERS]

        for postKey in self.QuestionAnswerPairs.keys():
            userId = self.QuestionAnswerPairs[postKey].OwnerUserId
            for index, user in enumerate(userList):
                if user.Id == userId:
                     self.QuestionAnswerPairs[postKey].F1_AnswerersReputation = userList[index].Reputation

        pass

    def GetAnswerersViews(self):

        userList = self.documentDict[self.USERS]

        for postKey in self.QuestionAnswerPairs.keys():
            userId = self.QuestionAnswerPairs[postKey].OwnerUserId
            for index, user in enumerate(userList):
                if user.Id == userId:
                     self.QuestionAnswerPairs[postKey].F6_AnswerersViews = userList[index].Views

        pass

    def AcceptedAnswer(self):

        postList = self.documentDict[self.POSTS]

        for postKey in self.QuestionAnswerPairs.keys():
            postId = self.QuestionAnswerPairs[postKey].Id
            for index, posts in enumerate(postList):
                    if postId == posts.AcceptedAnswerId:
                         self.QuestionAnswerPairs[postKey].F5_AcceptedAnswer = 1
                         break
                    else:
                         self.QuestionAnswerPairs[postKey].F5_AcceptedAnswer = 0

        pass

    def GetAnswerersUpvotes(self):

        userList = self.documentDict[self.USERS]

        for postKey in self.QuestionAnswerPairs.keys():
            userId = self.QuestionAnswerPairs[postKey].OwnerUserId
            for index, user in enumerate(userList):
                if user.Id == userId:
                     self.QuestionAnswerPairs[postKey].F7_AnswerersUpvotes = userList[index].UpVotes

        pass

    def GetAnswerersDownvotes(self):

        userList = self.documentDict[self.USERS]

        for postKey in self.QuestionAnswerPairs.keys():
            userId = self.QuestionAnswerPairs[postKey].OwnerUserId
            for index, user in enumerate(userList):
                if user.Id == userId:
                     self.QuestionAnswerPairs[postKey].F8_AnswerersDownvotes = userList[index].DownVotes

        pass

    def GetBodyLength(self):

        postList = self.documentDict[self.POSTS]

        for postKey in self.QuestionAnswerPairs.keys():
            answerId = self.QuestionAnswerPairs[postKey].Id
            for index, post in enumerate(postList):
                if post.Id == answerId:
                   self.QuestionAnswerPairs[postKey].F4_BodyLength  = (len((postList[index].Body).split()))

        pass



    def NumberofComments(self):
        postList = self.documentDict[self.POSTS]

        for postKey in self.QuestionAnswerPairs.keys():
            answerId = self.QuestionAnswerPairs[postKey].Id
            for index, post in enumerate(postList):
                if post.Id == answerId:
                    self.QuestionAnswerPairs[postKey].F3_NumAnswerComments = postList[index].CommentCount

        pass

    def GetQuestionScore(self):
        postList = self.documentDict[self.POSTS]

        for postKey in self.QuestionAnswerPairs.keys():
            questionId = self.QuestionAnswerPairs[postKey].ParentId
            for index, post in enumerate(postList):
                if post.Id == questionId:
                    self.QuestionAnswerPairs[postKey].F9_QuestionScore = postList[index].Score

        pass

    def GetQuestionViewCount(self):
        postList = self.documentDict[self.POSTS]

        for postKey in self.QuestionAnswerPairs.keys():
            questionId = self.QuestionAnswerPairs[postKey].ParentId
            for index, post in enumerate(postList):
                if post.Id == questionId:
                    self.QuestionAnswerPairs[postKey].F10_QuestionViewCount = postList[index].ViewCount

        pass

    def GetQuestionCommentCount(self):
        postList = self.documentDict[self.POSTS]

        for postKey in self.QuestionAnswerPairs.keys():
            questionId = self.QuestionAnswerPairs[postKey].ParentId
            for index, post in enumerate(postList):
                if post.Id == questionId:
                    self.QuestionAnswerPairs[postKey].F11_QuestionCommentCount = postList[index].CommentCount

        pass

    def GetQuestionBodyLength(self):
        postList = self.documentDict[self.POSTS]

        for postKey in self.QuestionAnswerPairs.keys():
            questionId = self.QuestionAnswerPairs[postKey].ParentId
            for index, post in enumerate(postList):
                if post.Id == questionId:
                    self.QuestionAnswerPairs[postKey].F12_QuestionBodyLength = (len((postList[index].Body).split()))

        pass

    def GetQuestionTitleLength(self):
        postList = self.documentDict[self.POSTS]

        for postKey in self.QuestionAnswerPairs.keys():
            questionId = self.QuestionAnswerPairs[postKey].ParentId
            for index, post in enumerate(postList):
                if post.Id == questionId:
                    self.QuestionAnswerPairs[postKey].F13_QuestionTitleLength = (len((postList[index].Title).split()))

        pass

    def GetQuestionFavoriteCount(self):
        postList = self.documentDict[self.POSTS]

        for postKey in self.QuestionAnswerPairs.keys():
            questionId = self.QuestionAnswerPairs[postKey].ParentId
            for index, post in enumerate(postList):
                if post.Id == questionId:
                    self.QuestionAnswerPairs[postKey].F14_QuestionFavoriteCount = postList[index].FavoriteCount

        pass


    def ExtractAllFeatures(self, hours):

        #Create the Object of Feature Class
        features = APFeatures.Features()

        #1. Need to sort the posts dict in ascending order of timestamp, then view the posts.
        allPosts = self.documentDict[self.POSTS]
        postDict, sortedKeys = self.SortByPostCreationTime(allPosts)


        #2. Questioners Reputation
        self.GetAnswerersReputation()
        self.GetBodyLength()
        self.NumberofComments()
        self.GetAnswerersViews()
        self.GetAnswerersUpvotes()
        self.GetAnswerersDownvotes()
        self.GetQuestionScore()
        self.GetQuestionViewCount()
        self.GetQuestionCommentCount()
        self.GetQuestionBodyLength()
        self.GetQuestionTitleLength()
        self.GetQuestionFavoriteCount()

        #3. Questions asked by questionaire

        userDict = {}   #this will store userID and questions asked by the user
        userList = self.documentDict[self.USERS]
        for postKey in sortedKeys: #posts sorted by creation time
            if postDict[postKey].PostTypeId == '2': # If id is 1, it is a question
                #search the user who has asked the question
                userID = postDict[postKey].OwnerUserId

                #for this userID enter a new user in dictionary or update the 'question asked until this post' in the existing entry
                try: #try updating
                    userDict[userID].answerProvided += 1
                except:
                    #create new pbject of User class
                    newUser = QA.User(userID)
                    newUser.answerProvided = 0
                    userDict[userID] = newUser    #initialize the number of questions asked by the user previous to asking this question

                #we know the post ID of this question. We can append this feature value in the self.QuestionAnswerPairs dict
                currentPostId = postDict[postKey].Id

                #To the current Post ID add the feature - question asked by the questionaire before asking the current question
                self.QuestionAnswerPairs[currentPostId].F2_AnsByAnswerer = userDict[userID].answerProvided
                #self.QuestionAnswerPairs[currentPostId].Owner = userList[userID] #add the original users object
        a=9

        for key, qaPairs in self.QuestionAnswerPairs.items():
            feature = APFeatures.Feature()

            feature.F1_AnswerersReputation        =   qaPairs.F1_AnswerersReputation
            feature.F2_AnsByAnswerer      =   qaPairs.F2_AnsByAnswerer
            feature.F3_NumAnswerComments  =   qaPairs.F3_NumAnswerComments
            feature.F4_BodyLength                    =   qaPairs.F4_BodyLength
            feature.F5_AcceptedAnswer        =   qaPairs.F5_AcceptedAnswer
            feature.F6_AnswerersViews = qaPairs.F6_AnswerersViews
            feature.F7_AnswerersUpvotes = qaPairs.F7_AnswerersUpvotes
            feature.F8_AnswerersDownvotes = qaPairs.F8_AnswerersDownvotes
            feature.F9_QuestionScore = qaPairs.F9_QuestionScore
            feature.F10_QuestionViewCount = qaPairs.F10_QuestionViewCount
            feature.F11_QuestionCommentCount = qaPairs.F11_QuestionCommentCount
            feature.F12_QuestionBodyLength = qaPairs.F12_QuestionBodyLength
            feature.F13_QuestionTitleLength = qaPairs.F13_QuestionTitleLength
            feature.F14_QuestionFavoriteCount = qaPairs.F14_QuestionFavoriteCount


            feature.Y_Label_AnswerScore        =   qaPairs.Y_Label_AnswerScore



            features.featureList.append(feature)


        return features.featureList

        pass


    def CreateLabels(self):
        quesAnsPair = self.QuestionAnswerPairs
        AnswerScoreList = [int(value.Score)  for key,value in quesAnsPair.items()]
        import statistics
        medianAnswerScoreList = statistics.median(AnswerScoreList)

        for key, value in quesAnsPair.items():
            if int(quesAnsPair[key].Score) <= medianAnswerScoreList:
                quesAnsPair[key].Y_Label_AnswerScore = 0
            else:
                quesAnsPair[key].Y_Label_AnswerScore = 1

        pass