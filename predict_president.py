#!/bin/python2
import sys
sys.path.append("presidential_summaries")

import csv
import os
import numpy as np
import urllib
from bs4 import BeautifulSoup
from getpass import getpass
from pprint import pprint
import operator
from sklearn import tree
from States import States
import pres_summary

NAME = 0
EMPLOYER = 1
OCCUPATION = 2
DESCRIPTION = 3
CITY = 4
STATE = 5
ZIP = 6
RECEIPT_DATE = 7
AMOUNT = 8
MEMO = 9
REPORT_TYPE = 10
REPORT_YEAR = 11
IMAGE_NUM = 12
TRANSACTION_CODE = 13
OTHER_ID = 14
CANDIDATE_ID = 15
TRANSACTION_PGI = 16

OBAMA_2012 = 'FEC_2012_P80003338_F3P_17A.csv'
ROMNEY_2012 = 'FEC_2012_P80003353_F3P_17A.csv'

################################################
#
# Read from a file above and return a column list
#
################################################
def get_inputs(candidate):
    i = 0
    d = {}
    with open(candidate) as csv_file:
        #with open('obama_2008_ind_contributions.dat', 'w') as output:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in reader:
            i += 1 # skip the first 8 rows. their not actual data
            if i > 8:
                state_abbrev = row[STATE]
                # if they screwed up with state abbreviation, just skip it
                if not state_abbrev in States:
                    continue
                # get state name
                state = States[state_abbrev]
                # try to convert to a float value
                try:
                    amount = float(row[AMOUNT].strip('$'))
                except (ValueError, TypeError):
                    print("Amount '%s' invalid in row %d" % (row[AMOUNT],i))

                # add amount to that state
                if state in d:
                    d[state] += amount
                else:
                    d[state] = amount
    # sort by the state name
    results_sorted = sorted(d.items(), key=operator.itemgetter(0))
    return results_sorted

################################################
#
# convert hash of individual contributions to
# column array
#
################################################
def get_x(hash):
    print(type(hash))
    for k,v in hash.items():
        print(k)

################################################
#
# get the results of election from file
#
################################################
def get_y(filename, n_samples):
    i = 0
    y = np.zeros(shape=(n_samples,1))
    with open(filename, 'r') as f:
        for line in f:
            l = line.split(" ")
            r = int(l[-1].strip())
            y[i] = r
            i += 1
    return y

################################################
#
# get the state name from the <li> element
#
################################################
def get_state(li_elem):
    return li_elem.contents[0].split(" ")[0]

################################################
#
# scrape the results of election
#
################################################
def get_results():
    site = "http://www.smh.com.au/world/us-election/us-election-list-how-each-state-voted-20121107-28y63.html"

    soup = BeautifulSoup(urllib.urlopen(site).read())

    div = soup.find("div", {"class": "article__body"})
    uls = div.find_all("ul")
    i = 1
    results = {}
    for ul in uls:
        lis = ul.find_all("li")
        for li in lis:
            if li.next_element.next_element == u'\n':
                if i == 1:
                    state = get_state(li)
                    results[state] = 1
                    #print("d: %s" % state)
                elif i == 2:
                    state = get_state(li)
                    results[state] = 2
                    #print("r: %s" % state)
                else: break
        i += 1

    results_sorted = sorted(results.items(), key=operator.itemgetter(0))

    with open('20xx_results', 'w') as f:
        for k,v in results_sorted:
            f.write("%s %s\n" % (k, v))

    def get_inputs(x_file):
        with open(x_file, 'r') as f:
            print("not implemented")

################################################
#
#
#
################################################
def gen_ml_input_file(x, y, output_file):
    with open(output_file, 'w') as f:
        print("not implemented")

################################################
#
#
#
################################################
def convert_arr_to_column_arr(arr):
    l = len(arr)
    ret = np.zeros(shape=(l, 1))
    for i in range(0, l):
        ret[i] = arr[i][1]
    return ret

################################################
#
# split array and combine taking one element out
#
################################################
def get_train_set(arr, i):
    beginning = arr[0:i]
    end = arr[i+1:]
    if len(beginning) > 0:
        if len(end) > 0:
            return (np.concatenate((beginning,end)))
        else:
            return beginning
    else:
        return end

################################################
#
# run the test
#
################################################
def run_test(x, y, num_samples, num_features):
    num_correct = 0
    for i in range(0,num_samples):
        testx = x[i]
        testy = y[i]
        trainx = get_train_set(x, i)
        trainy = get_train_set(y, i)
        #X = trainx.reshape(-1,num_features)
        X = trainx
        Y = trainy.reshape(1,-1)[0]
        clf_tree = tree.DecisionTreeClassifier()
        clf_tree.fit(X,Y)
        guess = clf_tree.predict([testx])
        #clf = GaussianNB()
        #clf.fit(X,Y)
        #print(clf.get_params())
        #guess = clf.predict([testx])
        if testy == guess: num_correct += 1
        print("Testing with %d: NB guess %d, actual %d" % (i+1, guess[0], testy))

    return (float(num_correct)/num_samples)

################################################
#
# combine two features
#
################################################
def gen_2d_feature_set(f1, f2):
    return np.column_stack((f1,f2))

################################################
#
# Get presidential summary data
#  load: 0 means don't re-import
#          1 means import from csv files
#  save: 0 means don't save data
#        1 means save data
#
################################################
def get_pres_summaries_data(load=1, save=0):
    data = {}
    if load:
        for candidate in pres_summary.FEC_FILES:
            d = pres_summary.import_summary(candidate)
            data[candidate] = d
            if save: pres_summary.save_summary(d, candidate)
    else:
        if save:
            print("You don't need to select save when not loading.")
            print("Otherwise you need to select load.")
        for candidate in pres_summary.FEC_FILES:
            d = pres_summary.get_summary(candidate)
            data[candidate] = d

    return data
    #if save:


################################################
#
# main
#
################################################
if __name__ == "__main__":
    f1_pres_sum = get_pres_summaries_data(0)
    print(f1_pres_sum)
    sys.exit()

    num_features = 1
    num_samples = 51
    y = get_y('2012_state_results', num_samples)
    i1 = get_inputs(OBAMA_2012) # TODO change to load
    # TODO add read_inputs and save_inputs
    i2 = get_inputs(ROMNEY_2012)
    x1 = convert_arr_to_column_arr(i1)
    x2 = convert_arr_to_column_arr(i2)

    x = gen_2d_feature_set(x1, x2)
    accuracy = run_test(x, y, num_samples, num_features)
    print("Accuracy of %.2f%%\n" % (accuracy*100))
