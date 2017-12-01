

import LongTermValue as LTV
import QuestionTagger as QT
import PredictQuestionAnswerQuality as PQAQ

import os

if __name__ == "__main__":

    #Step 0: Check if necessary folders exists
    OutputDirList = ["CSV Files", "CSV Files_Q", "CSV Files_A", "Images_LTV", "Images_Q", "Images_A"]
    for dir in OutputDirList:
        try:
            os.mkdir("./" + dir)
        except:
            print(dir + " folder already exists. Output will be overwritten.")

    #Step 1: Find Long Term Value of a Question
    ltv = LTV.LongTermValue()
    ltv.predictLongTermValue()

    #Step 2: Question Tagging
    q = QT.QuestionTagger()
    q.tagger()
    #Step 3: Question Answer Quality
    PQAQ.QAQuality()