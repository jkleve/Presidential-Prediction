from sklearn.naive_bayes import GaussianNB
from sklearn import tree
import numpy as np
import matplotlib.pyplot as plt
import sys

def read_data(file_name, n_features, n_samples):
    n = n_features
    m = n_samples
    y = np.zeros(shape=(m,1)) 
    arr = np.zeros(shape=(m,n))
    i = 0
    
    with open(file_name) as f:
        for l in f:
            data = [int(d.rstrip()) for d in l.split(',')]
            arr[i] = data[0:n]
            y[i] = data[n]
            i += 1

    return arr, y

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

def gen_2d_feature_set(f1, f2):
    return np.column_stack((f1,f2))

def run_test(x, y, num_samples, num_features):
    num_correct = 0
    for i in range(0,num_samples):
        testx = x[i]
        testy = y[i]
        trainx = get_train_set(x, i)
        trainy = get_train_set(y, i)
        X = trainx.reshape(-1,num_features)
        Y = trainy.reshape(1,-1)[0]
        clf_tree = tree.DecisionTreeClassifier()
        clf_tree.fit(X,Y)
        guess = clf_tree.predict([testx])
        #clf = GaussianNB()
        #clf.fit(X,Y)
        #print(clf.get_params())
        #guess = clf.predict([testx])
        if testy == guess: num_correct += 1
        #print("Testing with %d: NB guess %d, actual %d" % (i+1, guess[0], testy))
    
    return (num_correct/36.0)

def print_results(d):
    import operator
    output = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    print(output)


if __name__ == "__main__":
    num_features = 1
    num_samples = 50
    features, y = read_data('data.txt', num_features, num_samples)
    print(y)
    sys.exit()
    #num_samples = features.shape[0]

    tests = {} 

    # go through each feature
    for i in range(0, num_features):

        x = None
        test_name = ""
        num_f = 0
        # if i == j lets just test that one feature
        if i == j:
            x = features[:,i]
            num_f = 1
            test_name = "%d" % (i+1)
        else:
            x = gen_2d_feature_set(features[:,i], features[:,j])
            num_f = 2
            test_name = "%d,%d" % (i+1,j+1)
        accuracy = run_test(x, y, num_samples, num_f)
        tests[test_name] = accuracy
        #print("%d,%d: %f" % (i,j,accuracy))

    print_results(tests)

    sys.exit()

#plt.plot(x5,y,'ro')
#plt.show()
#sys.exit()

