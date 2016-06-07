from os import listdir
from os.path import isfile, join
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
# FIXME change your data path/folder here

class Predict:

    def __init__(self):
        """ initialize the path of all the folder and files to be used """

        print '-'*60
        self.train_folder = './data/new_train/' # folder
        self.test_folder = './data/new_test/' # folder
        self.label_file = './data/train_labels.csv' # path
        #pred_file = './submission_NB.csv' # predicitons
        self.pred_file = './submission.csv'

        self.train_ans = []
        self.test_index = []

    def get_labels(self):
        """ get train_labels.csv and return a dictionary """

        print 'Loading label data ...'
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

        print 'Loading training data ...'
        #train_index = []
        #train_ans = []
        train_raw = []
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
                    train_raw.append( f.read() )

        #return train_raw, train_index, train_ans
        return train_raw

    def get_testing_data(self):
        """ get testing data and return a list, in which an item is the content of a document """
        print 'Loading testing data ...'
        #test_index = []
        test_raw = []
        cnt = 0

        for f in listdir(self.test_folder):
            file_path = join(self.test_folder, f)
            if isfile(file_path):
                cnt += 1
                if cnt % 10000 == 0:
                    print 'finished:', cnt # line counter
                self.test_index.append(f[:-4])
                with open(file_path, 'rb') as f:
                    test_raw.append( f.read() )

        return test_raw

    def get_tfidf_vectors(self):
        """ initialize vectorizer and return 'training vector' and 'testing vector' """

        train_raw = self.get_training_data()
        test_raw = self.get_testing_data()

        print 'Initilizing tf vectorizer ...'
        vectorizer = TfidfVectorizer(lowercase = True, smooth_idf=True, stop_words='english')
        vectorizer.fit(train_raw+test_raw)

        print 'Transforming data to tfidf vector ...'
        train_vec = vectorizer.transform(train_raw)
        #print len(vectorizer.get_feature_names())
        test_vec = vectorizer.transform(test_raw)

        return train_vec, test_vec

    def get_classifier(self):
        """ build classifier and fit all the data into it"""

        print 'Building Multinomial Naive Bayes classifier ...'
        clf =  MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
        #clf = BernoulliNB()
        return clf

    def predict(self):
        """ make predictions and store them into submission.csv """
        train_vec, test_vec = self.get_tfidf_vectors()
        clf = self.get_classifier()

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
    p.predict()
