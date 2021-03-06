
from LRClassifier import  LRClassifier
from SVMClassifier import  SVMClassifier
from NBClassifier import NBClassifier

import GraphPlotting

def vcClassifier(postType, featureDimension):

    gp = GraphPlotting.GraphPlot()

    hours = [1,6,12,24]
    graph_list= []
    #LR
    for hour in hours:
        acc_list = []
        print("For Hour: "+str(hour))
        for k in range(2,11):
            l = LRClassifier('CSV Files/data_std_hr'+str(hour)+'.csv','CSV Files/label_std_hr'+str(hour)+'.csv', k, featureDimension)
            acc_list.append(l.kfold_validator()[0])
        graph_list.append((hour,acc_list))
    gp.PlotGraph(graph_list, "Hours", "Accuracy", "Logistic Regression", postType)

    #SVM
    grap_list =[]
    for hour in hours:
        acc_list =[]
        print("For Hour: "+str(hour))
        for k in range(2,11):
            l = SVMClassifier('CSV Files/data_std_hr'+str(hour)+'.csv','CSV Files/label_std_hr'+str(hour)+'.csv', k, featureDimension)
            acc_list.append(l.kfold_validator())
        grap_list.append((hour,acc_list))
    gp.PlotGraph(grap_list, "Hours", "Accuracy", "Support vector machines", postType)

    #NB
    graph_list=[]
    for hour in hours:
        acc_list =[]
        print("For Hour: "+str(hour))
        for k in range(2,11):
            l = NBClassifier('CSV Files/data_std_hr'+str(hour)+'.csv','CSV Files/label_std_hr'+str(hour)+'.csv', k, featureDimension)
            acc_list.append(l.kfold_validator())
        graph_list.append((hour,acc_list))
    gp.PlotGraph(graph_list,"Hours", "Accuracy", "Navie Bayes", postType)
