
class Question:

    def __init__(self):

        #Attributes from Posts class
        self.Id = None
        self.ViewCount = None
        self.CreationDate = None
        self.OwnerUserId = None
        self.AnswerCount = None
        self.CommentCount = None
        self.Score = None

        #Newly Created Attributes
        self.AnswersList = []
        self.Owner = None

        self.F1_QuestionersReputation = None
        self.F2_QuesAskedByQuestionaire = None
        self.F3_NumAnswerToQuestionInOneHour = None
        self.F4_SumScores = None
        self.F5_BestScoreAnswerLength = None
        self.F6_BestScoreNumComments = None
        self.F7_BestScoreTimeDiff = None


        pass


    def InitializeQuestion(self, post,  PossibleAnswerDict):
        self.Id = post.Id
        self.ViewCount = post.ViewCount #To be Predicted
        self.CreationDate = post.CreationDate
        self.AnswerCount = post.AnswerCount
        self.CommentCount = post.CommentCount
        self.Score = post.Score
        




        self.OwnerUserId = post.OwnerUserId
        self.Owner = None


        self.GetAnswers(PossibleAnswerDict)



        pass

    def GetAnswers(self, PossibleAnswerDict):

        answers = None

        #Try getting all the answers list from the dictionary using Question's Post ID as key
        try:
            answers = PossibleAnswerDict[self.Id]
        except:
            print("Not found. Not an Error. Dont Worry!")

        if answers is not None:
            for answer in answers:
                self.AnswersList.append(answer)

        pass


class Answer:

    def __init__(self):
        self.Id = None
        self.CreationDate = None
        self.OwnerUserId = None
        self.Score = None
        self.ParentId = None
        self.CommentCount = None
        self.Body = None
        self.TimeDifference = None




        pass

    def InitializeAnswer(self, post):
        self.Id = post.Id
        self.CreationDate = post.CreationDate
        self.OwnerUserId = post.OwnerUserId
        self.Score = post.Score
        self.ParentId = post.ParentId
        self.CommentCount = post.CommentCount
        self.Body = post.Body
        self.TimeDifference = None




        pass



class User:
    def __init__(self, userId):
        self.UserId = userId
        self.questionAsked = None
        self.answerGiven = None
        pass

