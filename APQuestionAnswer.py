
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
        self.Title = None
        self.Body = None
        self.FavoriteCount = None


        pass


    def InitializeQuestion(self, post):
        self.Id = post.Id
        self.ViewCount = post.ViewCount
        self.CreationDate = post.CreationDate
        self.AnswerCount = post.AnswerCount
        self.CommentCount = post.CommentCount
        self.Score = post.Score                #To be predicted
        self.CommentsList = post.CommentsList
        self.Body = post.Body
        self.Title = post.Title
        self.FavoriteCount = post.FavoriteCount
        self.OwnerUserId = post.OwnerUserId

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
        self.CommentsList = None

        self.QuestionsList = []
        self.CommentsList = []
        self.Owner = None

        self.F1_AnswerersReputation = None
        self.F2_AnsByAnswerer = None
        self.F3_NumAnswerComments = None
        self.F4_BodyLength = None
        self.F5_AcceptedAnswer = None
        self.F6_AnswerersViews = None
        self.F7_AnswerersUpvotes = None
        self.F8_AnswerersDownvotes = None
        self.F9_QuestionScore = None
        self.F10_QuestionViewCount = None
        self.F11_NumQuestionComments = None
        self.F12_QuestionBodyLength = None
        self.F13_QuestionTitleLength = None
        self.F14_QuestionFavoriteCount = None

        self.Y_Label_AnswerScore = None



        pass

    def InitializeAnswer(self, post,PossibleQuestionDict):
        self.Id = post.Id
        self.CreationDate = post.CreationDate
        self.OwnerUserId = post.OwnerUserId
        self.Score = post.Score
        self.ParentId = post.ParentId
        self.CommentCount = post.CommentCount
        self.Body = post.Body
        self.TimeDifference = None
        self.CommentsList = post.CommentsList

        self.GetQuestions(PossibleQuestionDict)

        pass

    def GetQuestions(self, PossibleQuestionDict):

        questions = None

        #Try getting all the answers list from the dictionary using Question's Post ID as key
        try:
            questions = PossibleQuestionDict[self.Id]
        except:
            print("Not found. Not an Error. Dont Worry!")

        if questions is not None:
            for question in questions:
                self.QuestionsList.append(question)

        pass



class User:
    def __init__(self, userId):
        self.UserId = userId
        self.answerQuestioned = None
        self.questionGiven = None
        pass

