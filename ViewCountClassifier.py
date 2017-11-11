
from LRClassifier import  LRClassifier
def main():
    for k in range(2,11):
        l = LRClassifier('data_std.csv','label_std.csv',fold =k)
        print ("k value:"+str(k) +" accuracy: "+str(l.kfold_validator()))

if __name__ =='__main__':
    main()