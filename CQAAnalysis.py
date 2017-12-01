

import LongTermValue as LTV
import QuestionTagger as QT
import PredictQuestionAnswerQuality as PQAQ

import os

if __name__ == "__main__":

    #Step 0: Check if necessary folders exists

    #Input Folders and Files:
    #Folder: Data/ai_stackexchange_com
    #Files to be present:
    #1. "./Data/ai_stackexchange_com/Badges.xml",
    #2. "./Data/ai_stackexchange_com/Comments.xml"
    #3. "./Data/ai_stackexchange_com/PostHistory.xml"
    #4. "./Data/ai_stackexchange_com/PostLinks.xml"
    #5. "./Data/ai_stackexchange_com/Posts.xml"
    #6. "./Data/ai_stackexchange_com/Tags.xml"
    #7. "./Data/ai_stackexchange_com/Users.xml"
    #8. "./Data/ai_stackexchange_com/Votes.xml"


    #Checks for Output Folder
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