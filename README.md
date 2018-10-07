# Movie Review Ranking and Sentiment Predictions (Turkish)

In this project, the aim is to predict users' ranking (0 to 5) and sentiments(positive/negative) over their reviews which are written in Turkish.

**Dataset**:

Dataset is created by scraping beyazperde.com (Turkish movie review site). By using beautifulsoup library, around 35k review-ranking pair are downloaded to excel file (ReviewAndRatings.xlsx).

**Methods:**

- **Data preprocessing**: While scraping movie review website, data processing was necessary because of Turkish characters (i,ü,ö,ç,ğ), punctuation marks etc. **DatasetGenerationAndPreprocessing.py** file is attached to the project for information purposes. You do not need to run it.

 - **Word2Vec** : This method is used to generate vector representation of the sentences. A corpus is created by using all of the reviews to train this model. (corpus :review_all.txt)

	To learn more : [W2V](https://radimrehurek.com/gensim/models/word2vec.html)

- **Ranking and Sentiment Prediction** : SVC and MLP models by [scikit-learn](http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC) is implemented.  Performances are discussed in the notebook.
