import Files
import APHelperClass as HC
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
            X_matrix = np.empty(shape=(0, 14))
            Y_matrix = np.empty(shape=(0, 1))
            for QA_Pair in QA_Pairs:
                X_matrix = np.append(X_matrix, [[int(val) if val else 0 for val in
                                                 [QA_Pair.F1_AnswerersReputation,
                                                  QA_Pair.F2_AnsByAnswerer,
                                                  QA_Pair.F3_NumAnswerComments,
                                                  QA_Pair.F4_BodyLength,
                                                  QA_Pair.F5_AcceptedAnswer,
                                                  QA_Pair.F6_AnswerersViews,
                                                  QA_Pair.F7_AnswerersUpvotes,
                                                  QA_Pair.F8_AnswerersDownvotes,
                                                  QA_Pair.F9_QuestionScore,
                                                  QA_Pair.F10_QuestionViewCount,
                                                  QA_Pair.F11_QuestionCommentCount,
                                                  QA_Pair.F12_QuestionBodyLength,
                                                  QA_Pair.F13_QuestionTitleLength,
                                                  QA_Pair.F14_QuestionFavoriteCount
                                                  ]]], axis=0)
                Y_matrix = np.append(Y_matrix, [[int(QA_Pair.Y_Label_AnswerScore)]])
            np.savetxt('CSV Files_' + postType +'/data_hr'+str(key)+'.csv', X_matrix, delimiter=',',fmt='%i')
            np.savetxt('CSV Files_' + postType +'/label_hr'+str(key)+'.csv', Y_matrix, delimiter=',',fmt='%i')

    def generate_standardized_data(self, postType):
        for key,qapairs in self.questionAnswerPairsDict.items():
            QA_Pairs = qapairs
            X_matrix = np.empty(shape=(0, 14))
            Y_matrix = np.empty(shape=(0,1))
            for QA_Pair in QA_Pairs:
                X_matrix = np.append(X_matrix, [[int(val) if val else 0 for val in
                                                 [QA_Pair.F1_AnswerersReputation,
                                                  QA_Pair.F2_AnsByAnswerer,
                                                  QA_Pair.F3_NumAnswerComments,
                                                  QA_Pair.F4_BodyLength,
                                                  QA_Pair.F5_AcceptedAnswer,
                                                  QA_Pair.F6_AnswerersViews,
                                                  QA_Pair.F7_AnswerersUpvotes,
                                                  QA_Pair.F8_AnswerersDownvotes,
                                                  QA_Pair.F9_QuestionScore,
                                                  QA_Pair.F10_QuestionViewCount,
                                                  QA_Pair.F11_QuestionCommentCount,
                                                  QA_Pair.F12_QuestionBodyLength,
                                                  QA_Pair.F13_QuestionTitleLength,
                                                  QA_Pair.F14_QuestionFavoriteCount
                                             ]]], axis=0)
                Y_matrix = np.append(Y_matrix,[[int(QA_Pair.Y_Label_AnswerScore)]])
            X_matrix = StandardScaler().fit_transform(X_matrix)
            np.savetxt('CSV Files_' + postType +'/data_std_hr'+str(key)+'.csv',X_matrix,delimiter=',')
            np.savetxt('CSV Files_' + postType +'/label_std_hr'+str(key)+'.csv',Y_matrix,delimiter=',')

        pass

