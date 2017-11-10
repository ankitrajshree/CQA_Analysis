import HelperClass as HC
import MLStripper as mls
import html.parser as ht
import nltk
from nltk.stem import WordNetLemmatizer
import pandas as pd
import numpy as np
import Files

class QuestionTagger:

    #Default Constructor
    def __init__(self):
        self.helperObj = HC.HelperClass()
        self.htmlstrip = mls.MLStripper()
        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.coOccMatrix = None
        self.wordList = None
        self.tagList = None;
        self.tagsPrior = None;
        self.baseLevel = None

    def loadFiles(self):
        for file in Files.InputFiles.keys():
            try:
                self.helperObj.ParseFile(Files.InputFiles[file], file)
                self.helperObj.setHCAAttribute(file,self.helperObj.documentDict.get(file.lower()));
            except:
                print("Error Parsing File")

    #Strips the Html tags from the body of the post
    def stripHtmlTags(self,html):
        html = ht.unescape(html)
        self.htmlstrip.feed(html)
        return self.htmlstrip.get_data()

    #Tokenize and lemmatize the words
    def getTokenLemma(self,sentence):
        tokens = nltk.word_tokenize(sentence)
        words = []
        for token in tokens:
            actWord = self.wordnet_lemmatizer.lemmatize(token)
            words.append(actWord);
        return words;

    #Creates the CoOccurance matrix between words of post and tags
    '''def createCoOccurMat(self,):
        #coOccurancematrix =
        self.coOccMatrix = coOccurancematrix;

        pass'''

    #Base level of the Tag
    def getBaseLevel(self):
        tagsprior = []
        baseLevel = []
        coOccMat = self.coOccMatrix;
        N = 100
        for i in range(self.coOccMatrix.shape[1]):
            sum = coOccMat[i].sum()
            prior = sum/float(N)
            tagsprior.append(prior)
            baseVal = np.log([prior/(1-prior)])
            baseLevel.append(baseVal)
        self.tagsPrior = pd.dataFrame(tagsprior)
        self.baseLevel = pd.dataFrame(baseLevel)
        pass

    #Entropy of the word
    def getEntropy(self):


        pass

    #Method which processes all the model parameters
    def tagger(self):
        self.loadFiles();
        for post in self.helperObj.Posts:
            body = post.Body
            body = body.replace('\n','').replace('\r','')
            proBody = self.stripHtmlTags(body)
            words = self.getTokenLemma(proBody)
            tags = post.Tags

if __name__ =='__main__':
    questagger = QuestionTagger()
    questagger.tagger()



