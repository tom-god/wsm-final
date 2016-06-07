import os
from os import listdir
from os.path import isfile, join
import random
import shutil
import sys

class PreProcess:
    def __init__(self):
        """ """
        self.src = './data/train/'
        self.src_label = './data/train_labels.csv'
        self.dst1 = './data/new_test/'
        self.dst2 = './data/new_train/'

        self.dst3 = './data/new_test_labels.csv'
        self.dst4 = './data/new_train_labels.csv'

        self.test_num = 18000

    def create_dir(self):
        """ create folder if not found """
        dir1 = os.path.dirname(self.dst1)
        dir2 = os.path.dirname(self.dst2)

        if not os.path.exists(dir1):
            os.makedirs(dir1)
        if not os.path.exists(dir2):
            os.makedirs(dir2)

    def split(self):

        self.create_dir()
        print '-'*60
        print "Loading files from", self.src
        src_files = []
        cnt = 0
        for fname in os.listdir(self.src):
            filepath = join(self.src, fname)
            if isfile(filepath):
                cnt += 1
                src_files.append(fname)

            sys.stdout.write("\rStatus: %s"%(cnt))
            sys.stdout.flush()

        print "\nRandomly picking files from", self.src
        dst_files = random.sample(src_files, self.test_num)
        #print dst_files

        print "Putting randomed files into", self.dst1, "and", self.dst2
        cnt = 0
        for filename in src_files:
            cnt += 1
            if filename in dst_files:
                shutil.copy(os.path.join(self.src, filename), self.dst1)
            else:
                shutil.copy(os.path.join(self.src, filename), self.dst2)

            sys.stdout.write("\rStatus: %s"%(cnt))
            sys.stdout.flush()

        #print dst_files
        return dst_files

    def render(self):

        dst_files = self.split()
        dst_indexes = [ f[:-4] for f in dst_files ]
        #print dst_indexes
	label = {}
        index_list = []
        answer_list = []

        print "\nLoading data from", self.src_label
        #lines = sum(1 for line in open(self.src_label))

        f = open(self.src_label, 'rb')
        cnt = 0
        for line in f:
            cnt += 1
            index, answer = line.rstrip('\n').split(',')
            index_list.append(index)
            answer_list.append(answer)

            sys.stdout.write("\rStatus: %s"%(cnt))
            sys.stdout.flush()

        index_list = index_list[1:]
        answer_list = answer_list[1:]

        print "\nMatching indexes and writing 'index, ground truth' into", self.dst3, "&", self.dst4

        f1 = open(self.dst3, "w") # './data/new_test_labels.csv'
        f2 = open(self.dst4, "w") # './data/new_train_labels.csv'
        row1 = ["file_index,ground_truth"]
        row2 = ["file_index,ground_truth"]

        for i in xrange(len(index_list)):
            if index_list[i] in dst_indexes:
                row1.append(index_list[i] + "," + answer_list[i])
            else:
                row2.append(index_list[i] + "," + answer_list[i])
                #row2.append("%s,%s") % (index_list[i], answer_list[i])
                #f2.write("file_index","ground_truth")
                #f2.write(str(index_list[i]) + "," + str(answer_list[i]) + "\n")

            sys.stdout.write("\rStatus: %s"%(i+1))
            sys.stdout.flush()

        f1.write('%s\n' %  ('\n'.join(row1)))
        f2.write('%s\n' %  ('\n'.join(row2)))

        f1.close()
        f2.close()

        print ""

if __name__ == '__main__':
    p = PreProcess()
    p.render()


