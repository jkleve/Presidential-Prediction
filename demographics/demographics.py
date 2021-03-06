import csv
import numpy as np
import sexmachine.detector as gender
from sklearn import tree, neural_network
import gender_detector
import random
import time
import sys
from demo_histograms import gen_histogram

#NUM_FEATURES = 9
#NUM_FEATURES = 13 # with gender
#NUM_FEATURES = 5

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
def get_features(filename, num_features):
    n = count_samples(filename)
    print("%d number of lines" % n)
    m = num_features
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
                data[i][10] = occupation
                #data[i][10] = is_male(name)
                data[i][m] = get_candidate(candidate)
            i += 1
            if i % n == 0:
                print("%d%%" % int(float(i)/n*100))

    return data

################################################
#
#
#
################################################
def convert_to_nd_array(d, num):
    n = len(d)
    m = num
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
    num_features = len(data[0]) - 1
    data = convert_to_nd_array(data, num_features)
    return (num_features, data)

################################################
#
# Save data matrix to .dat file
#
################################################
def save_features(filename, data, num_features):
    one_feature = True
    n = data.shape[0]
    if num_features != 1:
        m = data.shape[1]
        one_feature = False

    with open(filename, 'w') as f:
        for i in range(0,n):
            if one_feature:
                f.write("%d\n" % data[i])
            else:
                #if data[i][num_features] != 0: # TODO should I remove? could be useful data
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
def test(data, num_features, subset_size=10):
    accuracy = []
    correct = 0
    attempts = 0

    samples = data.shape[0]
    test_size = int(float(samples)/subset_size) # TODO a little error in getting data subsets but...

    for i in range(subset_size):
        start = i*test_size
        end = start + test_size
        train, test = get_test_sets(data, start, end)
        X = train[:,0:num_features]
        X = np.zeros(shape=(train.shape[0],1))
        y = train[:,-1]
        #save_features("x.dat", X, 1)
        #save_features("y.dat", y, 1)
        #sys.exit()
        clf_tree = tree.DecisionTreeClassifier()
        clf_tree.fit(X,y)
        #nn = neural_network.MLPClassifier()
        #nn.fit(X,y)
        test_data = test[:,0:num_features]
        for i in range(0, test.shape[0]):
            guess = clf_tree.predict(test_data[i])
            #guess = nn.predict(test_data[i])
            if guess == test[i,-1]:
                correct += 1
            attempts += 1
        accuracy.append(float(correct)/attempts)
    accuracy = sum(accuracy) / len(accuracy)
    return accuracy

################################################
#
#
#
################################################
def get_out_of_bag_error(data, num_features, feature):
    accuracy_with_feature = test(data, num_features)

    d1 = d2 = None
    n = data.shape[1]
    b = [i for i in range(0,feature-1)]
    e = [i for i in range(feature,n)]

    if len(b) > 0:
        d1 = data[:,b]
    if len(e) > 0:
        d2 = data[:,e]

    if d1 is not None and d2 is not None:
        data = np.column_stack((d1,d2))
    elif d1 is not None:
        data = d1
    else:
        data = d2

    #save_features("data_testing_wo_feature.dat", data, NUM_FEATURES-1)
    #sys.exit()
    accuracy_without = test(data, num_features-1)

    return (accuracy_with_feature, accuracy_without)

def get_three_random_nums(num_features):
    f1 = random.randint(1,num_features)
    f2 = random.randint(1,num_features)
    f3 = random.randint(1,num_features)
    return f1, f2, f3

def get_four_random_nums(num_features):
    f1 = random.randint(1,num_features)
    f2 = random.randint(1,num_features)
    f3 = random.randint(1,num_features)
    f4 = random.randint(1,num_features)
    return f1, f2, f3, f4

def get_four_features(num_features):
    f1, f2, f3, f4 = get_four_random_nums(num_features)
    while f1 == f2 or f1 == f3 or f1 == f4 or f2 == f3 or f2 == f4 or f3 == f4:
        f1, f2, f3, f4 = get_four_random_nums(num_features)
    return f1, f2, f3, f4

def extract_four_features(data, f1, f2, f3, f4):
    return data[:,[f1-1,f2-1,f3-1,f4-1,-1]]

def extract_three_features(data, f1, f2, f3):
    return data[:,[f1-1,f2-1,f3-1,-1]]

def extract_one_features(data, f1):
    return data[:,[f1-1,-1]]

if __name__ == "__main__":
    t0 = time.time() # get start time
    #d = get_features(FEC_FILES['iowa'])
    #save_features('IA.dat', d)

    num_features, d = load_features("IA_gender.dat")

    # check the data to see how ofter each candidate is contributed to
    n = d.shape[0]
    dem = 0
    rep = 0
    lib = 0
    total = 0
    for i in range(0,n):
        party = d[i][13]
        if party == DEMOCRATIC:
            dem += 1
        elif party == REPUBLICAN:
            rep += 1
        elif party == LIBERTARIAN:
            lib += 1
        else:
            print("unknown party")
        total += 1
    dem_occ = float(dem)/total
    rep_occ = float(rep)/total
    lib_occ = float(lib)/total
    print("Dem: %f, Rep: %f, Lib: %f" % (dem_occ, rep_occ, lib_occ))
    sys.exit()
    #for row in d:


    #num_features, d = load_features("IA-test.dat")
    #num_features, d = load_features("IA.dat")
    #save_features("data_after_load.dat", d, NUM_FEATURES)

    # get out of bag error and save to accuracies.dat
    #with open("accuracies1.dat", 'w') as f:
    #    for i in range(1, num_features+1):
    #        with_feature, wo_feature = get_out_of_bag_error(d, num_features, i)
    #        wo_f = 100.0*wo_feature
    #        f.write("feature %2d: %6.2f%%\n" % (i, wo_f))

    #print(test(d))

    accuracies = []
    accuracies_string = []
    bins = np.arange(65,85,1)
    f1 = 13
    num_tests = 40

    data = extract_one_features(d, f1)
    a = test(data, 1)
    a = 100.0*a
    print(a)
    sys.exit()

    filename = "feature" + str(f1) + ".dat"
    with open(filename, 'w') as f:
        for i in range(0, num_tests): # get 20 tests
            f2, f3, f4 = get_three_random_nums(num_features)
            while f1 == f2 or f1 == f3 or f1 == f4 or f2 == f3 or f2 == f4 or f3 == f4:
                 f2, f3, f4 = get_three_random_nums(num_features)
            data = extract_four_features(d, f1, f2, f3, f4)
            accuracy = test(data, 4)
            accuracy = 100.0*accuracy
            test_name = "%2d,%2d,%2d,%2d" % (f1, f2, f3, f4)
            f.write("%s: %5.2f%%\n" % (test_name, accuracy))
            accuracies.append(accuracy)
            s = "%s: %5.2f%%" % (test_name, accuracy)
            accuracies_string.append(s)
    print(accuracies_string)
    print(time.time() - t0)
    gen_histogram(accuracies, bins)

    sys.exit()











    f1, f2, f3, f4 = get_four_features(num_features)
    f1 = 1
    f2 = 2
    f3 = 3
    f4 = 4
    #data = extract_one_features(d, f1)
    data = extract_three_features(d, f1, f2, f3)
    accuracy = test(data, 3)
    accuracy = 100.0*accuracy
    filename = str(f1) + str(f2) + str(f3)
    #with open(filename, 'w') as f:
    #    f.write("features %d: accuracy %6.2f%%\n" % \
    #            (f1, accuracy))
    print(accuracy)
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
    save_features('IA.dat', d, NUM_FEATURES)
    sys.exit()
