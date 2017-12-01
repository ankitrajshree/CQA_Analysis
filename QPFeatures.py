
class Feature:
    def __init__(self):

        self.F1_QuestionersReputation = None
        self.F2_QuesAskedByQuestionaire = None
        self.F3_NumAnswerToQuestionInXHours = None
        self.F4_ViewCount = None
        self.F5_NumQuestionComments = None
        self.F6_BodyLength = None
        self.F7_TitleLength = None
        self.F8_FavoriteCount = None
        self.F9_QuestionersViews = None
        self.F10_QuestionersUpVotes = None
        self.F11_QuestionersDownVotes = None
        self.F12_BestScoreAnswerLength = None
        self.F13_BestScoreNumComments = None
        self.F14_BestScoreTimeDiff = None
        self.F15_ReputedUserNumComments = None
        self.F16_SumScores = None
        self.F17_ReputedUserReputation = None

        self.Y_Label_QuestionScore = None


class Features:
    def __init__(self):
        self.featureList = []