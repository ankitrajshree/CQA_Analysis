import Files
import HelperClass as HC
from numpy import  genfromtxt
import numpy as np
from sklearn.model_selection import train_test_split,KFold
from sklearn.linear_model import LogisticRegression as lr

from random import randint

class Longitivty(object):
    def __init__(self,X,Y,fold):
        self.X = genfromtxt(X,delimiter=',')
        self.Y = genfromtxt(Y,delimiter=',')
        self.fold = fold

    def kfold_validator(self):
        kf = KFold(n_splits=self.fold,shuffle=True)
        accuracy = 0.0
        for train_indeces,test_indeces in kf.split(X=self.X):
            X1_train = np.empty(shape =(0,8))
            y1_train = np.empty(shape= (0))
            X1_test = np.empty(shape=(0, 8))
            y1_test = np.empty(shape=(0, ))
            for index in train_indeces:
                X1_train = np.append(X1_train,[self.X[index]],axis=0)
                y1_train = np.append(y1_train,[self.Y[index]],axis=0)
            for index in test_indeces:
                X1_test = np.append(X1_test, [self.X[index]],axis=0)
                y1_test = np.append(y1_test, [self.Y[index]],axis=0)
            accuracy +=self.test(X1_train,y1_train,X1_test,y1_test)
        return accuracy/self.fold
        pass

    def split(self,X,Y,fold):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
        self.X,self.Y, test_size = fold, random_state = 1)

    def train(self,X,Y):
        lorgeg = lr()
        return lorgeg.fit(X,Y)

    def test(self,X_train,y_train,x_test,y_test):
        return self.train(X_train,y_train).score(x_test,y_test)


if __name__ =='__main__':
    for k in range(2,11):
        l = Longitivty('data_std.csv','label_std.csv',fold =k)
        print ("k value:"+str(k) +" accuracy: "+str(l.kfold_validator()))
    l = Longitivty('data.csv','label.csv',fold =k)