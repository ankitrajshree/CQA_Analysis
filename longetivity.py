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
        '''CODE TO BE MODIFIED
        kf = KFold(n_splits=self.fold,shuffle=True)
        accuracy = 0.0
        for train_indeces,test_indeces in kf.split(X=self.X):
            X1_train = np.empty(shape =(0,8))
            y1_train = np.empty(shape= (0,))
            X1_test = np.empty(shape=(0, 8))
            y1_test = np.empty(shape=(0, ))
            for index in train_indeces:
                np.append(X1_train,[self.X[index]],axis=0)
                np.append(y1_train,[self.Y[index]],axis=0)
            for index in test_indeces:
                np.append(X1_test, [self.X[index]],axis=0)
                np.append(y1_test, [self.Y[index]],axis=0)
            accuracy +=self.test(X1_train,y1_train,X1_test,y1_test)

        return accuracy/self.fold
        '''
        pass

    # def split(self,X,Y,fold):
    #     self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
    #     self.X,self.Y, test_size = fold, random_state = 1)

    def train(self,X,Y):
        # self.split(self.X,self.Y,fold=self.fold)
        lorgeg = lr()
        return lorgeg.fit(X,Y)

    def test(self,X_train,y_train,x_test,y_test):
        return self.train(X_train,y_train).score(x_test,y_test)

    # def test_1(self):
    #     ind = randint(0,self.X_test.shape[0])
    #     print(repr(ind))
    #     print (self.X_test[ind])

        return self.train().predict([self.X_test[ind]])
if __name__ =='__main__':
    l = Longitivty('data.csv','label.csv',fold =10)
    l.kfold_validator()
