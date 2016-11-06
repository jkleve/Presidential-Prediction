import csv
import numpy as np
import time

# added parent directory
import sys
sys.path.append("..")

# Machine Learning algorithms
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC

# my variables
from States import States
# my functions
from csv_file_data import DEMOCRATIC, \
                          REPUBLICAN, \
                          LIBERTARIAN, \
                          CANDIDATES, \
                          GENERAL_ELECTION_CANDIDATES
from numpy_utils import add_row_to_array, \
                        add_column_to_array, \
                        split_into_two_ndarrays_by_rows, \
                        split_into_two_ndarrays_by_column
from handle_data import get_features, \
                        get_all_outputs, \
                        load_new_state_data, \
                        load_all_new_state_data, \
                        load_and_save_all_features, \
                        load_and_save_all_new_features

DEBUG = 0

################################################
#
#
#
################################################
def test(data, subset_size=10):
    accuracy = []
    correct = 0
    attempts = 0

    num_features = data.shape[1] - 1

    samples = data.shape[0]
    test_size = int(float(samples)/subset_size) # TODO a little error in getting data subsets but...

    for i in range(subset_size):
        start = i*test_size
        end = start + test_size
        train, test = split_into_two_ndarrays_by_rows(data, start, end)
        X = train[:,0:num_features]
        y = train[:,-1]
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

# train and test with subsets of 2008 & 2012 data
def test_state(state):
    print("implement")

# train with 2008 & 2012, predict 2016
def predict_state(state):
    print("implement")

################################################
#
# Debuging function TODO update to work with new files
#
################################################
def compare_features_to_outputs():
    for k, v in States.items():
        a1 = np.zeros(shape=(2,1)) # dem party num
        a2 = np.zeros(shape=(2,1)) # dem party money
        a3 = np.zeros(shape=(2,1)) # dem cand num
        a4 = np.zeros(shape=(2,1)) # dem cand money
        X = load_old_state_data(k)
        y = get_output_for_state(k)
        if X[0][0] > X[0][2]:
            a1[0] = 1
        else:
            a1[0] = 2
        if X[0][1] > X[0][3]:
            a2[0] = 1
        else:
            a2[0] = 2
        if X[0][6] > X[0][8]:
            a3[0] = 1
        else:
            a3[0] = 2
        if X[0][7] > X[0][9]:
            a4[0] = 1
        else:
            a4[0] = 2

        if X[1][0] > X[1][2]:
            a1[1] = 1
        else:
            a1[1] = 2
        if X[1][1] > X[1][3]:
            a2[1] = 1
        else:
            a2[1] = 2
        if X[1][6] > X[1][8]:
            a3[1] = 1
        else:
            a3[1] = 2
        if X[1][7] > X[1][9]:
            a4[1] = 1
        else:
            a4[1] = 2
        print(k)
        print(a1)
        print(a2)
        print(a3)
        print(a4)
        print(y)

################################################
#
# Go through testing each feature by itself
#  returns array of accuracies.
#   length of array will be how many features
#    there are.
#
################################################
def test_each_features_independently(X, y, print_output=False):
    accuracy = []

    data = add_column_to_array(X, y)
    acc = test(data)
    acc = 100.0*acc
    accuracy.append(acc)

    for i in range(0, X.shape[1]):
        x = split_into_two_ndarrays_by_column(X, i, i+1)[0]
        data = add_column_to_array(x, y)

        acc = test(data)
        acc = 100.0*acc
        accuracy.append(acc)

    if print_output:
        for i, acc in enumerate(accuracy):
            print("%d: %6.2f%%" % (i, acc))

    return accuracy

#==============================================#
#                                              #
#                  Main                        #
#                                              #
#==============================================#
if __name__ == "__main__":

    # output
    prediction = {}
    clinton = 0
    trump = 0
    total = 0

    # get old data
    train_X = get_features('state_features.dat')
    train_y = get_all_outputs(States)

    # get new data
    test_X = get_features('new_state_features.dat')

    # get ml algorithm
    clf = DecisionTreeClassifier()
    #clf = LinearSVC()
    # fit ml algorithm with old data
    clf.fit(train_X, train_y)

    # predict each state
    for i, state in enumerate(sorted(States.items())):
        abbrev = state[0]
        data = state[1]
        votes = data['votes']

        p = clf.predict(test_X[i])

        if p == 1:
            clinton += votes
        else:
            trump += votes

        total += votes
        prediction[abbrev] = p

    print("Clinton: %d" % clinton)
    print("Trump:   %d" % trump)
    print("Total:  %d" % total)

    for state, val in sorted(prediction.items()):
        print("%s: %d" % (state, val))

    sys.exit()





    X = get_features('state_features.dat')
    y = get_all_outputs(States)

    acc = {}
    for i in range(0, 4):
        for j in range(0, 4):
            x = X[:,[i,j]]
            data = add_column_to_array(x, y)
            a = test(data)
            nm = str(i) + str(j)
            acc[nm] = a

    for key, value in sorted(acc.iteritems(), key=lambda (k,v): (v,k)):
        print "%s: %s" % (key, value)

    #accuracy = test_each_features_independently(X, y, True)
