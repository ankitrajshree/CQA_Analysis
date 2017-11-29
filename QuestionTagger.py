from sqlalchemy.sql.functions import coalesce

import HelperClass as HC
import MLStripper as mls
import html.parser as ht
import nltk
from nltk.stem import WordNetLemmatizer
import pandas as pd
import numpy as np
import Files
import math

class QuestionTagger:

    #Default Constructor
    def __init__(self):
        self.helperObj = HC.HelperClass()
        self.htmlstrip = mls.MLStripper()
        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.coOccMatrixBody = None
        self.coOccMatrixTitle = None
        self.wordList = None
        self.tagsList = None
        self.tagsPrior = None
        self.baseLevel = None
        self.strengthAssoBody = None
        self.strengthAssoTitle = None
        self.scaledEntropyBody = None
        self.scaledEntropyTitle = None
        self.weightBody = 1.75
        self.weightTitle = 0.93
        self.attentionWeightBody = None
        self.attentionWeightTitle = None
        self.tagActivationWeight = None

    def applyGivenTotals(self, rowOrColumn, rowOrColumnTotals, rowOrColumnName):
        return rowOrColumn/float(rowOrColumnTotals[rowOrColumnName])
    
    def applyLog(self, value):
        if (value==0):
            return 0
        else:
            return math.log10(value)
        
    def piLogpi(self, value):
        if(value ==0):
            return 0
        else:
            return -value * math.log10(value)

    def loadFiles(self):
        for file in Files.InputFiles.keys():
            try:
                self.helperObj.ParseFile(Files.InputFiles[file], file)
                self.helperObj.setHCAttribute(file,self.helperObj.documentDict.get(file.lower()));
            except Exception as  inst :
                print(inst)
                print("Error Parsing File")

    #Strips the Html tags from the body of the post
    def stripHtmlTags(self,html):
        html = ht.unescape(html)
        self.htmlstrip.feed(html)
        return self.htmlstrip.get_data()

    #Creates the CoOccurance matrix between words of post and tags
    def createCoOccurMat(self,):
        co_occurence_matrix_body = {key: {} for key in self.tagsList}
        co_occurence_matrix_title = {key: {} for key in self.tagsList}
        for post in self.helperObj.Posts:
            if (post.Tags is None):
                continue
            if (post.PostTypeId == 2):
                continue
            tagsForPost = post.Tags.split("><")
            tagsForPost[0] = tagsForPost[0].lstrip("<")
            tagsForPost[-1] = tagsForPost[-1].rstrip(">")
            body = self.stripHtmlTags(post.Body)
            bodyTokens = nltk.word_tokenize(body)
            for token in bodyTokens:
                lem_token = self.wordnet_lemmatizer.lemmatize(token)
                for question_tag in tagsForPost:
                    present_value = (co_occurence_matrix_body.get(question_tag)).get(lem_token, 0)
                    present_value = present_value + 1
                    co_occurence_matrix_body[question_tag][lem_token] = present_value
            titleTokens = nltk.word_tokenize(post.Title)
            for token in titleTokens:
                lem_token = self.wordnet_lemmatizer.lemmatize(token)
                for question_tag in tagsForPost:
                    present_value = (co_occurence_matrix_title.get(question_tag)).get(lem_token, 0)
                    present_value = present_value + 1
                    co_occurence_matrix_title[question_tag][lem_token] = present_value
        co_occurence_body_df = pd.DataFrame(co_occurence_matrix_body)
        co_occurence_body_df = co_occurence_body_df.fillna(0)
        self.coOccMatrixBody = co_occurence_body_df;
        co_occurence_title_df = pd.DataFrame(co_occurence_matrix_title)
        co_occurence_title_df = co_occurence_title_df.fillna(0)
        self.coOccMatrixTitle = co_occurence_title_df

        pass

    #Strength Association of the words
    def getStrengthAssoc(self,coOccDf):
        co_occurence_total = coOccDf.sum().sum()
        rowTotals = coOccDf.sum(axis=1)
        columnTotals = coOccDf.sum(axis=0)
        coOccDf = coOccDf * 1.0
        colApplied = coOccDf.apply(lambda column:self.applyGivenTotals(column, columnTotals, column.name), axis=0)
        rowApplied = colApplied.apply(lambda row:self.applyGivenTotals(row, rowTotals, row.name), axis=1)
        rowApplied = rowApplied*float(co_occurence_total)
        strength_assoc = rowApplied.applymap(np.vectorize(self.applyLog))
        return strength_assoc
        pass

    #Base level of the Tag
    def getBaseLevel(self):
        tagFrequencies = [int(value.Count) for index, value in enumerate(self.helperObj.Tags)]
        totalFrequency = sum(tagFrequencies)
        tagPis = {}
        bi = {}
        for tag in self.helperObj.Tags:
            prob = float(tag.Count) / float(totalFrequency)
            tagbi = math.log10(prob / (1 - prob))
            tagPis[tag.TagName] = prob
            bi[tag.TagName] = tagbi
        self.baseLevel = bi;
        pass

    #Entropy of the word
    def getEntropy(self,coOccDf):
        entropy = {}
        rowTotals = coOccDf.sum(axis=1)
        rowApplied = coOccDf.apply(lambda row:self.applyGivenTotals(row, rowTotals, row.name), axis=1)
        unSummedPis = rowApplied.applymap(np.vectorize(self.piLogpi))
        entropy = unSummedPis.sum(axis=1).to_dict()
        entropyMax = max(entropy.values())
        scaledEntropy = {key: 1 - value / entropyMax for key, value in entropy.items()}
        return scaledEntropy
        pass
    
    #Gets the attentional activation of tags based on the words in the post
    def getAttenWeight(self,weight,scaledEntropy):
        tScaleEntpy = sum(scaledEntropy.values())
        attentionWeight = {key: (weight*value)/tScaleEntpy for key,value in scaledEntropy.items()}
        return attentionWeight

    #Gets the activation weights of the tags
    def getActWeights(self):
        wTitleValues = list(self.attentionWeightTitle.values())
        wBodyValues = list(self.attentionWeightBody.values())
        titleSums = (np.matrix(wTitleValues) * self.strengthAssoTitle.as_matrix()).tolist()[0]
        bodySums = (np.matrix(wBodyValues) * self.strengthAssoBody.as_matrix()).tolist()[0]
        titleTags = list(self.strengthAssoTitle.columns)
        bodyTags = list(self.strengthAssoBody.columns)
        titleSumsFinal = {titleTags[index]:value for index, value in enumerate(titleSums)}
        bodySumsFinal = {bodyTags[index]:value for index, value in enumerate(bodySums)}
        dicts = [titleSumsFinal, bodySumsFinal, self.baseLevel]
        activations = {concernedTag: sum(d[concernedTag] for d in dicts) for concernedTag in titleTags}
        self.tagActivationWeight = activations        

    #Method which processes all the model parameters
    def tagger(self):
        self.loadFiles()
        print("hey")
        self.tagsList = [value.TagName for index, value in enumerate(self.helperObj.Tags)]
        print("files loaded")
        self.createCoOccurMat()
        print("Co ouccurrence done")
        self.getBaseLevel()
        print("Base level done")
        self.scaledEntropyBody = self.getEntropy(self.coOccMatrixBody)
        self.scaledEntropyTitle = self.getEntropy(self.coOccMatrixTitle)
        print("Scaled entropy done")
        self.strengthAssoBody = self.getStrengthAssoc(self.coOccMatrixBody)
        self.strengthAssoTitle = self.getStrengthAssoc(self.coOccMatrixTitle)
        print("Strength Association done")
        self.attentionWeightBody = self.getAttenWeight(self.weightBody,self.scaledEntropyBody)
        self.attentionWeightTitle = self.getAttenWeight(self.weightTitle,self.scaledEntropyTitle)
        print("Attention weight done")
        self.getActWeights()
        print("Tag Activation",self.tagActivationWeight)


questagger=None
if __name__ =='__main__':
    questagger = QuestionTagger()
    print("hi")
    questagger.tagger()



