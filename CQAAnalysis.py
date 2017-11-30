

import LongTermValue as LTV
import QuestionTagger as QT


if __name__ == "__main__":

    #Step 1: Find Long Term Value of a Question
    ltv = LTV.LongTermValue()
    ltv.predictLongTermValue()

    #Step 2: Question Tagging
    q = QT.QuestionTagger()
    q.tagger()


