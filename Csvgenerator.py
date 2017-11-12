import Files
import HelperClass as HC
import csv
import numpy as np
from sklearn import  preprocessing

class CsvGenerator(object):
    def __init__(self, questionAnswerPairs):
        #self.helperObj = HC.HelperClass()
        self.questionAnswerPairsDict = questionAnswerPairs

    def genrate_csv(self):
        for key,qapairs in self.questionAnswerPairsDict.items():
            QA_Pairs = qapairs
            X_matrix = np.empty(shape=(0, 8))
            Y_matrix = np.empty(shape=(0, 1))
            for QA_Pair in QA_Pairs:
                X_matrix = np.append(X_matrix, [[int(val) if val else 0 for val in
                                                 [QA_Pair.F1_QuestionersReputation,
                                                  QA_Pair.F2_QuesAskedByQuestionaire,
                                                  QA_Pair.F3_NumAnswerToQuestionInXHours,
                                                  QA_Pair.F4_SumScores,
                                                  QA_Pair.F5_BestScoreAnswerLength,
                                                  QA_Pair.F6_BestScoreNumComments,
                                                  QA_Pair.F7_BestScoreTimeDiff,
                                                  QA_Pair.F8_ReputedUserNumComments
                                                  ]]], axis=0)
                Y_matrix = np.append(Y_matrix, [[int(QA_Pair.Y_Label_FrequentlyViewed)]])
            np.savetxt('CSV Files/data_hr'+str(key)+'.csv', X_matrix, delimiter=',',fmt='%i')
            np.savetxt('CSV Files/label_hr'+str(key)+'.csv', Y_matrix, delimiter=',',fmt='%i')

    def generate_standardized_data(self):
        for key, qapairs in self.questionAnswerPairsDict.items():
            QA_Pairs = qapairs
            X_matrix = np.empty(shape=(0, 8))
            Y_matrix = np.empty(shape=(0,1))
            for QA_Pair in QA_Pairs:
                X_matrix = np.append(X_matrix, [[int(val) if val else 0 for val in
                                            [QA_Pair.F1_QuestionersReputation,
                                             QA_Pair.F2_QuesAskedByQuestionaire,
                                             QA_Pair.F3_NumAnswerToQuestionInXHours,
                                             QA_Pair.F4_SumScores,
                                             QA_Pair.F5_BestScoreAnswerLength,
                                             QA_Pair.F6_BestScoreNumComments,
                                             QA_Pair.F7_BestScoreTimeDiff,
                                             QA_Pair.F8_ReputedUserNumComments
                                             ]]], axis=0)
                Y_matrix = np.append(Y_matrix,[[int(QA_Pair.Y_Label_FrequentlyViewed)]])
            X_matrix = preprocessing.scale(X_matrix)
            np.savetxt('CSV Files/data_std_hr'+str(key)+'.csv',X_matrix,delimiter=',')
            np.savetxt('CSV Files/label_std_hr'+str(key)+'.csv',Y_matrix,delimiter=',')

        pass

