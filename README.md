-----------------------------------------------------------------------------------------------------------------------------------------------
							**Learning from CQA Data**
							**Team No : 15**				
-----------------------------------------------------------------------------------------------------------------------------------------------

**1. Enviornment :**
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

**2. File Descriptions:**
	APCsvgenerator.py : CSV generator for answer quality prediction <br />
	APFeatures.py : Class to store features for answers quality prediction <br />
	APHelperClass.py : Helper class for answer quality prediction <br />
	APQuestionAnswer.py : For answer score prediction converts posts to questions and answers using post type id i.e question(id:1) or answer(id:2)<br />
	Badges.py : To store data from badges.xml file <br />
	CQAAnalysis.py : Main script to run the program.(Entry point)<br />
	Comments.py : To store data from comments.xml file <br />
	Csvgenerator.py : To generate CSV data to predict long term value of questions<br />
	Features.py : To store features for long term value <br />
	Files.py : To map the xml files. <br />
	GraphPlotting.py : To plot the accuracy graphs for long term value prediction<br />
	HelperClass.py : It contains helper functions for long term value prediction <br />
	LRClassifier.py : Logistic Regression for QA score prediction and long term value prediction.<br />
	LongTermValue.py : Entry point for long term value prediction called by CQAAnalysis.py<br />
	MLPClassifier.py : Multi Layer Perceptron for QA score prediction.<br />
	MLStripper.py : Strips html tags and code fragments.<br />
	NBClassifier.py :  Naive Bayes Classifier for QA score prediction and long term value prediction.<br />
	PostHistory.py : To store data from posthistory.xml file <br />
	PostLinks.py : To store data from postlinks.xml file <br />
	Posts.py : To store data from posts.xml file <br />
	PredictQuestionAnswerQuality.py : Entry point for Question Answer score prediction called by CQAAnalysis.py<br />
	QPCsvgenerator.py : CSV generator for question quality prediction<br />
	QPFeatures.py : To store features for question quality prediction<br />
	QPHelperClass.py : Helper class for question quality prediction<br />
	QPQuestionAnswer.py : For Question score prediction converts posts to questions and answers using post type id i.e question(id:1) or answer(id:2)<br />
	QuestionAnswer.py : For Long term value prediction, converts posts to questions and answers using post type id i.e question(id:1) or answer(id:2)<br />
	QuestionTagger.py : Tag prediction model <br />
 	SVMClassifier.py : Support Vector Machines Classifier for QA score prediction and long term value prediction.<br />
	ScoreClassifier.py : Used for question answer score prediction using multiple models.<br />
	Tags.py : To store data from tags.xml file<br />
	Users.py : To store data from users.xml file<br />
	ViewCountClassifier.py : Used for long term value prediction using multiple models.<br />
	Votes.py : To store data from votes.xml file<br />
	<br/>
	<br/>
**3. Using the program :**
   1. Unzip CQA_Analysis.zip.<br/>
   2. Change directory to CQA_Analysis<br/>
   4. Make sure these folders exist.<br/>
	 a. Data/ai.stackexchange.com<br/>
	 b. CSV Files<br/>
	 c. CSV Files_A<br/>
	 d. CSV Files_Q<br/>
	 e. Images_LTV<br/>
	 f. Images_A<br/>
	 g. Images_Q<br/>
   5. $python3 CQAAnalysis.py<br/>
<br/>
<br/>

**4. Expected output: **
   Following the above instructions the program will train the data and test and create the following accuracy graphs

**5. Results: **
     The results are in the form of graphs generated from the analysis which are added in the images folder.<br/>
	1. Images\Logistic RegressionClassifier.png : Accuracy vs time for Long term value prediction using Logistic Regression<br/>
	2. Images\Support vector machinesClassifier.png : Accuracy vs time for Long term value prediction using SVM.<br/>
	3. Images\Navie BayesClassifier.png : Accuracy vs time for Long term value prediction using Naive Bayes<br/>
	4. Images_Q\Accuracy.PNG: Performance of differnt models for Question score prediction<br/>
	5. Images_Q\MLP_Classifier.png :Accuracy vs k value of k-fold for Question score prediction using MLP<br/>
	6. Images_Q\Gaussian_Naive_Bayes.png : Accuracy vs k value of k-fold for Question score prediction using GNB<br/>
	7. Images_Q\Support_Vector_Machine.png : Accuracy vs k value of k-fold for Question score prediction using SVM<br/>
	8. Images_Q\Logistic_Regression.png : Accuracy vs k value of k-fold for Question score prediction using LR<br/>
	9. Images_Q\coefficient.PNG : Coefficents for each features in LR for Question score prediction<br/>
	10. Images_A\Accuracy.PNG: Performance of differnt models for Answer score prediction<br/>
	11. Images_A\MLP_Classifier.png :Accuracy vs k value of k-fold for Answer score prediction using MLP<br/>
	12. Images_A\Gaussian_Naive_Bayes.png : Accuracy vs k value of k-fold for Answer score prediction using GNB<br/>
	13. Images_A\Support_Vector_Machine.png : Accuracy vs k value of k-fold for Answer score prediction using SVM<br/>
	14. Images_A\Logistic_Regression.png : Accuracy vs k value of k-fold for Answer score prediction using LR<br/>
	15. Images_A\coefficient.PNG : Coefficents for each features in LR for Answer score prediction<br/>
