import csv
import numpy as np
import sexmachine.detector as gender
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

# output (save) filenames
DATA_FILES = {
    'obama_2012':  'presidential_summaries/2012_obama_sum.dat',
    'romney_2012': 'presidential_summaries/2012_romney_sum.dat',
    'mccain_2008': 'presidential_summaries/2008_mccain_sum.dat',
    'obama_2008':  'presidential_summaries/2008_obama_sum.dat'
}

# output (save) files included in 2012 election
election_2012 = [
    'obama_2012',
    'romney_2012'
]
# output (save) files included in 2008 election
election_2008 = [
    'mccain_2008',
    'obama_2008'
]

# the row the actual data starts in csv file
data_line = 16

# the columns where the wanted data is in the csv file for 2012
year_2012_values = {
    #ITEMIZED_CONTRIBUTIONS = 3
    'TOTAL_INDVID_CONTRIBUTIONS': 5,
    'TOTAL_CONTRIBUTIONS':        9,
    'OPERATING_EXPENDITURES':     20
}

# the columns where the wanted data is in the csv file for 2008
year_2008_values = {
    'TOTAL_INDVID_CONTRIBUTIONS': 3,
    'TOTAL_CONTRIBUTIONS':        7,
    'OPERATING_EXPENDITURES':     18
}


################################################
#
# import summary helper to convert to float
#  s: string to convert
#
################################################
def money_string_to_float(s):
    return float(s.strip('$').replace(',',''))

################################################
#
# Get data from FEC csv file
#  candidate: candidate to import. matches with
#     FEC_FILES dictionary above
#
################################################
def import_summary(candidate):
    i = 0
    data = {}

    # get indices of where data will be in csv file
    if candidate in election_2012:
        v = year_2012_values
        TOTAL_INDVID_CONTRIBUTIONS = v['TOTAL_INDVID_CONTRIBUTIONS']
        TOTAL_CONTRIBUTIONS =        v['TOTAL_CONTRIBUTIONS']
        OPERATING_EXPENDITURES =     v['OPERATING_EXPENDITURES']
    elif candidate in election_2008:
        v = year_2008_values
        TOTAL_INDVID_CONTRIBUTIONS = v['TOTAL_INDVID_CONTRIBUTIONS']
        TOTAL_CONTRIBUTIONS =        v['TOTAL_CONTRIBUTIONS']
        OPERATING_EXPENDITURES =     v['OPERATING_EXPENDITURES']
    else: # error handling
        from inspect import currentframe, getframeinfo
        frameinfo = getframeinfo(currentframe())
        print("Error in %s on line %s" % (frameinfo.filename, frameinfo.lineno))

    # read from csv file
    with open(FEC_FILES[candidate]) as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in reader:
            i += 1
            # get data on data line, skip info lines
            if i == data_line:
                #data[ITEMIZED_CONTRIBUTIONS]     = money_string_to_float(row[ITEMIZED_CONTRIBUTIONS])
                data[TOTAL_INDVID_CONTRIBUTIONS] = money_string_to_float(row[TOTAL_INDVID_CONTRIBUTIONS])
                data[TOTAL_CONTRIBUTIONS]        = money_string_to_float(row[TOTAL_CONTRIBUTIONS])
                data[OPERATING_EXPENDITURES]     = money_string_to_float(row[OPERATING_EXPENDITURES])

    return data

################################################
#
# Save imported data into my format as a .dat file.
#  inverse of get_summary
#   h: h or dictionary to save to file
#   candidate: candidate to save data to. Use DATA_FILES
#             dictionary above
#
################################################
def save_summary(h, candidate):
    filename = DATA_FILES[candidate]
    with open(filename, 'w') as f:
        for k,v in h.items():
            f.write("%d,%s\n" % (k,v))

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
        return 1
    return 0

################################################
#
# Guess if occupation is a farmer
#
################################################
def is_farmer(s):
    s = s.lower()
    if "farmer" in s:
        return 1
    return 0

################################################
#
# Guess if occupation is retired
#
################################################
def is_retired(s):
    s = s.lower()
    if "retired" in s:
        return 1
    return 0

################################################
#
# Guess if person is unemployed
#
################################################
def is_unemployed(s):
    s = s.lower()
    if "unemployed" in s:
        return 1
    return 0

################################################
#
# Guess if person is a student
#
################################################
def is_student(s):
    s = s.lower()
    if "unemployed" in s:
        return 1
    return 0

################################################
#
# Guess if person male
#
################################################
def is_male(s):
    s = s.lower().split(',')[1]
    d = gender.Detector()
    if d.get_gender(s) is 'male':
        return 1
    return 0

################################################
#
# Check if v1 is greater than v2
#
################################################
def is_greater(v1, v2):
    if v1 > v2: return 1
    return 0

################################################
#
# Get all features from file
#
################################################
def get_features(filename):
    n = count_samples(filename)
    m = NUM_FEATURES
    data = np.zeros(shape=(n,m))
    i = 0
    
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            i += 1

            if i > 1: # skip first line
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
                data[i][5] = is_greater(amount, 100)
                data[i][6] = is_greater(amount, 250)
                data[i][7] = is_greater(amount, 500)
                data[i][8] = is_greater(amount, 1000)
                data[i][9] = zip_code
                data[i][10] = is_male(name)

    return data

################################################
#
# Save data matrix to .dat file
#
################################################
def save_features(filename, data):
    with open(filename, 'w') as f:
        for row in data:
            print(row)

if __name__ == "__main__":
    d = get_features("P00000001-IA.csv")
    print(d)
    sys.exit()
    d = []
    with open("P00000001-IA.csv") as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            if row[1] not in d:
                d.append(row[1])
                d.append(row[2])
    for i in d:
        print("%s" % (i))

