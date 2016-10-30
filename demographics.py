import csv
import numpy as np
import sexmachine.detector as gender
import gender_detector
import sys

NUM_FEATURES = 11

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
    'iowa':  'demographics/P00000001-IA.csv'
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
    g = d1.guess(s)
    print('name is %s' % s)
    print('first detector guessed %s' % g)
    
    if g == 'male':
        print('returning male')
        return 1
    elif g == 'female':
        print('returning female')
        return 0

    # if first (faster) detector can't guess it
    # try second detector
    print('going to detector 2')
    d2 = gender.Detector()
    g = d2.get_gender(s)
    if g == 'male':
        print('male')
        return 1
    print('female')
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
# Get all features from file
#
################################################
def get_features(filename):
    n = count_samples(filename)
    print("%d number of lines" % n)
    m = NUM_FEATURES
    data = np.zeros(shape=(n,m))
    print_matrix(data)
    i = -1 
    
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:

            if i >= 0 and i < n: # skip first line
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
                print('\n')
                data[i][10] = is_male(name)
            i += 1

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
            for j in range(0,m):
                f.write("%d," % data[i][j])
            f.write("\n")

if __name__ == "__main__":
    d = get_features("P00000001-IA_subset.csv")
    save_features('test_output.dat', d)
    sys.exit()
