import csv
import numpy as np
import sys

from numpy_utils import add_row_to_array
from States import States
from csv_file_data import CANDIDATES, \
                          CANDIDATE_ID, \
                          CONTRIBUTION_AMOUNT, \
                          GENERAL_ELECTION_CANDIDATES, \
                          DEMOCRATIC, \
                          REPUBLICAN, \
                          LIBERTARIAN

DEBUG = 0

################################################
#
# Get candidate
#
################################################
def get_candidate_party(candidate):
    try:
        party = CANDIDATES[candidate]
    except:
        raise
    return party

################################################
#
# Get all features from data file
#
################################################
def get_features(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            data.append(line.rstrip().split(','))
    return np.array(data)

################################################
#
# Save data matrix to .dat file
#
################################################
def save_features(filename, features):
    n = features.shape[0]
    m = features.shape[1]

    with open(filename, 'w') as f:
        for i in range(0,n):
            if m == 1:
                f.write("%d\n" % features[i])
            else:
                for j in range(0,m):
                    if j == m-1:
                        f.write("%d" % features[i][j])
                    else:
                        f.write("%d," % features[i][j])
                f.write("\n")

################################################
#
# Loads all features from csv file.
#  Returns one sample
#
################################################
def load_features_for_sample(filename, year):

    num_features = 4

    data = np.zeros(shape=(1,num_features))

    # variables for gathering feature numbers
    dem_party_num_cont = 0
    dem_party_money = 0.0
    rep_party_num_cont = 0
    rep_party_money = 0.0
    lib_party_num_cont = 0
    lib_party_money = 0.0
    dem_cand_num_cont = 0
    dem_cand_money = 0.0
    rep_cand_num_cont = 0
    rep_cand_money = 0.0
    total_num_cont = 0
    total_money = 0.0
    total_cand_num_cont = 0
    total_cand_money = 0.0

    i = -1

    # get feature data
    with open(filename, 'r') as f:

        reader = csv.reader(f, delimiter=',', quotechar='"')

        for row in reader:

            if i >= 0: # skip first line

                candidate = row[CANDIDATE_ID]
                try:
                    party = get_candidate_party(candidate)
                except:
                    print("No candidate %s in %s" % (candidate, year))
                    sys.exit()

                try:
                    amount = float(row[CONTRIBUTION_AMOUNT])
                except ValueError:
                    print("Couldn't convert %s to float" % row[CONTRIBUTION_AMOUNT])
                    continue

                if party == DEMOCRATIC:
                    dem_party_num_cont += 1
                    dem_party_money += amount

                    if candidate in GENERAL_ELECTION_CANDIDATES[year]:
                        dem_cand_num_cont += 1
                        dem_cand_money += amount
                        total_cand_num_cont += 1
                        total_cand_money += amount

                elif party == REPUBLICAN:
                    rep_party_num_cont += 1
                    rep_party_money += amount

                    if candidate in GENERAL_ELECTION_CANDIDATES[year]:
                        rep_cand_num_cont += 1
                        rep_cand_money += amount
                        total_cand_num_cont += 1
                        total_cand_money += amount

                elif party == LIBERTARIAN: # TODO change to al other
                    lib_party_num_cont += 1
                    lib_party_money += amount

                else:
                    continue

                # keep track of all contibutions
                total_num_cont += 1
                total_money += amount

            i += 1

        # put features in terms of percentage of total contibutions
        v1 = float(dem_party_num_cont) / total_num_cont
        v2 = dem_party_money / total_money
        v3 = float(rep_party_num_cont) / total_num_cont
        v4 = rep_party_money / total_money
        v5 = float(lib_party_num_cont) / total_num_cont
        v6 = lib_party_money / total_money
        v7 = float(dem_cand_num_cont) / total_cand_num_cont
        v8 = dem_cand_money / total_cand_money
        v9 = float(rep_cand_num_cont) / total_cand_num_cont
        v10 = rep_cand_money / total_cand_money

        # feature 1. what party got more contributions
        if v1 > v3:
            f1 = 1
        else:
            f1 = 2
        # feature 2: what party got more money
        if v2 > v4:
            f2 = 1
        else:
            f2 = 2
        # feature 3: what candidate got more contributions
        if v7 > v9:
            f3 = 1
        else:
            f3 = 2
        # feature 4: what candidate got more money
        if v8 > v10:
            f4 = 1
        else:
            f4 = 2

        # put features in data array
        data[0][0] = f1
        data[0][1] = f2
        data[0][2] = f3
        data[0][3] = f4
        #data[0][4] = f5
        #data[0][5] = f6
        #data[0][6] = f7
        #data[0][7] = f8
        #data[0][8] = f9
        #data[0][9] = f10

        if DEBUG:
            print(data)
            # these next values should add up to 1.0
            print(v1+v3+v5)
            print(v2+v4+v6)
            print(v7+v9)
            print(v8+v10)

    return data

################################################
#
# Loads one state data
#  returns np array for this state
#
################################################
def load_old_state_data(state):
    filename_beg = "P00000001-"
    filename_end = ".csv"
    filename = filename_beg + state + filename_end

    data_2008_dir = "csvs_2008/"
    data_2012_dir = "csvs_2012/"
    data_2008_f = data_2008_dir + filename
    data_2012_f = data_2012_dir + filename

    d_2008 = load_features_for_sample(data_2008_f, '2008')
    d_2012 = load_features_for_sample(data_2012_f, '2012')

    data = np.concatenate((d_2008,d_2012))

    return data

################################################
#
# Load all old state data
#  returns np array of all old state data
#  NOTE: The order is dependent on the key in states
#  In my case it's sorted by state abbreviation
#
################################################
def load_all_state_data(states):
    ret = np.empty(shape=(0,0))

    for state, data in sorted(states.items()):
        #print(state)
        d = load_old_state_data(state)
        ret = add_row_to_array(ret, d)

    return ret


def load_new_state_data(state):
    filename_beg = "P00000001-"
    filename_end = ".csv"
    filename = filename_beg + state + filename_end

    data_2016_dir = "csvs_2016/"
    data_2016_f = data_2016_dir + filename

    return load_features_for_sample(data_2016_f, '2016')

def load_all_new_state_data(states):
    ret = np.empty(shape=(0,0))

    for state, data in sorted(states.items()):
        #print(state)
        d = load_new_state_data(state)
        ret = add_row_to_array(ret, d)

    return ret

################################################
#
# Loads one state output
#  returns np array for this state
#
################################################
def get_output_for_state(state):
    num_samples = 2

    data = np.zeros(shape=(num_samples,1))

    data[0] = States[state]['2008']
    data[1] = States[state]['2012']

    return data

################################################
#
# Loads all state output
#  returns np array for all states
#
################################################
def get_all_outputs(states):
    ret = np.empty(shape=(0,0))

    for state, data in sorted(states.items()):
        #print(state)
        d = get_output_for_state(state)
        ret = add_row_to_array(ret, d)

    return ret

################################################
#
# Loads from csv files and saves to one dat file
#
################################################
def load_and_save_all_features(dat_file, states):
    features = load_all_state_data(states)
    save_features(dat_file, features)

################################################
#
# Loads from csv files and saves to one dat file
#
################################################
def load_and_save_all_new_features(dat_file, states):
    features = load_all_new_state_data(states)
    save_features(dat_file, features)
