import csv
import sys

CANDIDATE_ID = 1
CANDIDATE_NAME = 2

def get_candidates(filename):
    ids = []
    data = []
    # get feature data
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')

        for row in reader:
            cand_id = row[CANDIDATE_ID]
            cand_name = row[CANDIDATE_NAME]
            if cand_id not in ids:
                ids.append(cand_id)
                data.append((cand_id, cand_name))

    print(len(ids))
    return data

if __name__ == "__main__":
    d = get_candidates("csvs_2012/P00000001-IA.csv")
    print(d)
