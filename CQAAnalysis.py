

import LongTermValue as LTV
import QuestionTagger as QT
import PredictQuestionAnswerQuality as PQAQ

if __name__ == "__main__":

    #Step 1: Find Long Term Value of a Question
    ltv = LTV.LongTermValue()
    ltv.predictLongTermValue()

    #Step 2: Question Tagging
    q = QT.QuestionTagger()
    q.tagger()
    #Step 3: Question Answer Quality
    PQAQ.QAQuality()