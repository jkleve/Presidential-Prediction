import csv
import numpy as np
import sexmachine.detector as gender
from sklearn import tree
import gender_detector
import time
import sys

NUM_FEATURES = 10

CANDIDATE_ID = 1
CANDIDATE_NAME = 2
CONTRIBUTOR_NAME = 3
CONTRIBUTOR_CITY = 4
CONTRIBUTOR_STATE = 5
CONTRIBUTOR_ZIP = 6
CONTRIBUTOR_EMPLOYER = 7
CONTRIBUTOR_OCCUPATION = 8
CONTRIBUTION_AMOUNT = 9
CONTRIBUTION_DATE = 10

DEMOCRATIC = 1
REPUBLICAN = 2
LIBERTARIAN = 3

# candidates 2008
CANDIDATES = {
    'P80003478': REPUBLICAN, # Mike Huckabee
    'P80000748': REPUBLICAN, # Ron Paul
    'P80003395': REPUBLICAN, # Duncan Hunter
    'P80003338': DEMOCRATIC, # Barack Obama
    'P80003411': DEMOCRATIC, # Bill Richardson
    'P00003186': REPUBLICAN, # Fred Dalton Thompson
    'P00003392': DEMOCRATIC, # Hillary Clinton
    'P80002983': REPUBLICAN, # John Cox
    'P40002347': DEMOCRATIC, # John Edwards
    'P00003251': REPUBLICAN, # Rudolph Giuliani
    'P80003353': REPUBLICAN, # Mitt Romney
    'P80003288': REPUBLICAN, # Sam Brownback
    'P60003795': REPUBLICAN, # Tommy Thomson
    'P80003429': REPUBLICAN, # Thomas Tancredo
    'P80000722': DEMOCRATIC, # Joe Biden
    'P80003387': DEMOCRATIC, # Chris Dodd
    'P80002801': REPUBLICAN, # John Mccain
    'P40002545': DEMOCRATIC, # Dennis Kucinich
    'P60004751': LIBERTARIAN # Mike Gravel
}

# FEC file names
FEC_FILES = {
    #'iowa':  'demographics/P00000001-IA.csv'
    'iowa':  'P00000001-IA.csv'
}

################################################
#
# Count number of samples in csv file
#
################################################
def count_samples(filename):
    i = 0
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            i += 1
    return (i-1) # remove 1 count b/c of first line

################################################
#
# Guess if occupation is a teacher
#
################################################
def is_teacher(s):
    s = s.lower()
    if "teacher" in s:
        #print("teacher in %s" % s)
        return 1
    #print("teacher not in %s" % s)
    return 0

################################################
#
# Guess if occupation is a farmer
#
################################################
def is_farmer(s):
    s = s.lower()
    if "farmer" in s:
        #print("farmer in %s" % s)
        return 1
    #print("farmer not in %s" % s)
    return 0

################################################
#
# Guess if occupation is retired
#
################################################
def is_retired(s):
    s = s.lower()
    if "retired" in s:    
        #print("retired in %s" % s)
        return 1
    #print("retired not in %s" % s)
    return 0

################################################
#
# Guess if person is unemployed
#
################################################
def is_unemployed(s):
    s = s.lower()
    if "unemployed" in s:
        #print("unemployed in %s" % s)
        return 1
    #print("unemployed not in %s" % s)
    return 0

################################################
#
# Guess if person is a student
#
################################################
def is_student(s):
    s = s.lower()
    if "student" in s:
        #print("student in %s" % s)
        return 1
    #print("student not in %s" % s)
    return 0

################################################
#
# Guess if person male
#
################################################
def is_male(s):
    try:
        s = s.lower().split(' ')[1]
    except IndexError:
        print("Failed to get first name. %s" % s)
    d1 = gender_detector.GenderDetector('us')
    try:
        g = d1.guess(s)
    except KeyError:
	print("Failed to get gender of name %s" % s)
    #print('name is %s' % s)
    #print('first detector guessed %s' % g)
    
    if g == 'male':
        #print('returning male')
        return 1
    elif g == 'female':
        #print('returning female')
        return 0

    # if first (faster) detector can't guess it
    # try second detector
    #print('going to detector 2')
    d2 = gender.Detector()
    g = d2.get_gender(s)
    if g == 'male':
        #print('male')
        return 1
    #print('female')
    return 0

################################################
#
# Check if v1 is greater than v2
#
################################################
def is_greater(v1, v2):
    if v1 > v2:
        #print("%f > %f" % (v1,v2))
        return 1
    #print("%f < %f" % (v1,v2))
    return 0

################################################
#
# Print 2D matrix
#
################################################
def print_matrix(matrix):
    s = matrix.shape
    n = s[0]
    m = s[1]
    mat_string = "["
    for i in range(0,n):
        row = "["
        for j in range(0,m):
            row += (" %d " % matrix[i][j])
        mat_string += row
    mat_string += "]"

