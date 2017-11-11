
class Feature:
    def __init__(self):

        self.F1_QuestionersReputation = None
        self.F2_QuesAskedByQuestionaire = None
        self.F3_NumAnswerToQuestionInXHours = None
        self.F4_SumScores = None
        self.F5_BestScoreAnswerLength = None
        self.F6_BestScoreNumComments = None
        self.F7_BestScoreTimeDiff = None
        self.F8_ReputedUserNumComments = None

        self.Y_Label_FrequentlyViewed = None


class Features:
    def __init__(self):
        self.featureList = []