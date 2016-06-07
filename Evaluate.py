import sys

class Evaluate:
    def __init__(self):
        """ God Denffer"""
        self.src1 = './data/new_test_labels.csv'
        self.src2 = './submission.csv'
        print '-'*60

    def load_src1(self):
        """ load data from new_test_labels.txt and return index_list & gt_list """

        index_list = []
        gt_list = [] # gt_list stands for 'ground truth list
        print "Loading data from" + self.src1
#        lines =  sum(1 for line in open(self.src1))
        cnt = 0

        with open(self.src1, 'rb') as f:
            for line in f:
                cnt += 1
                index, gt = line.rstrip('\n').split(',')
                index_list.append(index)
                gt_list.append(gt)
                #print cnt
                sys.stdout.write("\rStatus: %s"%(cnt))
                sys.stdout.flush()

        return index_list[1:], gt_list[1:]

    def load_src2(self):
        """ load data from submission.txt and return index_list & pd_list """

        index_list = []
        pd_list = [] # pd_list stands for 'prediction list'

        print "\nLoading data from" + self.src2
        #lines =  sum(1 for line in open(self.src2))

        with open(self.src2, 'rb') as f:
            cnt = 0
            f.next() # skip header line
            for line in f:
                cnt += 1
                index, predictions = line.rstrip('\n').split(',')
                index_list.append(index)
                pd1, pd2, pd3 = predictions.strip('\n').split(' ')
                pd_list.append([pd1, pd2, pd3])

                sys.stdout.write("\rStatus: %s"%(cnt))
                sys.stdout.flush()

        return index_list, pd_list

    def run_eval(self):

        gt_index_list, gt_list = self.load_src1()
        pd_index_list, pd_list = self.load_src2()

        score = 0
        score_list = []

        print "\nEvaluating performance on" + self.src2
        for i in xrange(len(pd_index_list)):
            for j in xrange(len(gt_index_list)):
                if pd_index_list[i] == gt_index_list[j]:
                    if pd_list[i][0] == gt_list[j]:
                        score = 1
                    elif pd_list[i][1] == gt_list[j]:
                        score = 0.6
                    elif pd_list[i][2] == gt_list[j]:
                        score = 0.2
                    else:
                        score = 0
            sys.stdout.write("\rStatus: %s/%s"%(i+1,j+1))
            sys.stdout.flush()

            score_list.append(score)
        #print score_list
        avg_score = sum(score for score in score_list)/len(score_list)
        print "\nPerformance:", avg_score

if __name__ == '__main__':
    e = Evaluate()
    e.run_eval()



