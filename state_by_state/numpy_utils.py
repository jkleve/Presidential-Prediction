import numpy as np

################################################
#
# Add 2 np arrays row wise
#
################################################
def add_row_to_array(a, b):
    if a.shape == (0,0):
        return b

    if a.shape[1] != b.shape[1]:
        print("Number of columns doesn't match. %d vs %d" % (a.shape[1], b.shape[1]))
        print("Can't add row to array")

    return np.concatenate((a,b))

################################################
#
# Add 2 np arrays column wise
#
################################################
def add_column_to_array(a, b):
    if a.shape == (0,0):
        return b

    if a.shape[0] != b.shape[0]:
        print("Number of columns doesn't match. %d vs %d" % (a.shape[0], b.shape[0]))
        print("Can't add row to array")

    return np.column_stack((a,b))

################################################
#
# Split one ndarray into two
#  start: start row of ndarray to extract
#  stop: stop row of ndarray to extract
#
################################################
def split_into_two_ndarrays_by_rows(d, start, stop):
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
# Split one ndarray into two
#  start: start column of ndarray to extract
#  stop: stop column of ndarray to extract
# TODO nothing implemented besides the extracted array
# TODO no error checking on ndarray size
################################################
def split_into_two_ndarrays_by_column(d, start, stop):
    return (d[:,start:stop], np.zeros(shape=(0,0)))
