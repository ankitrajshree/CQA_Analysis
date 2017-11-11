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
        sij = {key: {} for key in self.tagsList}
        for word in coOccDf.index:
            for tag in self.tagsList:
                rowTotal = rowTotals[word]
                columnTotal = columnTotals[tag]
                tempvalue = (coOccDf.loc[word][tag] * co_occurence_total) / float(rowTotal * columnTotal)
                if (tempvalue == 0):
                    sij[tag][word] = 0
                else:
                    sij[tag][word] = math.log10(tempvalue)
        sij_df = pd.DataFrame(sij)
        sij_df = sij_df.fillna(0)
        return sij_df
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
        columnTotals = coOccDf.sum(axis=0)
        for word in coOccDf.index:
            totalEntropyForPost = 0
            for tag in self.tagsList:
                rowTotal = rowTotals[word]
                nji = coOccDf.loc[word][tag]
                if ((rowTotal > 0) and (nji > 0)):
                    pIGivenJ = nji / float(rowTotal)
                    totalEntropyForPost = totalEntropyForPost - pIGivenJ * math.log10(pIGivenJ)
            entropy[word] = totalEntropyForPost
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
        ais = {}
        for key in self.baseLevel:
            sumTitleW,sumBodyW = 0,0
            for attkey in self.attentionWeightTitle:
                sumTitleW += self.attentionWeightTitle[attkey] * self.strengthAssoTitle.loc[attkey][key]
            for attkey in self.attentionWeightBody:
                sumBodyW += self.attentionWeightBody[attkey] * self.strengthAssoBody.loc[attkey][key]
            ais[key] = self.baseLevel[key]+sumBodyW+sumTitleW
        self.tagActivationWeight = ais


    #Method which processes all the model parameters
    def tagger(self):
        self.loadFiles()
        self.tagsList = [value.TagName for index, value in enumerate(self.helperObj.Tags)]
        self.createCoOccurMat()
        #print("Co ouccurrence done")
        self.getBaseLevel()
        #print("Base level done")
        self.scaledEntropyBody = self.getEntropy(self.coOccMatrixBody)
        self.scaledEntropyTitle = self.getEntropy(self.coOccMatrixTitle)
        #print("Scaled entropy done")
        self.strengthAssoBody = self.getStrengthAssoc(self.coOccMatrixBody)
        self.strengthAssoTitle = self.getStrengthAssoc(self.coOccMatrixTitle)
        #print("Strength Association done")
        self.attentionWeightBody = self.getAttenWeight(self.weightBody,self.scaledEntropyBody)
        self.attentionWeightTitle = self.getAttenWeight(self.weightTitle,self.scaledEntropyTitle)
        #print("Attention weight done")
        self.getActWeights()
        #print("Tag Activation",self.tagActivationWeight)



if __name__ =='__main__':
    questagger = QuestionTagger()
    questagger.tagger()



