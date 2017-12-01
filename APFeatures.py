
class Feature:
    def __init__(self):

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
        self.F11_QuestionCommentCount = None
        self.F12_QuestionBodyLength = None
        self.F13_QuestionTitleLength = None
        self.F14_QuestionFavoriteCount = None

        self.Y_Label_AnswerScore = None


class Features:
    def __init__(self):
        self.featureList = []