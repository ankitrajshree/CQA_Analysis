
import Files

import HelperClass as HC

import Csvgenerator

"""
Main Function
"""
def main():

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
    hourList = [1,2,3,4,5,6,7,8,9,10,11,12]
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


if __name__ == "__main__":
    #Call main function
    main()
    print("End")