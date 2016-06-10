from os import listdir
from os.path import isfile, join
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn import svm, linear_model

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import sys
import re

class Predict:

    def __init__(self):
        """ initialize the path of all the folder and files to be used """

        print '-'*60
        
        self.train_folder = '../data_eval/new_train_clean/' # folder
        self.test_folder = '../data_eval/new_test_clean/' # folder
        self.label_file = '../data_eval/new_train_labels.csv' # path

        self.pred_file = '..data_eval/result/submission.csv'

        self.train_ans = []
        self.test_index = []

    def get_labels(self):
        """ get train_labels.csv and return a dictionary """

        print 'Loading label data from', self.label_file, '...'
        labels = {}
        with open(self.label_file, 'rb') as f:
            f.next() # skip header line
            for line in f:
                index, answer = line.rstrip('\n').split(',')
                labels[index] = answer

        return labels

    def get_training_data(self):
        """ get training data and return a list, in which an item is the content of a document """
        labels = self.get_labels()

        print 'Loading training data from ', self.train_folder , '...'
        train_index = []
        #train_ans = []
        train_text = []
        cnt = 0

        for f in listdir(self.train_folder):
            file_path = join(self.train_folder, f)
            if isfile(file_path):
                cnt += 1
                if cnt % 10000 == 0:
                    print 'finished:', cnt # line counter
                #train_index.append(f[:-4])
                self.train_ans.append(labels[f[:-4]])
                with open(file_path, 'rb') as f:
                    train_text.append( f.read() )

        return train_text

    def get_testing_data(self):
        """ get testing data and return a list, in which an item is the content of a document """

        print 'Loading testing data ', self.test_folder , '...'
        test_text = []
        cnt = 0

        for f in listdir(self.test_folder):
            file_path = join(self.test_folder, f)
            if isfile(file_path):
                cnt += 1
                if cnt % 10000 == 0:
                    print 'finished:', cnt # line counter
                self.test_index.append(f[:-4])
                with open(file_path, 'rb') as f:
                    test_text.append( f.read() )

        return test_text

    def get_tfidf_vectors(self):
        """ initialize vectorizer and return 'training vector' and 'testing vector' """

        train_text = self.get_training_data()
        test_text = self.get_testing_data()

        print 'Initilizing tf vectorizer ...'
        vectorizer = TfidfVectorizer(lowercase = True, smooth_idf=True, stop_words='english')
        vectorizer.fit( train_text + test_text )

        print 'Transforming data to tfidf vector ...'
        train_vec = vectorizer.transform(train_text)
        #print len(vectorizer.get_feature_names())
        test_vec = vectorizer.transform(test_text)

        return train_vec, test_vec

    def get_classifier(self):
        """ build classifier and fit all the data into it"""

        print 'Building Multinomial Naive Bayes classifier ...'
        #clf =  MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
        clf = BernoulliNB(alpha=0.28)

        #print 'build Suport Vector Machine classifier ...'''
		#clf = svm.SVC(kernel='rbf', probability=True, tol=0.1)
        #clf = svm.SVC(C=0.5, kernel='linear', probability=True, tol=0.1, max_iter=100, decision_function_shape='ovr')

        #print 'build Stochastic gradient descent classifier...'''
        #clf = linear_model.SGDClassifier(alpha=0.0002 ,loss="log", n_iter=8)

        return clf

    def predict(self):
        """ make predictions and store them into submission.csv """
        train_vec, test_vec = self.get_tfidf_vectors()
        clf = self.get_classifier()

        print '-'*40
        print 'Making predictions ...'
        clf.fit(train_vec, self.train_ans)
        clf_predictions = clf.predict_proba(test_vec)

        print 'Storing predictions in', self.pred_file
        pred_out = ["Id,predictions"]
        num_pred = range(30)
        for fid, pred in zip(self.test_index, clf_predictions):
            top_rec = sorted(num_pred, key=lambda k: pred[k], reverse=True)[:3]
            pred_out.append("%s,%s" % (fid, ' '.join( [clf.classes_[rec] for rec in top_rec] )))
        with open(self.pred_file, 'w') as f:
            f.write('%s\n' % ('\n'.join(pred_out)))

if __name__ == '__main__':
    p = Predict()
    #p.get_tfidf_vectors()
    p.predict()
