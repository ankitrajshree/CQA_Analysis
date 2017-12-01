import Files
import QPHelperClass as HC
import csv
import numpy as np
from sklearn.preprocessing import StandardScaler

class CsvGenerator(object):
    def __init__(self, questionAnswerPairs):
        #self.helperObj = HC.HelperClass()
        self.questionAnswerPairsDict = questionAnswerPairs

    def genrate_csv(self, postType):
        for key,qapairs in self.questionAnswerPairsDict.items():
            QA_Pairs = qapairs
            X_matrix = np.empty(shape=(0, 17))
            Y_matrix = np.empty(shape=(0, 1))
            for QA_Pair in QA_Pairs:
                X_matrix = np.append(X_matrix, [[int(val) if val else 0 for val in
                                                 [QA_Pair.F1_QuestionersReputation,
                                                  QA_Pair.F2_QuesAskedByQuestionaire,
                                                  QA_Pair.F3_NumAnswerToQuestionInXHours,
                                                  QA_Pair.F4_ViewCount,
                                                  QA_Pair.F5_NumQuestionComments,
                                                  QA_Pair.F6_BodyLength,
                                                  QA_Pair.F7_TitleLength,
                                                  QA_Pair.F8_FavoriteCount,
                                                  QA_Pair.F9_QuestionersViews,
                                                  QA_Pair.F10_QuestionersUpVotes,
                                                  QA_Pair.F11_QuestionersDownVotes,
                                                  QA_Pair.F12_BestScoreAnswerLength,
                                                  QA_Pair.F13_BestScoreNumComments,
                                                  QA_Pair.F14_BestScoreTimeDiff,
                                                  QA_Pair.F15_ReputedUserNumComments,
                                                  QA_Pair.F16_SumScores,
                                                  QA_Pair.F17_ReputedUserReputation
                                                  ]]], axis=0)
                Y_matrix = np.append(Y_matrix, [[int(QA_Pair.Y_Label_QuestionScore)]])
            np.savetxt('CSV Files_' + postType +'/data_hr'+str(key)+'.csv', X_matrix, delimiter=',',fmt='%i')
            np.savetxt('CSV Files_' + postType +'/label_hr'+str(key)+'.csv', Y_matrix, delimiter=',',fmt='%i')

    def generate_standardized_data(self, postType):
        for key,qapairs in self.questionAnswerPairsDict.items():
            QA_Pairs = qapairs
            X_matrix = np.empty(shape=(0, 17))
            Y_matrix = np.empty(shape=(0,1))
            for QA_Pair in QA_Pairs:
                X_matrix = np.append(X_matrix, [[int(val) if val else 0 for val in
                                                 [QA_Pair.F1_QuestionersReputation,
                                                  QA_Pair.F2_QuesAskedByQuestionaire,
                                                  QA_Pair.F3_NumAnswerToQuestionInXHours,
                                                  QA_Pair.F4_ViewCount,
                                                  QA_Pair.F5_NumQuestionComments,
                                                  QA_Pair.F6_BodyLength,
                                                  QA_Pair.F7_TitleLength,
                                                  QA_Pair.F8_FavoriteCount,
                                                  QA_Pair.F9_QuestionersViews,
                                                  QA_Pair.F10_QuestionersUpVotes,
                                                  QA_Pair.F11_QuestionersDownVotes,
                                                  QA_Pair.F12_BestScoreAnswerLength,
                                                  QA_Pair.F13_BestScoreNumComments,
                                                  QA_Pair.F14_BestScoreTimeDiff,
                                                  QA_Pair.F15_ReputedUserNumComments,
                                                  QA_Pair.F16_SumScores,
                                                  QA_Pair.F17_ReputedUserReputation
                                                  ]]], axis=0)
                Y_matrix = np.append(Y_matrix,[[int(QA_Pair.Y_Label_QuestionScore)]])
            X_matrix = StandardScaler().fit_transform(X_matrix)
            np.savetxt('CSV Files_' + postType +'/data_std_hr'+str(key)+'.csv',X_matrix,delimiter=',')
            np.savetxt('CSV Files_' + postType +'/label_std_hr'+str(key)+'.csv',Y_matrix,delimiter=',')

        pass

