import os
from os import listdir
from os.path import isfile, join
import sys
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

class PreProcess:

    def __init__(self):
        """ initialize the path of all the folder and files to be used """

        print '-'*60
        self.train_folder = './data/train/'
        self.test_folder = './data/test/'
        self.train_clean_folder = './data/train_clean/'
        self.test_clean_folder = './data/test_clean/'

        self.mood_file = './data/moods_mapping.txt'
        self.emoticons_file = './data/emoticons.txt'

    def create_dir(self):
        """ create folder if not found """
        dir1 = os.path.dirname(self.train_clean_folder)
        dir2 = os.path.dirname(self.test_clean_folder)

        if not os.path.exists(dir1):
            os.makedirs(dir1)
        if not os.path.exists(dir2):
            os.makedirs(dir2)

    def get_training_data(self):
        """ get training data and return a list, in which an item is the content of a document """

        print 'Loading training data from ', self.train_folder, '...'
        train_index = []
        train_raw = []
        cnt = 0

        for f in listdir(self.train_folder):
            file_path = join(self.train_folder, f)
            if isfile(file_path):
                cnt += 1
                if cnt % 10000 == 0:
                    print 'finished:', cnt # line counter
                train_index.append(f[:-4])
                with open(file_path, 'rb') as f:
                    train_raw.append( f.read() )

        return train_index, train_raw

    def get_testing_data(self):
        """ get testing data and return a list, in which an item is the content of a document """

        print 'Loading testing data from ', self.test_folder, '...'
        test_index = []
        test_raw = []
        cnt = 0

        for f in listdir(self.test_folder):
            file_path = join(self.test_folder, f)
            if isfile(file_path):
                cnt += 1
                if cnt % 10000 == 0:
                    print 'finished:', cnt # line counter
                test_index.append(f[:-4])
                with open(file_path, 'rb') as f:
                    test_raw.append( f.read() )

        return test_index, test_raw

    def get_moods(self):
        """ get mood_mappings.txt and return a list of moods """
        moods = []
        print 'Loading', self.mood_file

        with open(self.mood_file, 'rb') as f:
            f.next() # skip header line
            for line in f:
                index, mood = line.rstrip('\n').split(',')
                moods.append(mood)

        return moods

    def get_emoticons(self):
        """ get emoticons.txt and return a list of emoticons """
        emoticons = []
        print 'Loading', self.emoticons_file

        #uni2ascii = {ord('\xe2\x80\x91'.decode('utf-8')): ord("-")}
        with open(self.emoticons_file, 'rb') as f:
            for line in f:
                emoticons = line.rstrip('\n').split(' ')
            for e in emoticons:
                print e.encode('ascii', 'ignore')
                #e.decode('utf-8').translate(uni2ascii).encode('ascii')
        print emoticons
        return emoticons

    def clean_html(self,raw):
        """ clean html tags & css & javascript"""

        text_list = []
        for text in raw:
            text = re.sub(r'^https?:\/\/.*[\r\n]*', ' ', text, flags=re.MULTILINE)
            soup = BeautifulSoup(text, 'html.parser') # create a new bs4 object from the html data loaded
            for script in soup(["script", "style"]): # remove all javascript and stylesheet code
                script.extract()
            # get text
            text = soup.get_text()
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            text_list.append(text)

        #print text_list
        return text_list

    def clean(self,raw, moods):
        """ remove whatever crap it is in the text """

        text_list = []
        stemmer = SnowballStemmer("english")
        stop_words = stopwords.words('english')

        print "Cleaning ..."
        cnt = 0
        for text in raw:
            cnt += 1
            text = text.lower()
            for mood in moods:
                text = re.sub(r'%s' %(mood), (' ' + mood + ' ')*5, text)
            #for emoticon in emoticons:
             #   text = re.sub(r'%s' %(emoticon), (" "+emoticon+" "), text)
            #text = re.sub(r'<.*?>',' ', text)
            text = re.sub(r'\s_\s', ' ', text)
            text = re.sub("\d+", ' ', text)
            text = re.sub(r'[^\w\s]',' ',text)
            text = re.sub(r'\n', ' ', text)
            text = " ".join([stemmer.stem(word) for word in text.split(" ")])
            text = " ".join([i for i in text.split() if i not in stop_words])
            text = re.sub(r'\s+', ' ', text)

            text_list.append(text)

            sys.stdout.write('\rStatus: %s' %(cnt))
            sys.stdout.flush()

        print text_list
        #print ""
        return text_list

    def render(self):
        """ render files and put them in folder 'train_clean' & 'test_clean' """

        self.create_dir()
        moods = self.get_moods()
        #emoticons = self.get_emoticons()

        train_index, train_raw = self.get_training_data()
        test_index, test_raw = self.get_testing_data()
        train_clean =self.clean_html(train_raw)
        test_clean =self.clean_html(test_raw)
        train_clean = self.clean(train_clean, moods)
        test_clean = self.clean(test_clean, moods)

        print "Putting files into", self.train_clean_folder
        for i in xrange(len(train_index)):
            f_name = train_index[i] + ".txt"
            f_path = self.train_clean_folder + f_name
            f1 = open(f_path, "w")
            f1.write('%s\n' %(train_clean[i]))
            f1.close()

            sys.stdout.write("\rStatus: %s"%(i+1))
            sys.stdout.flush()

        print "\nPutting files into", self.test_clean_folder
        for j in xrange(len(test_index)):
            f_name = test_index[j] + ".txt"
            f_path = self.test_clean_folder + f_name
            f2 = open(f_path, "w")
            f2.write('%s\n' %(test_clean[j]))
            f2.close()

            sys.stdout.write("\rStatus: %s"%(j+1))
            sys.stdout.flush()

        print ""

if __name__ == '__main__':
    p = PreProcess()
    p.render()
