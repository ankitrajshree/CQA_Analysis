#import matplotlib.pyplot

class GraphPlot:
    def __init__(self):
        pass

    def PlotGraph(self, hoursAccuracyTuplesList, xlabel, ylabel, classifier, postType):
        import matplotlib.pyplot as plt
        import numpy as np

        accuracies = None
        hourList = []
        for idx, hoursAccuracyTuples in enumerate(hoursAccuracyTuplesList):
            hour, AccuracyListFrom2Fold = hoursAccuracyTuples

            hourList.append(hour)

            if idx == 0:
                accuracies = np.array([AccuracyListFrom2Fold])
            else:
                accuracies = np.concatenate((accuracies, [AccuracyListFrom2Fold]), axis=0)

        averageAccuracies = np.average(accuracies, axis=0)

        indexOfMaxAvg = np.argmax(averageAccuracies)
        kValueForMaxAvg = indexOfMaxAvg + 2

        avgMaxAccuracies = np.array(
            [[accuracies[rowIndex][indexOfMaxAvg] for rowIndex in range(0, len(accuracies))]])
        maxHourIndex = np.argmax(avgMaxAccuracies)

        avgMaxAccuracies = avgMaxAccuracies * 100

        plt.plot(hourList, avgMaxAccuracies[0], c="red")

        plt.axis([0, 28, 30, 100])

        #plt.annotate('Best k-fold value ' + str(kValueForMaxAvg),
        #             xytext=(hourList[maxHourIndex]-3, avgMaxAccuracies[0][maxHourIndex] - 10),

        #             )

        plt.title(classifier + "K = " + str(kValueForMaxAvg) +": "+ xlabel + "_vs_" + ylabel)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig("Images_" + postType +"/"+classifier + "Classifier.png")
        plt._show()
        pass