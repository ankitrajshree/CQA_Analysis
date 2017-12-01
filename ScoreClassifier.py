
from LRClassifier import  LRClassifier
from SVMClassifier import  SVMClassifier
from NBClassifier import NBClassifier
from MLPClassifier import MLPClassifier

import GraphPlotting
import matplotlib.pyplot as plt
import numpy as np

def scoreClassifier(postType, featureDimension):
    #MLP
    acc_list = []
    for k in range(2, 11):
        l = MLPClassifier('CSV Files_' + postType +'/data_std_hr24.csv', 'CSV Files_' + postType +'/label_hr24.csv', k , featureDimension)
        acc_list.append(l.kfold_validator())
    t = np.arange(2, 11, 1)
    plt.plot(t, acc_list, 'ro')
    plt.ylabel('accuracy')
    plt.xlabel('K-fold')
    plt.title('MLP Classifier')
    plt.savefig('Images_' + postType + "/"+"MLP_Classifier.png")
    plt.close()
    #plt.show()
    #LR
    acc_list = []
    avgCoeff = np.zeros(shape=(1,featureDimension))
    for k in range(2,11):
        l = LRClassifier('CSV Files_' + postType +'/data_std_hr24.csv', 'CSV Files_' + postType +'/label_hr24.csv',k, featureDimension)
        accuracy, lrCoeff = l.kfold_validator()
        acc_list.append(accuracy)
        avgCoeff = avgCoeff + lrCoeff

    avgCoeff /= 9
    print(avgCoeff)
    t = np.arange(2, 11, 1)
    plt.plot(t, acc_list, 'ro')
    plt.ylabel('accuracy')
    plt.xlabel('K-fold')
    plt.title('Logistic Regression')
    plt.savefig('Images_' + postType + "/" + "Logistic_Regression.png")
    plt.close()
    #plt.show()
    #SVM
    acc_list =[]
    for k in range(2,11):
        l = SVMClassifier('CSV Files_' + postType +'/data_std_hr24.csv', 'CSV Files_' + postType +'/label_hr24.csv',k, featureDimension)
        acc_list.append(l.kfold_validator())
    t = np.arange(2, 11, 1)
    plt.plot(t, acc_list, 'ro')
    plt.ylabel('accuracy')
    plt.xlabel('K-fold')
    plt.title('Support Vector Machine')
    plt.savefig('Images_' + postType + "/" + "Support_Vector_Machine.png")
    plt.close()
    #plt.show()
    #NB
    acc_list =[]
    for k in range(2,11):
        l = NBClassifier('CSV Files_' + postType +'/data_std_hr24.csv', 'CSV Files_' + postType +'/label_hr24.csv',k, featureDimension)
        acc_list.append(l.kfold_validator())
    t = np.arange(2, 11, 1)
    plt.plot(t, acc_list, 'ro')
    plt.ylabel('accuracy')
    plt.xlabel('K-fold')
    plt.title('Gaussian Naive Bayes')
    plt.savefig('Images_' + postType + "/" + "Gaussian_Naive_Bayes.png")
    plt.close()
    #plt.show()
