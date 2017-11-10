
import Files

import HelperClass as HC
import MLStripper
from html.parser import HTMLParser
import html as ht
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import EnglishStemmer
import math
#nltk.download('all')

"""
Main Function
"""
def main():

    #Step 1. Parse all the input files
    print(Files.InputFiles)

    helperObj = HC.HelperClass()
    wordnet_lemmatizer = WordNetLemmatizer()
    english_stemmer = EnglishStemmer()

    print("starting")
    for file in Files.InputFiles.keys():
        try:
            helperObj.ParseFile(Files.InputFiles[file], file )

        except Exception as e:
            print(e)
            print("Error Parsing File")
    helperObj.setHCAttribute("Posts", helperObj.documentDict.get("posts"))
    helperObj.setHCAttribute("Tags", helperObj.documentDict.get("tags"))

    tagsList = [value.TagName for index, value in enumerate(helperObj.Tags)]
    tagFrequencies = [int(value.Count) for index, value in enumerate(helperObj.Tags)]
    totalFrequency = sum(tagFrequencies)
    tagPis = {}
    bi = {}
    for tag in helperObj.Tags:
        prob = float(tag.Count)/float(totalFrequency)
        tagbi = math.log10(prob/(1-prob))
        tagPis[tag.TagName] = prob
        bi[tag.TagName] = tagbi

    print("finished bis")
    co_occurence_matrix = {key: {} for key in tagsList}

    for post in helperObj.Posts:
        if (post.Tags is None):
            continue
        tagsForPost = post.Tags.split("><")
        tagsForPost[0] = tagsForPost[0].lstrip("<")
        tagsForPost[-1] = tagsForPost[-1].rstrip(">")
        bodyTokens = nltk.word_tokenize(post.Body)
        for token in bodyTokens:
            lem_token = wordnet_lemmatizer.lemmatize(token)
            for question_tag in tagsForPost:
                present_value = (co_occurence_matrix.get(question_tag)).get(lem_token, 0)
                present_value = present_value + 1
                co_occurence_matrix[question_tag][lem_token] = present_value
    co_occurence_df = pd.DataFrame(co_occurence_matrix)
    co_occurence_df = co_occurence_df.fillna(0)
    co_occurence_total = co_occurence_df.sum().sum()


    print("finished cooccur")
    rowTotals = co_occurence_df.sum(axis=1)
    columnTotals = co_occurence_df.sum(axis=0)

    sij = {key: {} for key in tagsList}
    for word in co_occurence_df.index:
        for tag in tagsList:
            rowTotal = rowTotals[word]
            columnTotal =columnTotals[tag]
            tempvalue = (co_occurence_df.loc[word][tag] * co_occurence_total)/float(rowTotal * columnTotal)
            if (tempvalue==0):
                sij[tag][word] = 0
            else:
                sij[tag][word] = math.log10(tempvalue)
    sij_df = pd.DataFrame(sij)
    sij_df = sij_df.fillna(0)

    print("hi")
    entropy = {}
    for word in co_occurence_df.index:
        totalEntropyForPost = 0
        for tag in tagsList:
            rowTotal = rowTotals[word]
            nji = co_occurence_df.loc[word][tag]
            if ((rowTotal>0) and (nji>0)):
                pIGivenJ = nji/float(rowTotal)
                totalEntropyForPost = totalEntropyForPost - pIGivenJ * math.log10(pIGivenJ)
        entropy[word] = totalEntropyForPost

    entropyMax = max(entropy.values())
    scaledEntropy = {key:1-value/entropyMax for key, value in entropy.items()}
    print(scaledEntropy)
#    print(co_occurence_df)




def strip_tags(html):
    parser = HTMLParser()
    html = ht.unescape(html)
    s = MLStripper.MLStripper()
    s.feed(html)
    return s.get_data()

if __name__ == "__main__":
    #Call main function
    main()
    print("End")