
import Files

import QPHelperClass as QPHC

import QPCsvgenerator

import APHelperClass as APHC

import APCsvgenerator

import ScoreClassifier as SC

"""
Main Function
"""
def predictQuestionQuality(postType):

    #Step 1. Parse all the input files
    print(Files.InputFiles)

    helperObj = QPHC.HelperClass()

    for file in Files.InputFiles.keys():
        try:
            helperObj.ParseFile(Files.InputFiles[file], file )

        except:
            print("Error Parsing File")


    helperObj.PairCommentWithPosts()


    #Step 2. Create Question Answer Pairs
    questionAnswerPairs = helperObj.CreateQuestionAnswerPair()

    # Step 3. We have created Q/A pairs. Now we need to extract the features.
    #hourList = [1, 6, 12, 24]
    hourList = [24]
    hourFeaturePair = {}
    for hour in hourList:
        helperObj.CreateLabels()
        featureList = helperObj.ExtractAllFeatures(hour)
        hourFeaturePair[hour] = featureList


    # Step 4: Create csv files
    csvGenerator = QPCsvgenerator.CsvGenerator(hourFeaturePair)
    csvGenerator.generate_standardized_data(postType)
    csvGenerator.genrate_csv(postType)

    c = 20

def predictAnswerQuality(postType):

    #Step 1. Parse all the input files
    print(Files.InputFiles)

    helperObj = APHC.HelperClass()

    for file in Files.InputFiles.keys():
        try:
            helperObj.ParseFile(Files.InputFiles[file], file )

        except:
            print("Error Parsing File")


    helperObj.PairCommentWithPosts()


    #Step 2. Create Question Answer Pairs
    questionAnswerPairs = helperObj.CreateQuestionAnswerPair()

    # Step 3. We have created Q/A pairs. Now we need to extract the features.
    #hourList = [1, 6, 12, 24]
    hourList = [24]
    hourFeaturePair = {}
    for hour in hourList:
        helperObj.CreateLabels()
        featureList = helperObj.ExtractAllFeatures(hour)
        hourFeaturePair[hour] = featureList


    # Step 4: Create csv files
    csvGenerator = APCsvgenerator.CsvGenerator(hourFeaturePair)
    csvGenerator.generate_standardized_data(postType)
    csvGenerator.genrate_csv(postType)

    c = 20


def QAQuality():
    #Call main function
    predictQuestionQuality('Q')
    print("End")
    SC.scoreClassifier('Q', 17)
	
	
    #Call main function
    predictAnswerQuality('A')
    print("End")
    SC.scoreClassifier('A', 14)
    print("Done")