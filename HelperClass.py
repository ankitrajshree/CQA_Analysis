
import xml.dom.minidom

import Badges as bdg
import Comments as cmts
import PostHistory as phist
import PostLinks as plink
import Posts as posts
import Tags as tags
import Users as users
import Votes as votes

import QuestionAnswer as QA

import Features

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


    def PairAnswerWithQuestion(self, allPairs, ans):
        try:
            allPairs[ans.ParentId].AnswersList.append(ans)
            return True
        except:
            return False


    def CreateQuestionAnswerPair(self):
        allPosts = self.documentDict[self.POSTS]
        allQuestions = []
        allAnswers = {}
        allPairs = {}

        for i, post in enumerate(allPosts):
            if post.PostTypeId == '1':
                #This is a question
                allQuestions.append(post)
                question = QA.Question()
                question.InitializeQuestion(post,allAnswers)



                #Add the question to Question/Answer Pair
                try:
                    allPairs[question.Id] = question
                except:
                    print("Question Id is None")


                pass
            elif post.PostTypeId == '2':
                #This is an answer

                ans = QA.Answer()
                ans.InitializeAnswer(post)
                isPaired = self.PairAnswerWithQuestion(allPairs, ans)

                if isPaired == False:
                    #Add answer to allAnswer dictionary
                    try:
                        allAnswers[post.ParentId].append(post)
                    except:
                        allAnswers[post.ParentId] = [post]

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


    def GetQuestionersReputation(self):

        userList = self.documentDict[self.USERS]

        for postKey in self.QuestionAnswerPairs.keys():
            userId = self.QuestionAnswerPairs[postKey].OwnerUserId
            for index, user in enumerate(userList):
                if user.Id == userId:
                    self.QuestionAnswerPairs[postKey].F1_QuestionersReputation = userList[index].Reputation
                    break

        pass


    def FindNumAnswerAndTheirScoresInXHours(self, hours):

        for postKey in self.QuestionAnswerPairs.keys():
            questionAnswerPair = self.QuestionAnswerPairs[postKey]
            timeQuestion = questionAnswerPair.CreationDate
            answerList = questionAnswerPair.AnswersList
            questionCreationTime = datetime.datetime.strptime(timeQuestion, "%Y-%m-%dT%H:%M:%S.%f")

            numAnswerCount = 0
            sumScores = 0
            answerInOneHourList = []
            for answer in answerList:

                #Answer in 1 Hour and Score
                answerCreationTime = datetime.datetime.strptime(answer.CreationDate, "%Y-%m-%dT%H:%M:%S.%f")
                diff_in_minutes = (answerCreationTime - questionCreationTime).total_seconds() / 60.0
                if diff_in_minutes <= (hours*60):
                    answerInOneHourList.append(answer)
                    numAnswerCount += 1
                    sumScores += int(answer.Score)

            self.QuestionAnswerPairs[postKey].F3_NumAnswerToQuestionInXHours = numAnswerCount

            self.QuestionAnswerPairs[postKey].F4_SumScores = sumScores




            #Getting the best scored answer for each post
            bestScoredAnswer = None
            try:
                sorted(answerInOneHourList, key=lambda a: int(a.Score), reverse=True)
                bestScoredAnswer = answerInOneHourList[0]
            except:
                print("No Answer within 1 hour")

            if bestScoredAnswer is not None:
                bodyStr = bestScoredAnswer.Body
                import re
                pattern = re.compile('<.*?>')
                tagStrippedBodyStr = re.sub(pattern, '', bodyStr)

                self.QuestionAnswerPairs[postKey].F5_BestScoreAnswerLength = tagStrippedBodyStr.__len__()

                #self.QuestionAnswerPairs[postKey].F5_BestScoreAnswerLength = bestScoredAnswer.Body.__len__()
                self.QuestionAnswerPairs[postKey].F6_BestScoreNumComments = bestScoredAnswer.CommentCount

                answerCTime = datetime.datetime.strptime(bestScoredAnswer.CreationDate, "%Y-%m-%dT%H:%M:%S.%f")
                self.QuestionAnswerPairs[postKey].F7_BestScoreTimeDiff = (answerCTime - questionCreationTime).total_seconds() / 60.0




        x = 20


        pass


    def NumCommentsInQAOfHighRepUser(self, hours):

        for postKey in self.QuestionAnswerPairs.keys():
            questionAnswerPair = self.QuestionAnswerPairs[postKey]
            timeQuestion = questionAnswerPair.CreationDate
            answerList = questionAnswerPair.AnswersList
            questionCreationTime = datetime.datetime.strptime(timeQuestion, "%Y-%m-%dT%H:%M:%S.%f")

            numAnswerCount = 0
            answerInOneHourList = []
            for answer in answerList:

                #Answer in 1 Hour
                answerCreationTime = datetime.datetime.strptime(answer.CreationDate, "%Y-%m-%dT%H:%M:%S.%f")
                diff_in_minutes = (answerCreationTime - questionCreationTime).total_seconds() / 60.0
                if diff_in_minutes <= (hours*60):
                    answerInOneHourList.append(answer)
                    numAnswerCount += 1

            #Find the reputation of each user in answerInOneHourList and get the highest
            userIdLists = []
            for ans in answerInOneHourList:
                userIdLists.append(ans.OwnerUserId)


            reputationDict = {}
            for userId in userIdLists:
                for user in self.documentDict[self.USERS]:
                    if userId == user.Id:
                        reputationDict[userId] = int(user.Reputation)
                        break

            reputedUserId, reputationScore = [None,None]
            try:
                reputedUserId, reputationScore = sorted(reputationDict.items(), key=operator.itemgetter(1), reverse=True)[0]
            except:
                print("Object may be None")

            #reputedUserId, reputationScore =  max([(userId, user.Reputation)  for user in self.documentDict[self.USERS] if userId == user.Id] , key=operator.itemgetter(1))

            questionCreationTimePlusX = questionCreationTime + datetime.timedelta(hours=1)
            numComments = self.NumberofComments(reputedUserId, questionCreationTimePlusX)
            self.QuestionAnswerPairs[postKey].F8_ReputedUserNumComments = numComments

            c = 40


        pass

    def NumberofComments(self, userId, time):
        posts_before_onehr = []
        allPosts = self.documentDict[self.POSTS]
        postDict, sortedKeys = self.SortByPostCreationTime(allPosts)

        numComments = 0
        for postKey in sortedKeys: #posts sorted by creation time
            postCreationTime = datetime.datetime.strptime(postDict[postKey].CreationDate, "%Y-%m-%dT%H:%M:%S.%f")

            if postDict[postKey].OwnerUserId == userId and postDict[postKey].CommentsList is not None :
                if postCreationTime <= time:
                    for comment in postDict[postKey].CommentsList:
                        commentCreationTime = datetime.datetime.strptime(comment.CreationDate,"%Y-%m-%dT%H:%M:%S.%f")
                        if commentCreationTime <time:
                            numComments += 1
            else:
                pass
        return numComments
        pass


    def ExtractAllFeatures(self, hours):

        #Create the Object of Feature Class
        features = Features.Features()

        #1. Need to sort the posts dict in ascending order of timestamp, then view the posts.
        allPosts = self.documentDict[self.POSTS]
        postDict, sortedKeys = self.SortByPostCreationTime(allPosts)


        #2. Questioners Reputation
        self.GetQuestionersReputation()

        #3. Questions asked by questionaire

        userDict = {}   #this will store userID and questions asked by the user
        userList = self.documentDict[self.USERS]
        for postKey in sortedKeys: #posts sorted by creation time
            if postDict[postKey].PostTypeId == '1': # If id is 1, it is a question
                #search the user who has asked the question
                userID = postDict[postKey].OwnerUserId

                #for this userID enter a new user in dictionary or update the 'question asked until this post' in the existing entry
                try: #try updating
                    userDict[userID].questionAsked += 1
                except:
                    #create new pbject of User class
                    newUser = QA.User(userID)
                    newUser.questionAsked = 0
                    userDict[userID] = newUser    #initialize the number of questions asked by the user previous to asking this question

                #we know the post ID of this question. We can append this feature value in the self.QuestionAnswerPairs dict
                currentPostId = postDict[postKey].Id

                #To the current Post ID add the feature - question asked by the questionaire before asking the current question
                self.QuestionAnswerPairs[currentPostId].F2_QuesAskedByQuestionaire = userDict[userID].questionAsked
                #self.QuestionAnswerPairs[currentPostId].Owner = userList[userID] #add the original users object
        a=9


        #4. Num Answers to Questions within one hour and Sum of their Scores
        self.FindNumAnswerAndTheirScoresInXHours(hours)


        #8. NumComments in Q/A of highest reputation user of the answer of current post
        self.NumCommentsInQAOfHighRepUser(hours)


        for key, qaPairs in self.QuestionAnswerPairs.items():
            feature = Features.Feature()

            feature.F1_QuestionersReputation        =   qaPairs.F1_QuestionersReputation
            feature.F2_QuesAskedByQuestionaire      =   qaPairs.F2_QuesAskedByQuestionaire
            feature.F3_NumAnswerToQuestionInXHours  =   qaPairs.F3_NumAnswerToQuestionInXHours
            feature.F4_SumScores                    =   qaPairs.F4_SumScores
            feature.F5_BestScoreAnswerLength        =   qaPairs.F5_BestScoreAnswerLength
            feature.F6_BestScoreNumComments         =   qaPairs.F6_BestScoreNumComments
            feature.F7_BestScoreTimeDiff            =   qaPairs.F7_BestScoreTimeDiff
            feature.F8_ReputedUserNumComments       =   qaPairs.F8_ReputedUserNumComments

            feature.Y_Label_FrequentlyViewed        =   qaPairs.Y_Label_FrequentlyViewed



            features.featureList.append(feature)


        return features.featureList

        pass


    def CreateLabels(self):
        quesAnsPair = self.QuestionAnswerPairs
        ViewCountList = [int(value.ViewCount)  for key,value in quesAnsPair.items()]
        import statistics
        medianViewCountList = statistics.median(ViewCountList)

        for key, value in quesAnsPair.items():
            if int(quesAnsPair[key].ViewCount) <= medianViewCountList:
                quesAnsPair[key].Y_Label_FrequentlyViewed = 0
            else:
                quesAnsPair[key].Y_Label_FrequentlyViewed = 1
        pass
