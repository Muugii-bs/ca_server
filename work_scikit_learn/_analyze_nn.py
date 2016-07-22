from sklearn.neural_network import MLPClassifier
from create_dataset import create_dataset
import numpy as np
np.set_printoptions(threshold=np.nan)
import sys

X, Y = [], []

def run():
    #clf = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(8, 4), random_state=1, verbose=10)
    clf = MLPClassifier(hidden_layer_sizes=(100, 100), max_iter=10, alpha=1e-4,
                    algorithm='sgd', verbose=10, tol=1e-4, random_state=1,
                    learning_rate_init=.1)
    TRAIN_SIZE = int(len(X) * 0.8) 
    X_train = X[:TRAIN_SIZE]
    Y_train = Y[:TRAIN_SIZE]
    X_test = X[TRAIN_SIZE:]
    Y_test = Y[TRAIN_SIZE:]
    clf.fit(X_train, Y_train)
    res = clf.predict_proba(X_test)
    print("Training set score: %f" % clf.score(X_train, Y_train))
    print("Test set score: %f" % clf.score(X_test, Y_test))
    #for i in range(0, len(Y[TRAIN_SIZE:])):
        #print(np.array_str(res[i]) + "\t" + " ".join([str(j) for j in Y[TRAIN_SIZE:][i]]))
        #tmp = [False] * len(Y[TRAIN_SIZE:])
        #tmp[i] = np.array_equal(Y[TRAIN_SIZE:][i], res[i])
    #print(tmp)

def main(): 
    global X, Y
    X, Y = np.load('dataset.npy'), np.load('label.npy')
    run()

if __name__ == '__main__':
    main()
