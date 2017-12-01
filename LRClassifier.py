from numpy import  genfromtxt
import numpy as np
from sklearn.model_selection import train_test_split,KFold
from sklearn.linear_model import LogisticRegression as lr

from random import randint

class LRClassifier(object):
    def __init__(self,X,Y,fold, shape):
        self.X = genfromtxt(X,delimiter=',')
        self.Y = genfromtxt(Y,delimiter=',')
        self.fold = fold
        self.shape = shape

    def kfold_validator(self):
        kf = KFold(n_splits=self.fold,shuffle=True)
        accuracy = 0.0
        coeff = np.zeros(shape=(1,self.shape))
        for train_indeces,test_indeces in kf.split(X=self.X):
            X1_train = np.empty(shape =(0,self.shape))
            y1_train = np.empty(shape= (0, ))
            X1_test = np.empty(shape=(0,self.shape))
            y1_test = np.empty(shape=(0, ))
            for index in train_indeces:
                X1_train = np.append(X1_train,[self.X[index]],axis=0)
                y1_train = np.append(y1_train,[self.Y[index]],axis=0)
            for index in test_indeces:
                X1_test = np.append(X1_test, [self.X[index]],axis=0)
                y1_test = np.append(y1_test, [self.Y[index]],axis=0)

            lr, lrCoeff = self.train(X1_train,y1_train)
            coeff = (coeff + lrCoeff)

            accuracy +=self.test(lr,X1_test,y1_test)

        return [accuracy/self.fold, coeff/self.fold]
        pass

    def split(self,X,Y,fold):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
        self.X,self.Y, test_size = fold, random_state = 1)

    def train(self,X,Y):
        logreg = lr()
        logreg.fit(X,Y)
        return [logreg, logreg.coef_]

    def test(self,lr,x_test,y_test):
        return lr.score(x_test,y_test)


