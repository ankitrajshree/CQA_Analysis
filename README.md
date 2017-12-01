-----------------------------------------------------------------------------------------------------------------------------------------------
							Learning from CQA Data
							Team No : 15				
-----------------------------------------------------------------------------------------------------------------------------------------------

1. Enviornment :
    Python version : 3.6.1
    Anaconda version : 4.4.0 
    Modules required to run the program:	
	 a. numpy
	 b. scikit
	 c. nltk
	 d. pandas
	 e. matplotlib
	 f. re
	 g. statistics
	 h. math

2. File Descriptions:
	APCsvgenerator.py : CSV generator for answer quality prediction __
	APFeatures.py : Class to store features for answers quality prediction __
	APHelperClass.py : Helper class for answer quality prediction __
	APQuestionAnswer.py : For answer score prediction converts posts to questions and answers using post type id i.e question(id:1) or answer(id:2)
	Badges.py : To store data from badges.xml file 
	CQAAnalysis.py : Main script to run the program.(Entry point)
	Comments.py : To store data from comments.xml file 
	Csvgenerator.py : To generate CSV data to predict long term value of questions
	Features.py : To store features for long term value 
	Files.py : To map the xml files. 
	GraphPlotting.py : To plot the accuracy graphs for long term value prediction
	HelperClass.py : It contains helper functions for long term value prediction 
	LRClassifier.py : Logistic Regression for QA score prediction and long term value prediction.
	LongTermValue.py : Entry point for long term value prediction called by CQAAnalysis.py
	MLPClassifier.py : Multi Layer Perceptron for QA score prediction.
	MLStripper.py : Strips html tags and code fragments.
	NBClassifier.py :  Naive Bayes Classifier for QA score prediction and long term value prediction.
	PostHistory.py : To store data from posthistory.xml file 
	PostLinks.py : To store data from postlinks.xml file 
	Posts.py : To store data from posts.xml file 
	PredictQuestionAnswerQuality.py : Entry point for Question Answer score prediction called by CQAAnalysis.py
	QPCsvgenerator.py : CSV generator for question quality prediction
	QPFeatures.py : To store features for question quality prediction
	QPHelperClass.py : Helper class for question quality prediction
	QPQuestionAnswer.py : For Question score prediction converts posts to questions and answers using post type id i.e question(id:1) or answer(id:2)
	QuestionAnswer.py : For Long term value prediction, converts posts to questions and answers using post type id i.e question(id:1) or answer(id:2)
	QuestionTagger.py : Tag prediction model 
 	SVMClassifier.py : Support Vector Machines Classifier for QA score prediction and long term value prediction.
	ScoreClassifier.py : Used for question answer score prediction using multiple models.
	Tags.py : To store data from tags.xml file
	Users.py : To store data from users.xml file
	ViewCountClassifier.py : Used for long term value prediction using multiple models.
	Votes.py : To store data from votes.xml file

3. Using the program :
   1. Unzip CQA_Analysis.zip.
   2. Change directory to CQA_Analysis
   4. Make sure these folders exist.
	 a. Data/ai.stackexchange.com
	 b. CSV Files
	 c. CSV Files_A
	 d. CSV Files_Q
	 e. Images_LTV
	 f. Images_A
	 g. Images_Q
   5. $python3 CQAAnalysis.py

4. Expected output:
   Following the above instructions the program will train the data and test and create the following accuracy graphs
	1. 
4. Results:
     The results are in the form of graphs generated from the analysis which are added in the images folder.
	1. Images\Logistic RegressionClassifier.png : Accuracy vs time for Long term value prediction using Logistic Regression
	2. Images\Support vector machinesClassifier.png : Accuracy vs time for Long term value prediction using SVM.
	3. Images\Navie BayesClassifier.png : Accuracy vs time for Long term value prediction using Naive Bayes
	4. Images_Q\Accuracy.PNG: Performance of differnt models for Question score prediction
	5. Images_Q\MLP_Classifier.png :Accuracy vs k value of k-fold for Question score prediction using MLP
	6. Images_Q\Gaussian_Naive_Bayes.png : Accuracy vs k value of k-fold for Question score prediction using GNB
	7. Images_Q\Support_Vector_Machine.png : Accuracy vs k value of k-fold for Question score prediction using SVM
	8. Images_Q\Logistic_Regression.png : Accuracy vs k value of k-fold for Question score prediction using LR
	9. Images_Q\coefficient.PNG : Coefficents for each features in LR for Question score prediction
	10. Images_A\Accuracy.PNG: Performance of differnt models for Answer score prediction
	11. Images_A\MLP_Classifier.png :Accuracy vs k value of k-fold for Answer score prediction using MLP
	12. Images_A\Gaussian_Naive_Bayes.png : Accuracy vs k value of k-fold for Answer score prediction using GNB
	13. Images_A\Support_Vector_Machine.png : Accuracy vs k value of k-fold for Answer score prediction using SVM
	14. Images_A\Logistic_Regression.png : Accuracy vs k value of k-fold for Answer score prediction using LR
	15. Images_A\coefficient.PNG : Coefficents for each features in LR for Answer score prediction
