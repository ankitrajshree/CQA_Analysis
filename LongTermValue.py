
import Files

import HelperClass as HC

import Csvgenerator

"""
Class to predict Long Term Value of the post
"""
class LongTermValue:

    def __init__(self):
        pass

    def predictLongTermValue(self):

        #Step 1. Parse all the input files
        print(Files.InputFiles)

        helperObj = HC.HelperClass()

        for file in Files.InputFiles.keys():
            try:
                helperObj.ParseFile(Files.InputFiles[file], file )

            except:
                print("Error Parsing File")


        helperObj.PairCommentWithPosts()


        #Step 2. Create Question Answer Pairs
        questionAnswerPairs = helperObj.CreateQuestionAnswerPair()

        # Step 3. We have created Q/A pairs. Now we need to extract the features.
        hourList = [1,6,12,24]
        hourFeaturePair = {}
        for hour in hourList:
            helperObj.CreateLabels()
            featureList = helperObj.ExtractAllFeatures(hour)
            hourFeaturePair[hour] = featureList


        # Step 4: Create csv files
        csvGenerator = Csvgenerator.CsvGenerator(hourFeaturePair)
        csvGenerator.generate_standardized_data()
        csvGenerator.genrate_csv()

        c = 20