from sklearn.neural_network import MLPClassifier
from create_dataset import create_dataset
import numpy as np
np.set_printoptions(threshold=np.nan)
import sys

X, Y = [], []

def run():
    clf = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(8, 8), random_state=1)
    TRAIN_SIZE = int(len(X) * 0.8) 
    TEST_SIZE = len(X) - TRAIN_SIZE
    print(clf.fit(X[:TRAIN_SIZE], Y[:TRAIN_SIZE]))
    print(Y[TRAIN_SIZE:])
    res = clf.predict(X[TRAIN_SIZE:])
    print(res)
    for i in range(0, len(Y[TRAIN_SIZE:])):
        tmp = [False] * len(Y[TRAIN_SIZE:])
        tmp[i] = np.array_equal(Y[TRAIN_SIZE:][i], res[i])
    #print(tmp)

def main(): 
    global X, Y
    X, Y = create_dataset()
    run()

if __name__ == '__main__':
    main()
