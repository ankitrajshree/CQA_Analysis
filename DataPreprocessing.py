
import Files

import HelperClass as HC

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


    #Step 2. Create Question Answer Pairs
    questionAnswerPairs = helperObj.CreateQuestionAnswerPair()




if __name__ == "__main__":
    #Call main function
    main()
    print("End")