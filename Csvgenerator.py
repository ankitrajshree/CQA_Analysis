import Files
import HelperClass as HC
import csv
import numpy as np
from sklearn import  preprocessing

class CsvGenerator(object):
    def __init__(self):
        self.helperObj = HC.HelperClass()

    def getQuestion_pair(self):
        for file in Files.InputFiles.keys():
            try:
                self.helperObj.ParseFile(Files.InputFiles[file], file)

            except:
                print("Error Parsing File")

        self.helperObj.PairCommentWithPosts()

        # Step 2. Create Question Answer Pairs
        questionAnswerPairs = self.helperObj.CreateQuestionAnswerPair()

        # Step 3. We have created Q/A pairs. Now we need to extract the features.
        self.helperObj.ExtractAllFeatures()
        self.helperObj.CreateLabels()
        return questionAnswerPairs

    def genrate_csv(self):
        QA_Pairs = self.getQuestion_pair()
        X_matrix = np.empty(shape=(0, 8))
        Y_matrix = np.empty(shape=(0, 1))
        for key, QA_Pair in QA_Pairs.items():
            X_matrix = np.append(X_matrix, [[int(val) if val else 0 for val in
                                             [QA_Pair.F1_QuestionersReputation,
                                              QA_Pair.F2_QuesAskedByQuestionaire,
                                              QA_Pair.F3_NumAnswerToQuestionInOneHour,
                                              QA_Pair.F4_SumScores,
                                              QA_Pair.F5_BestScoreAnswerLength,
                                              QA_Pair.F6_BestScoreNumComments,
                                              QA_Pair.F7_BestScoreTimeDiff,
                                              QA_Pair.F8_ReputedUserNumComments
                                              ]]], axis=0)
            Y_matrix = np.append(Y_matrix, [[int(QA_Pair.Y_Label_FrequentlyViewed)]])
        np.savetxt('data.csv', X_matrix, delimiter=',',fmt='%i')
        np.savetxt('label.csv', Y_matrix, delimiter=',',fmt='%i')

    def generate_normalized_csv(self):
        QA_Pairs = self.getQuestion_pair()
        X_matrix = np.empty(shape=(0, 8))
        Y_matrix = np.empty(shape=(0,1))
        for key, QA_Pair in QA_Pairs.items():
            X_matrix = np.append(X_matrix, [[int(val) if val else 0 for val in
                                        [QA_Pair.F1_QuestionersReputation,
                                         QA_Pair.F2_QuesAskedByQuestionaire,
                                         QA_Pair.F3_NumAnswerToQuestionInOneHour,
                                         QA_Pair.F4_SumScores,
                                         QA_Pair.F5_BestScoreAnswerLength,
                                         QA_Pair.F6_BestScoreNumComments,
                                         QA_Pair.F7_BestScoreTimeDiff,
                                         QA_Pair.F8_ReputedUserNumComments
                                         ]]], axis=0)
            Y_matrix = np.append(Y_matrix,[[int(QA_Pair.Y_Label_FrequentlyViewed)]])
        X_matrix = preprocessing.scale(X_matrix)
        np.savetxt('data_std.csv',X_matrix,delimiter=',')
        np.savetxt('label_std.csv',Y_matrix,delimiter=',')

        pass

if __name__ =='__main__':
    csvgen = CsvGenerator()
    csvgen.generate_normalized_csv()
    csvgen.genrate_csv()
