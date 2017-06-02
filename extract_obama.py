import csv

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

i = 0
total = 0.0
with open('FEC_2012_P80003338_F3P_17A.csv') as csv_file:
    with open('obama_2008_ind_contributions.dat', 'w') as output:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in reader:
            i += 1
            if i > 8:
                state = row[STATE]
                try:
                    amount = float(row[AMOUNT].strip('$'))
                except (ValueError, TypeError):
                    print("Amount '%s' invalid in row %d" % (row[AMOUNT],i))
                output.write("[%s] %7.2f\n" % (state, amount))
                total += amount

print("%.2f" % total)
    