################################################
#
# Get candidate
#
################################################
def get_candidate(candidate):
    party = CANDIDATES[candidate]
    #party = get_attr(CANDIDATES, candidate) 
    if party == DEMOCRATIC:
        return 1
    elif party == REPUBLICAN:
        return 2
    elif party == LIBERTARIAN:
        return 3
    else:
        return 4

################################################
#
# Get all features from file
#
################################################
def get_features(filename):
    n = count_samples(filename)
    print("%d number of lines" % n)
    m = NUM_FEATURES
    data = np.zeros(shape=(n,m+1)) # add 1 for y (output)
    print_matrix(data)
    i = -1 
    
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:

            if i >= 0 and i < n: # skip first line
                candidate = row[CANDIDATE_ID]
                occupation = row[CONTRIBUTOR_OCCUPATION]
                name = row[CONTRIBUTOR_NAME]
                try:
                    zip_code = int(row[CONTRIBUTOR_ZIP])
                except ValueError:
                    print("Couldn't convert %s to int" % row[CONTRIBUTOR_ZIP])
                    continue
                try:
                    amount = float(row[CONTRIBUTION_AMOUNT])
                except ValueError:
                    print("Couldn't convert %s to float" % row[CONTRIBUTION_AMOUNT])
                    continue

                data[i][0] = is_teacher(occupation)
                data[i][1] = is_farmer(occupation)
                data[i][2] = is_retired(occupation)
                data[i][3] = is_unemployed(occupation)
                data[i][4] = is_student(occupation)
                data[i][5] = is_greater(amount, 100.0)
                data[i][6] = is_greater(amount, 250.0)
                data[i][7] = is_greater(amount, 500.0)
                data[i][8] = is_greater(amount, 1000.0)
                data[i][9] = zip_code
                #data[i][10] = is_male(name)
                data[i][NUM_FEATURES] = get_candidate(candidate)
            i += 1
            if i % n == 0:
                print("%d%%" % int(float(i)/n*100))

    return data

################################################
#
# 
#
################################################
def convert_to_nd_array(d):
    n = len(d)
    m = NUM_FEATURES
    data = np.zeros(shape=(n,m+1)) # add 1 for y (output)
    for s in range(0,n): # for each sample
        for f in range(0,m+1): # for each feature
            data[s][f] = d[s][f]
    return data

################################################
#
# Get all features from data file
#
################################################
def load_features(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            tmp = line.rstrip().split(',')[:-1]
            data.append(tmp)
    data = convert_to_nd_array(data)
    return data

################################################
#
# Save data matrix to .dat file
#
################################################
def save_features(filename, data):
    n = data.shape[0] 
    m = data.shape[1]
    with open(filename, 'w') as f:
        for i in range(0,n):
            if data[i][NUM_FEATURES] != 0:
                for j in range(0,m):
                    f.write("%d," % data[i][j])
                f.write("\n")

def get_test_sets(d, start, stop):
    train = None
    test = None

    if stop > d.shape[0]:
        print("Contraining end of test data")
        stop = d.shape[0]

    beginning = d[0:start]
    end = d[stop+1:]
    if len(beginning) > 0:
        if len(end) > 0:
            train =  (np.concatenate((beginning,end)))
        else:
            train =  beginning
    else:
        train = end

    test = d[start:stop+1]

    return (train, test)

################################################
#
# 
#
################################################
def test(data, subset_size=10):
    accuracy = []
    correct = 0
    attempts = 0 

    samples = data.shape[0]
    test_size = int(float(samples)/subset_size) # TODO a little error in getting data subsets but...

    for i in range(subset_size):
        start = i*test_size
        end = start + test_size
        train, test = get_test_sets(data, start, end)
        X = train[:,0:NUM_FEATURES]
        y = train[:,-1]
        clf_tree = tree.DecisionTreeClassifier()
        clf_tree.fit(X,y)
        test_data = test[:,0:NUM_FEATURES]
        for i in range(0, test.shape[0]):
            guess = clf_tree.predict(test_data[i])
            if guess == test[i,-1]:
                correct += 1
            attempts += 1
        accuracy.append(float(correct)/attempts)
    accuracy = sum(accuracy) / len(accuracy)
    return accuracy

if __name__ == "__main__":
    #t0 = time.time() # get start time
    #d = get_features(FEC_FILES['iowa'])
    #save_features('IA.dat', d)

    d = load_features("IA.dat")
    print(test(d))
    sys.exit()

    X = d[:,0:NUM_FEATURES]
    y = d[:,-1]
    clf_tree = tree.DecisionTreeClassifier()
    clf_tree.fit(X,y)
    guess = clf_tree.predict([1,0,0,0,0,1,0,0,0,0])
    
    print(guess)
    sys.exit()

    ## timing
    #t = time.time() - t0
    #h = int(t / 3600)
    #t -= h*3600
    #m = int(t / 60)
    #t -= m*60
    #s = int(t)
    #print("Time: %d hours %d minutes %d seconds" % (h, m, s)) 

    # save the features
    save_features('IA.dat', d)
    sys.exit()
